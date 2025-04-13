import os
import sys

# Add the parent directory to the Python path to resolve the 'models' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.entry import Entry
from database.db_handler import Database

class BudgetManager:
    def __init__(self):
        self.db = Database()

    def add_entry(self, entry_type, amount, category, date, description=None):
        if entry_type not in ['income', 'expense']:
            raise ValueError("Type must be 'income' or 'expense'")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.db.add_entry(entry_type, amount, category, date, description)

    def get_all_entries(self):
        raw_entries = self.db.get_entries()
        return [Entry(*entry) for entry in raw_entries]

    def calculate_balance(self):
        return self.db.get_balance()

    def delete_entry_by_id(self, entry_id):
        self.db.delete_entry(entry_id)

    def update_entry(self, entry_id, **kwargs):
        valid_fields = {'type', 'amount', 'category', 'date', 'description'}
        if invalid := set(kwargs.keys()) - valid_fields:
            raise ValueError(f"Invalid fields: {invalid}")
        self.db.update_entry(entry_id, **kwargs)
        
    def get_monthly_summary(self):
        cursor = self.db.conn.cursor()
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
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM entries 
            GROUP BY category
        ''')
        return dict(cursor.fetchall())

    def get_entries(self, start_date=None, end_date=None):
        cursor = self.db.conn.cursor()
        query = "SELECT * FROM entries"
        params = []

        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params.extend([start_date, end_date])

        cursor.execute(query, params)
        return cursor.fetchall()

    def populate_random_data(self):
        import random
        from datetime import datetime, timedelta

        categories = ['Food', 'Rent', 'Salary', 'Entertainment', 'Utilities']
        types = ['income', 'expense']

        for _ in range(50):
            entry_type = random.choice(types)
            amount = round(random.uniform(10, 1000), 2)
            category = random.choice(categories)
            date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            description = f"Random {entry_type} entry"

            self.add_entry(entry_type, amount, category, date, description)

        print("Random data populated successfully.")