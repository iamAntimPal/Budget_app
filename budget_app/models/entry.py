from dataclasses import dataclass
from datetime import datetime
from .category import CATEGORIES

@dataclass
class Entry:
    id: int
    type: str
    amount: float
    category: str
    date: str
    description: str = None

    @property
    def date_obj(self):
        return datetime.strptime(self.date, '%Y-%m-%d').date()

    @staticmethod
    def get_categories():
        return [category.name for category in CATEGORIES]