import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='budget.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                currency TEXT DEFAULT 'USD'
            )
        ''')
        
        # Entries Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Recurring Transactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recurring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL,
                currency TEXT NOT NULL,
                category TEXT NOT NULL,
                frequency TEXT CHECK(frequency IN ('daily', 'weekly', 'monthly')),
                start_date TEXT NOT NULL,
                end_date TEXT,
                last_occurrence TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        self.conn.commit()