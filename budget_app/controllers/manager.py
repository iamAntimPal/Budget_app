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