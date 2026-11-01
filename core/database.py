import sqlite3
from pathlib import Path

class Database:
    def __init__(self, db_path):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.setup()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def setup(self):
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    path TEXT UNIQUE NOT NULL
                );

                CREATE TABLE IF NOT EXISTS recent_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE NOT NULL,
                    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tabs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL
                );
            """)

    def add_bookmark(self, name, path):
        with self.connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO bookmarks(name,path) VALUES (?,?)",
                (name, path)
            )

    def get_bookmarks(self):
        with self.connect() as db:
            return db.execute(
                "SELECT name,path FROM bookmarks ORDER BY name"
            ).fetchall()

    def remove_bookmark(self, path):
        with self.connect() as db:
            db.execute("DELETE FROM bookmarks WHERE path=?", (path,))

    def add_recent(self, path):
        with self.connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO recent_files(path,opened_at) "
                "VALUES (?,CURRENT_TIMESTAMP)",
                (path,)
            )

    def get_recent(self, limit=50):
        with self.connect() as db:
            return db.execute(
                "SELECT path,opened_at FROM recent_files "
                "ORDER BY opened_at DESC LIMIT ?",
                (limit,)
            ).fetchall()

    def set_setting(self, key, value):
        with self.connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO settings(key,value) VALUES (?,?)",
                (key, str(value))
            )

    def get_setting(self, key, default=None):
        with self.connect() as db:
            result = db.execute(
                "SELECT value FROM settings WHERE key=?", (key,)
            ).fetchone()
            return result[0] if result else default
