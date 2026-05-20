# Guitar Song Tracker

A web app for keeping track of songs you're learning on guitar. Store each song's tuning, capo position, a YouTube link, and a learning status. Data is persisted in a PostgreSQL database.

## Features

- Add, edit, and delete songs
- Filter by status (Wishlist, In Progress, Learned), tuning, and capo
- Search by title
- Song detail page with embedded YouTube video
- Import and export your library as a JSON file

## Running locally

Requires Python 3, Flask, and a PostgreSQL database (e.g. [Neon](https://neon.tech) free tier).

```bash
pip install -r requirements.txt
export DATABASE_URL="your-postgres-connection-string"
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.
