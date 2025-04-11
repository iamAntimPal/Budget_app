class Category:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category(name='{self.name}')"

# Predefined categories
CATEGORIES = [
    Category("Food"),
    Category("Rent"),
    Category("Salary"),
    Category("Entertainment"),
    Category("Utilities"),
    Category("Transportation"),
    Category("Healthcare"),
    Category("Education"),
    Category("Savings"),
    Category("Miscellaneous")
]