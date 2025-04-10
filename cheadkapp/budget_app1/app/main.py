import tkinter as tk
from tkinter import ttk
from app.auth import AuthManager
from app.manager import BudgetManager
from ui.login import LoginForm
from ui.dashboard import Dashboard

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Manager Pro")
        self.geometry("1200x800")
        self.auth_manager = AuthManager()
        self.budget_manager = BudgetManager()
        self.show_login()

    def show_login(self):
        self.login_frame = LoginForm(self, self.auth_manager)
        self.login_frame.pack(expand=True)

    def show_main(self):
        self.login_frame.destroy()
        self.dashboard = Dashboard(self, self.budget_manager)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()