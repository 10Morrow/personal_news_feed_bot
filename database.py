import sqlite3

DB_NAME = "data_base.db"


def subscribe_user_to_channel(user_id, channel_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET channel_id = ? WHERE id = ?", (channel_id, user_id))

    conn.commit()
    conn.close()


def get_entries_by_user_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT text, mark FROM entries WHERE user_id = ?", (user_id,))
    results = cursor.fetchall()

    conn.close()

    entries = []
    for result in results:
        text, mark = result
        entries.append((text, mark))

    return entries


def add_entry(user_id, text, mark=0):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO entries (user_id, text, mark) VALUES (?, ?, ?)",
                   (user_id, text, mark))

    entry_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return entry_id


def update_entry_status(entry_id, mark):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("UPDATE entries SET mark = ? WHERE id = ?", (mark, entry_id))

    conn.commit()
    conn.close()


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    channel_id INTEGER,
                    FOREIGN KEY (channel_id) REFERENCES channels(id)
                )
            """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text TEXT,
                    mark INTEGER
                )
            """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
