import sqlite3

DB_FILE = "../anime.db"

def get_connection():
    """Connects to the SQLite database"""
    return sqlite3.connect(DB_FILE)

def init_db():
    """Creates the anime table if it doesn't exist"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            genre TEXT,
            release_date TEXT,
            image TEXT,
            video_url TEXT
        )
        ''')
        conn.commit()

def get_anime_list():
    """Returns the list of all animes"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, genre, image FROM anime')
        return cursor.fetchall()

def get_anime_by_id(anime_id):
    """Returns details of a specific anime by ID"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM anime WHERE id = ?', (anime_id,))
        return cursor.fetchone()
