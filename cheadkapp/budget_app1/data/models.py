from dataclasses import dataclass
from datetime import datetime

@dataclass
class Entry:
    id: int
    user_id: int
    type: str
    amount: float
    currency: str
    category: str
    date: str
    description: str = None

@dataclass
class RecurringTransaction:
    id: int
    user_id: int
    type: str
    amount: float
    currency: str
    category: str
    frequency: str
    start_date: str
    end_date: str = None
    last_occurrence: str = None