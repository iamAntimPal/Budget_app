from data.database import Database
from data.models import Entry, RecurringTransaction
from utils.currency import CurrencyConverter
from utils.scheduler import TransactionScheduler

class BudgetManager:
    def __init__(self):
        self.db = Database()
        self.scheduler = TransactionScheduler()
        self.currency_converter = CurrencyConverter()

    def add_entry(self, entry_data):
        # Add entry with validation and currency conversion
        converted_amount = self.currency_converter.convert(
            entry_data['amount'],
            entry_data['currency'],
            'USD'
        )
        self.db.conn.execute('''
            INSERT INTO entries 
            (user_id, type, amount, currency, category, date, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            entry_data['user_id'],
            entry_data['type'],
            converted_amount,
            entry_data['currency'],
            entry_data['category'],
            entry_data['date'],
            entry_data.get('description')
        ))
        self.db.conn.commit()

    def get_balance(self, user_id):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) -
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END)
            FROM entries
            WHERE user_id = ?
        ''', (user_id,))
        return cursor.fetchone()[0] or 0

    # Add other CRUD operations and business logic here