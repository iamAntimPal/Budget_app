import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='budget.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()

    def add_entry(self, entry_type, amount, category, date, description):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO entries (type, amount, category, date, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry_type, amount, category, date, description))
        self.conn.commit()

    def get_entries(self, start_date=None, end_date=None):
        cursor = self.conn.cursor()
        query = 'SELECT * FROM entries'
        if start_date or end_date:
            query += ' WHERE date BETWEEN ? AND ?'
            cursor.execute(query, (start_date, end_date))
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def delete_entry(self, entry_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        self.conn.commit()

    def update_entry(self, entry_id, **kwargs):
        set_clause = ', '.join([f"{k} = ?" for k in kwargs])
        values = list(kwargs.values()) + [entry_id]
        cursor = self.conn.cursor()
        cursor.execute(f'UPDATE entries SET {set_clause} WHERE id = ?', values)
        self.conn.commit()

    def get_balance(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END)
            FROM entries
        ''')
        return cursor.fetchone()[0] or 0

    def get_monthly_summary(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT 
                strftime('%Y', date) as year,
                strftime('%m', date) as month,
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
            FROM entries
            GROUP BY year, month
            ORDER BY year DESC, month DESC
            LIMIT 12
        ''')
        return cursor.fetchall()

    def get_category_breakdown(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM entries 
            GROUP BY category
        ''')
        return dict(cursor.fetchall())