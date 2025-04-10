import tkinter as tk
from tkinter import ttk
from models.entry import BudgetEntry

class Dashboard(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create UI elements
        header = ttk.Label(self, text="Budget Dashboard", font=("Helvetica", 16))
        header.pack(pady=10)

        # Example: Listbox for displaying entries
        self.entries_list = tk.Listbox(self, width=80, height=15)
        self.entries_list.pack(pady=10)

        # Button to refresh entries
        refresh_button = ttk.Button(self, text="Refresh", command=self.refresh_entries)
        refresh_button.pack()

        # Button to add a dummy entry (for demonstration purposes)
        add_button = ttk.Button(self, text="Add Example Entry", command=self.add_example_entry)
        add_button.pack(pady=5)

    def refresh_entries(self):
        '''Fetch entries from the database and display them.'''
        self.entries_list.delete(0, tk.END)
        entries = self.controller.db_handler.get_entries()
        for entry in entries:
            display_text = f"{entry[1]} | {entry[2]} | ${entry[3]} | {entry[5]}"
            self.entries_list.insert(tk.END, display_text)

    def add_example_entry(self):
        '''Add a sample budget entry for testing.'''
        from datetime import datetime
        entry_data = ("expense", "Food", 15.99, "Lunch", datetime.now().strftime("%Y-%m-%d"))
        self.controller.db_handler.add_entry(entry_data)
        self.refresh_entries()
