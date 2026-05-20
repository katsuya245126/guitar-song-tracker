import os
import json
import re
import logging
from flask import Flask, request, jsonify, render_template, send_file
from io import BytesIO

logging.basicConfig(filename='myProgramLog.txt',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
DB_FILE = os.path.join(os.path.dirname(__file__), 'guitar_songs.json')


def read_songs():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return []


def write_songs(songs):
    with open(DB_FILE, 'w') as f:
        json.dump(songs, f, indent=4)


def songs_match(a, b):
    return a['title'].strip().lower() == b['title'].strip().lower()


def youtube_embed_url(link):
    """Extract YouTube video ID and return embed URL, or None if not a YouTube link."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, link)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/song/<int:index>')
def song_detail(index):
    songs = read_songs()
    if index < 0 or index >= len(songs):
        return "Song not found", 404
    song = songs[index]
    embed_url = youtube_embed_url(song.get('link', ''))
    return render_template('song.html', song=song, index=index, embed_url=embed_url)


@app.route('/api/songs', methods=['GET'])
def get_songs():
    query = request.args.get('q', '').strip()
    songs = read_songs()
    for s in songs:
        s.setdefault('status', 'wishlist')
    if query:
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        songs = [s for s in songs if pattern.search(s['title'])]
    return jsonify(songs)


@app.route('/api/songs', methods=['POST'])
def add_song():
    data = request.get_json()
    songs = read_songs()
    songs.append({
        'title': data['title'],
        'link': data['link'],
        'tuning': data['tuning'],
        'capo': data['capo'],
        'status': data.get('status', 'wishlist'),
    })
    write_songs(songs)
    logging.info(f"Added song: {data['title']}")
    return jsonify({'ok': True}), 201


@app.route('/api/songs/<int:index>', methods=['PUT'])
def update_song(index):
    data = request.get_json()
    songs = read_songs()
    if index < 0 or index >= len(songs):
        return jsonify({'error': 'Not found'}), 404
    songs[index] = {
        'title': data['title'],
        'link': data['link'],
        'tuning': data['tuning'],
        'capo': data['capo'],
        'status': data.get('status', 'wishlist'),
    }
    write_songs(songs)
    logging.info(f"Updated song at index {index}: {data['title']}")
    return jsonify({'ok': True})


@app.route('/api/songs/<int:index>', methods=['DELETE'])
def delete_song(index):
    songs = read_songs()
    if index < 0 or index >= len(songs):
        return jsonify({'error': 'Not found'}), 404
    removed = songs.pop(index)
    write_songs(songs)
    logging.info(f"Deleted song: {removed['title']}")
    return jsonify({'ok': True})


@app.route('/api/export')
def export_songs():
    data = json.dumps(read_songs(), indent=4).encode('utf-8')
    return send_file(
        BytesIO(data),
        mimetype='application/json',
        as_attachment=True,
        download_name='guitar_songs.json'
    )


@app.route('/api/import', methods=['POST'])
def import_songs():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    try:
        incoming = json.loads(file.read().decode('utf-8'))
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    # Validate basic structure
    required = {'title', 'tuning', 'capo'}
    for song in incoming:
        song.setdefault('status', 'wishlist')
        song.setdefault('link', '')
        if not required.issubset(song.keys()):
            return jsonify({'error': 'Invalid song format'}), 400

    existing = read_songs()
    duplicates = []
    new_songs = []

    for song in incoming:
        if any(songs_match(song, e) for e in existing):
            duplicates.append(song)
        else:
            new_songs.append(song)

    # Return the analysis so the frontend can ask the user what to do
    return jsonify({
        'new': new_songs,
        'duplicates': duplicates,
        'existing': existing,
    })


@app.route('/api/import/confirm', methods=['POST'])
def import_confirm():
    data = request.get_json()
    new_songs = data.get('new', [])
    duplicates = data.get('duplicates', [])
    overwrite = data.get('overwrite', False)  # True = replace duplicates, False = skip

    existing = read_songs()

    if overwrite:
        for dup in duplicates:
            for i, e in enumerate(existing):
                if songs_match(dup, e):
                    existing[i] = dup
                    break

    existing.extend(new_songs)
    write_songs(existing)
    logging.info(f"Import confirmed: {len(new_songs)} added, {len(duplicates)} duplicates ({'overwritten' if overwrite else 'skipped'})")
    return jsonify({'ok': True, 'added': len(new_songs), 'duplicates_handled': len(duplicates)})


if __name__ == '__main__':
    app.run(debug=True)
