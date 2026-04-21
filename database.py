import sqlite3

class DatabaseManager:
    def __init__(self, db_name="logic_vault.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # 1. Table for General Code Snippets (The logic library)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                umbrella TEXT,      -- Web Dev, Game Dev, etc.
                title TEXT,
                code_block TEXT,
                category TEXT       -- Syntax, Logic, Event, etc.
            )
        ''')

        # 2. Table for General Information (The 'Knowledge' base)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS information (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                content TEXT,
                reference_link TEXT
            )
        ''')

        # 3. Table for YOUR Customized Snippets (The 'User Vault')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                custom_code TEXT,
                tags TEXT,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_user_snippet(self, title, code, tags):
        query = "INSERT INTO user_vault (title, custom_code, tags) VALUES (?, ?, ?)"
        self.cursor.execute(query, (title, code, tags))
        self.conn.commit()
        print(f"Success: '{title}' saved to your personal vault!")

    def fetch_all_by_umbrella(self, table, umbrella_name):
        # This helps us filter by "Game Dev" or "Web Dev"
        query = f"SELECT * FROM {table} WHERE umbrella = ?"
        self.cursor.execute(query, (umbrella_name,))
        return self.cursor.fetchall()

# Small Test Run
if __name__ == "__main__":
    db = DatabaseManager()
    # Test adding a custom snippet
    db.add_user_snippet("Godot Player Movement", "velocity = input_dir * speed", "Godot, Movement")