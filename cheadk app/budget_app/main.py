import tkinter as tk
from tkinter import ttk
from auth import AuthManager
from ui.components import LoginForm
from database import Database
from utils.currency import CurrencyConverter
from ttkthemes import ThemedTk

class BudgetApp(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("Budget Manager Pro")
        self.geometry("1200x800")
        self.auth_manager = AuthManager()
        self.currency_converter = CurrencyConverter()
        self.load_styles()
        self.show_login()

    def load_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.apply_theme('light')

    def apply_theme(self, theme_name):
        with open(f'styles/{theme_name}.css', 'r') as f:
            css = f.read()
        self.style.theme_create(theme_name, parent='clam', settings=css)
        self.style.theme_use(theme_name)

    def show_login(self):
        self.login_frame = LoginForm(self, self.auth_manager)
        self.login_frame.pack(expand=True)

    def show_main_app(self):
        self.login_frame.destroy()
        # Initialize main application components here

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()