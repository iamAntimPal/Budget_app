import tkinter as tk
from ui.navigation import Navigation
from django.conf import settings
import ttk.style as ttk
from controllers.manager import BudgetManager
class BudgetApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Budget Manager Pro")
        self.root.geometry("1200x800")
        self.roo# The line `self.root.minsize(800, 600)` in the `BudgetApp` class is setting the
        # minimum size that the root window can be resized to. In this case, it is setting the
        # minimum width to 800 pixels and the minimum height to 600 pixels. This means that
        # the user will not be able to resize the window to be smaller than these dimensions.
        t.minsize(800, 600)
        
        # Apply custom styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', rowheight=25)
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12), padding=5)
        
        self.navigation = Navigation(self.root)
        self.navigation.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BudgetApp()
    app.run()