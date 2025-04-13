import tkinter as tk
from ui.navigation import Navigation
from django.conf import settings
from tkinter import ttk
from controllers.manager import BudgetManager

class BudgetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Budget Manager Pro")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Apply custom styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', rowheight=25)
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), padding=5)
        
        self.navigation = Navigation(self.root)
        self.navigation.pack(fill=tk.BOTH, expand=True)

        # Populate random data for testing
        manager = BudgetManager()
        manager.populate_random_data()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BudgetApp()
    app.run()