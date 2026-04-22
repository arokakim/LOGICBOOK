import sqlite3

class DatabaseManager:
    def __init__(self, db_name="logic_vault.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # We added 'pseudo_code TEXT' to the middle of this command
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                umbrella TEXT,
                title TEXT,
                pseudo_code TEXT,
                code_block TEXT,
                category TEXT
            )
        ''')
        self.conn.commit()

    # We added 'pseudo' to the arguments and the SQL query
    def add_snippet(self, umbrella, title, pseudo, code):
        query = "INSERT INTO snippets (umbrella, title, pseudo_code, code_block) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (umbrella, title, pseudo, code))
        self.conn.commit()