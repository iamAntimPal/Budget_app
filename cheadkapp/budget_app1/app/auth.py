import bcrypt
from data.database import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
        self.current_user = None

    def register(self, username, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.db.conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                           (username, hashed))
        self.db.conn.commit()

    def login(self, username, password):
        user = self.db.conn.execute('SELECT * FROM users WHERE username = ?', 
                                   (username,)).fetchone()
        if user and bcrypt.checkpw(password.encode(), user[2]):
            self.current_user = user
            return True
        return False

    def get_user_currency(self):
        return self.current_user[3] if self.current_user else 'USD'