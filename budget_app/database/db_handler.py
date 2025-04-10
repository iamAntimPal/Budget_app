import sqlite3

class DBHandler:
    def __init__(self, db_name="budget.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT,
                    category TEXT,
                    amount REAL,
                    description TEXT,
                    date TEXT
                )
            """)

    def add_entry(self, entry_data):
        query = "INSERT INTO entries (type, category, amount, description, date) VALUES (?, ?, ?, ?, ?)"
        with self.connection:
            self.connection.execute(query, entry_data)

    def get_entries(self):
        query = "SELECT * FROM entries"
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def delete_entry(self, entry_id):
        query = "DELETE FROM entries WHERE id = ?"
        with self.connection:
            self.connection.execute(query, (entry_id,))

    def update_entry(self, entry_id, entry_data):
        query = """
        UPDATE entries SET type = ?, category = ?, amount = ?, description = ?, date = ?
        WHERE id = ?
        """
        with self.connection:
            self.connection.execute(query, entry_data + (entry_id,))
