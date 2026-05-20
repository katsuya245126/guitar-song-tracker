import os
import json
import re
import logging
from flask import Flask, request, jsonify, render_template, send_file, abort
from functools import wraps
from io import BytesIO
import psycopg2
from psycopg2.extras import RealDictCursor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


def require_password(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        password = os.environ.get('ADMIN_PASSWORD')
        if password and request.headers.get('X-Admin-Password') != password:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated


def get_conn():
    return psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS songs (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL DEFAULT '',
                    tuning TEXT NOT NULL,
                    capo INTEGER NOT NULL DEFAULT 0,
                    status TEXT NOT NULL DEFAULT 'wishlist'
                )
            ''')
        conn.commit()


def row_to_dict(row):
    return {
        'id': row['id'],
        'title': row['title'],
        'link': row['link'],
        'tuning': row['tuning'],
        'capo': row['capo'],
        'status': row['status'],
    }


def songs_match(a, b):
    return a['title'].strip().lower() == b['title'].strip().lower()


def youtube_embed_url(link):
    if not link:
        return None
    match = re.search(
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})',
        link
    )
    return f"https://www.youtube.com/embed/{match.group(1)}" if match else None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/song/<int:song_id>')
def song_detail(song_id):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM songs WHERE id = %s', (song_id,))
            row = cur.fetchone()
    if not row:
        return "Song not found", 404
    song = row_to_dict(row)
    embed_url = youtube_embed_url(song.get('link', ''))
    return render_template('song.html', song=song, index=song_id, embed_url=embed_url)


@app.route('/api/songs', methods=['GET'])
def get_songs():
    query = request.args.get('q', '').strip()
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if query:
                cur.execute(
                    'SELECT * FROM songs WHERE title ILIKE %s ORDER BY id',
                    (f'%{query}%',)
                )
            else:
                cur.execute('SELECT * FROM songs ORDER BY id')
            rows = cur.fetchall()
    return jsonify([row_to_dict(r) for r in rows])


@app.route('/api/songs', methods=['POST'])
@require_password
def add_song():
    data = request.get_json()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO songs (title, link, tuning, capo, status) VALUES (%s, %s, %s, %s, %s)',
                (data['title'], data.get('link', ''), data['tuning'], data['capo'], data.get('status', 'wishlist'))
            )
        conn.commit()
    logging.info(f"Added song: {data['title']}")
    return jsonify({'ok': True}), 201


@app.route('/api/songs/<int:song_id>', methods=['PUT'])
@require_password
def update_song(song_id):
    data = request.get_json()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE songs SET title=%s, link=%s, tuning=%s, capo=%s, status=%s WHERE id=%s',
                (data['title'], data.get('link', ''), data['tuning'], data['capo'], data.get('status', 'wishlist'), song_id)
            )
            updated = cur.rowcount
        conn.commit()
    if not updated:
        return jsonify({'error': 'Not found'}), 404
    logging.info(f"Updated song {song_id}: {data['title']}")
    return jsonify({'ok': True})


@app.route('/api/songs/<int:song_id>', methods=['DELETE'])
@require_password
def delete_song(song_id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM songs WHERE id = %s RETURNING title', (song_id,))
            row = cur.fetchone()
        conn.commit()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    logging.info(f"Deleted song {song_id}: {row[0]}")
    return jsonify({'ok': True})


@app.route('/api/export')
def export_songs():
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT title, link, tuning, capo, status FROM songs ORDER BY id')
            rows = cur.fetchall()
    data = json.dumps([dict(r) for r in rows], indent=4).encode('utf-8')
    return send_file(
        BytesIO(data),
        mimetype='application/json',
        as_attachment=True,
        download_name='guitar_songs.json'
    )


@app.route('/api/import', methods=['POST'])
@require_password
def import_songs():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    try:
        incoming = json.loads(file.read().decode('utf-8'))
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    required = {'title', 'tuning', 'capo'}
    for song in incoming:
        song.setdefault('status', 'wishlist')
        song.setdefault('link', '')
        if not required.issubset(song.keys()):
            return jsonify({'error': 'Invalid song format'}), 400

    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute('SELECT * FROM songs ORDER BY id')
            existing = [row_to_dict(r) for r in cur.fetchall()]

    duplicates = []
    new_songs = []
    for song in incoming:
        if any(songs_match(song, e) for e in existing):
            duplicates.append(song)
        else:
            new_songs.append(song)

    return jsonify({'new': new_songs, 'duplicates': duplicates, 'existing': existing})


@app.route('/api/import/confirm', methods=['POST'])
@require_password
def import_confirm():
    data = request.get_json()
    new_songs = data.get('new', [])
    duplicates = data.get('duplicates', [])
    overwrite = data.get('overwrite', False)

    with get_conn() as conn:
        with conn.cursor() as cur:
            if overwrite:
                for dup in duplicates:
                    cur.execute(
                        'UPDATE songs SET link=%s, tuning=%s, capo=%s, status=%s WHERE LOWER(title)=%s',
                        (dup.get('link', ''), dup['tuning'], dup['capo'], dup.get('status', 'wishlist'), dup['title'].lower())
                    )
            for song in new_songs:
                cur.execute(
                    'INSERT INTO songs (title, link, tuning, capo, status) VALUES (%s, %s, %s, %s, %s)',
                    (song['title'], song.get('link', ''), song['tuning'], song['capo'], song.get('status', 'wishlist'))
                )
        conn.commit()

    logging.info(f"Import: {len(new_songs)} added, {len(duplicates)} duplicates ({'overwritten' if overwrite else 'skipped'})")
    return jsonify({'ok': True, 'added': len(new_songs), 'duplicates_handled': len(duplicates)})


with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=True)
