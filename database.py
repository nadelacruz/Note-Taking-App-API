import sqlite3
import threading
from note import Note


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_db_if_not_exists()
        self.lock = threading.Lock()

        # Connect to the database and create a notes table if it doesn't exist
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS notes
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT NOT NULL,
                          content TEXT NOT NULL,
                          summary TEXT NOT NULL)''')
            conn.commit()
            conn.close()

    def create_db_if_not_exists(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT,
                summary TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_note(self, note):
        # Insert a new note into the database
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("INSERT INTO notes (title, content, summary) VALUES (?, ?, ?)",
                      (note.title, note.content, note.summary))
            conn.commit()
            note_id = c.lastrowid
            conn.close()
        return note_id

    def read_all_notes(self):
        # Retrieve all notes from the database
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM notes")
            notes_data = c.fetchall()
            conn.close()
        return [Note(*note_data[0:]) for note_data in notes_data]

    def read_note_by_id(self, note_id):
        # Retrieve a note from the database by ID
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM notes WHERE id=?", (note_id,))
            note_data = c.fetchone()
            conn.close()
        return note_data

    def update_note_by_id(self, note_id, title, content, summary):
        # Update a note in the database by ID
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("UPDATE notes SET title=?, content=?, summary=? WHERE id=?",
                      (title, content, summary, note_id))
            conn.commit()
            conn.close()

    def delete_note_by_id(self, note_id):
        # Delete a note from the database by ID
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("DELETE FROM notes WHERE id=?", (note_id,))
            conn.commit()
            conn.close()

    def search_notes(self, search_term):
        # Search notes in the database by title or content
        with self.lock:
            conn = sqlite3.connect(self.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?",
                      ('%'+search_term+'%', '%'+search_term+'%'))
            notes_data = c.fetchall()
            conn.close()
        return [Note(*note_data[0:]) for note_data in notes_data]