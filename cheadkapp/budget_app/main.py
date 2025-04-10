import tkinter as tk
from tkinter import ttk
from auth import AuthManager
from database import Database
from utils.currency import CurrencyConverter
from ttkthemes import ThemedTk
from ui.components import NavBar, EntryForm, ReportChart, BaseFrame

class Dashboard(BaseFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        self.navbar = NavBar(self, manager)
        self.entry_form = EntryForm(self, manager)
        self.report_chart = ReportChart(self, manager)

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
        self.style.theme_use("clam")
        self.apply_theme("light")

    def apply_theme(self, theme_name):
        theme_settings = {
            ".": {
                "configure": {
                    "background": "#ffffff",
                    "foreground": "#000000",
                    "font": ("Arial", 10)
                }
            },
            "TButton": {
                "configure": {
                    "padding": 5,
                    "relief": "flat",
                    "background": "#0078d7",
                    "foreground": "#ffffff"
                },
                "map": {
                    "background": [("active", "#005a9e"), ("disabled", "#d3d3d3")],
                    "foreground": [("disabled", "#a9a9a9")]
                }
            }
        }
        self.style.theme_create(theme_name, parent="clam", settings=theme_settings)
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