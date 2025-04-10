class BudgetEntry:
    def __init__(self, entry_type, category, amount, description, date):
        self.entry_type = entry_type  # e.g., 'expense' or 'income'
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date

    def to_tuple(self):
        return (self.entry_type, self.category, self.amount, self.description, self.date)
