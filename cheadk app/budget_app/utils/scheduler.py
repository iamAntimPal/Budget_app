import schedule
import time
from datetime import datetime
from database import Database

class TransactionScheduler:
    def __init__(self):
        self.db = Database()
        self.schedule_jobs()

    def schedule_jobs(self):
        schedule.every().day.at("00:00").do(self.process_recurring)

    def process_recurring(self):
        today = datetime.now().date()
        recurring = self.db.conn.execute('''
            SELECT * FROM recurring 
            WHERE (last_occurrence IS NULL OR last_occurrence < ?)
            AND start_date <= ?
            AND (end_date IS NULL OR end_date >= ?)
        ''', (today, today, today)).fetchall()

        for transaction in recurring:
            self.create_entry(transaction)
            self.update_last_occurrence(transaction[0], today)

    def create_entry(self, transaction):
        self.db.add_entry(
            user_id=transaction[1],
            type=transaction[2],
            amount=transaction[3],
            currency=transaction[4],
            category=transaction[5],
            date=datetime.now().strftime('%Y-%m-%d')
        )

    def update_last_occurrence(self, transaction_id, date):
        self.db.conn.execute('''
            UPDATE recurring SET last_occurrence = ? WHERE id = ?
        ''', (date, transaction_id))
        self.db.conn.commit()