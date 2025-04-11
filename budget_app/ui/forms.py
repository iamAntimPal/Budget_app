import os
import sys

# Add the parent directory to the Python path to resolve the 'controllers' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from controllers.manager import BudgetManager

class EntryForm(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.manager = BudgetManager()
        self.create_widgets()

    def create_widgets(self):
        # Form Frame
        form_frame = ttk.LabelFrame(self, text="Add/Edit Entry")
        form_frame.pack(padx=10, pady=10, fill='x')
        
        # Form Fields
        fields = [
            ("Type:", ttk.Combobox(form_frame, values=['income', 'expense'])),
            ("Amount:", ttk.Entry(form_frame)),
            ("Category:", ttk.Combobox(form_frame, values=['Food', 'Rent', 'Salary', 'Entertainment'])),
            ("Date:", DateEntry(form_frame, date_pattern='yyyy-mm-dd')),
            ("Description:", ttk.Entry(form_frame))
        ]
        
        for i, (label, widget) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            widget.grid(row=i, column=1, padx=5, pady=5)
        
        # Action Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var).pack(padx=10, pady=5)

    def save_entry(self):
        try:
            # Validation and submission logic
            self.status_var.set("Entry saved successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def update_entry(self):
        try:
            # Logic to update an existing entry
            self.status_var.set("Entry updated successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def delete_entry(self):
        try:
            # Logic to delete an entry
            self.status_var.set("Entry deleted successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def search_entry(self):
        try:
            # Logic to search for entries by date, income, or expense
            self.status_var.set("Search completed!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def clear_form(self):
        # Clear all form fields
        for child in self.winfo_children():
            if isinstance(child, ttk.Entry) or isinstance(child, DateEntry):
                child.delete(0, tk.END)