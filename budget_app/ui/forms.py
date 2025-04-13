import os
import sys

# Add the parent directory to the Python path to resolve the 'controllers' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from controllers.manager import BudgetManager
from tkinter import messagebox

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
        self.fields = [
            ("Type:", ttk.Combobox(form_frame, values=['income', 'expense'])),
            ("Amount:", ttk.Entry(form_frame)),
            ("Category:", ttk.Combobox(form_frame, values=['Food', 'Rent', 'Salary', 'Entertainment'])),
            ("Date:", DateEntry(form_frame, date_pattern='yyyy-mm-dd')),
            ("Description:", ttk.Entry(form_frame))
        ]
        
        for i, (label, widget) in enumerate(self.fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            widget.grid(row=i, column=1, padx=5, pady=5)
        
        # Action Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Search", command=self.search_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var).pack(padx=10, pady=5)

        # Search Box
        search_frame = ttk.LabelFrame(self, text="Search Income/Expense")
        search_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        search_btn = ttk.Button(search_frame, text="Search", command=self.search_entries)
        search_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Results Treeview
        self.results_tree = ttk.Treeview(self, columns=("id", "type", "amount", "category", "date", "description"), show="headings")
        self.results_tree.heading("id", text="ID")
        self.results_tree.heading("type", text="Type")
        self.results_tree.heading("amount", text="Amount")
        self.results_tree.heading("category", text="Category")
        self.results_tree.heading("date", text="Date")
        self.results_tree.heading("description", text="Description")
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Action Buttons
        action_frame = ttk.Frame(self)
        action_frame.pack(padx=10, pady=10, fill='x')

        ttk.Button(action_frame, text="Update", command=self.update_selected_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete", command=self.delete_selected_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Generate Report", command=self.generate_report).pack(side=tk.LEFT, padx=5)

    def save_entry(self):
        try:
            entry_type = self.fields[0][1].get()
            amount = float(self.fields[1][1].get())
            category = self.fields[2][1].get()
            date = self.fields[3][1].get()
            description = self.fields[4][1].get()

            self.manager.add_entry(entry_type, amount, category, date, description)
            self.status_var.set("Entry saved successfully!")
            self.update_results_tree()
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def update_entry(self):
        try:
            selected_item = self.results_tree.selection()
            if not selected_item:
                raise ValueError("No entry selected for update.")

            entry_id = self.results_tree.item(selected_item, 'values')[0]
            entry_type = self.fields[0][1].get()
            amount = float(self.fields[1][1].get())
            category = self.fields[2][1].get()
            date = self.fields[3][1].get()
            description = self.fields[4][1].get()

            self.manager.update_entry(entry_id, type=entry_type, amount=amount, category=category, date=date, description=description)
            self.status_var.set("Entry updated successfully!")
            self.update_results_tree()
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def delete_entry(self):
        try:
            selected_item = self.results_tree.selection()
            if not selected_item:
                raise ValueError("No entry selected for deletion.")

            entry_id = self.results_tree.item(selected_item, 'values')[0]
            self.manager.delete_entry_by_id(entry_id)
            self.status_var.set("Entry deleted successfully!")
            self.update_results_tree()
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def search_entries(self):
        query = self.search_var.get().strip().lower()
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        if not query:
            messagebox.showerror("Error", "Search query cannot be empty.")
            return

        all_entries = self.manager.get_all_entries()
        filtered_entries = [
            entry for entry in all_entries
            if query in str(entry.id).lower()
            or query in entry.type.lower()
            or query in str(entry.amount).lower()
            or query in str(entry.category).lower()
            or query in entry.date.lower()
        ]

        if not filtered_entries:
            messagebox.showinfo("No Results", "No matching entries found.")
            return

        for entry in filtered_entries:
            self.results_tree.insert('', 'end', values=(
                entry.id, entry.type, entry.amount, entry.category, entry.date, entry.description
            ))

    def update_results_tree(self):
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        all_entries = self.manager.get_all_entries()
        for entry in all_entries:
            self.results_tree.insert('', 'end', values=(
                entry.id, entry.type, entry.amount, entry.category, entry.date, entry.description
            ))

    def clear_form(self):
        # Clear all form fields
        for child in self.winfo_children():
            if isinstance(child, ttk.Entry) or isinstance(child, DateEntry):
                child.delete(0, tk.END)

    def update_selected_entry(self):
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No entry selected for update.")
            return
        # Logic to update the selected entry
        pass

    def delete_selected_entry(self):
        selected_item = self.results_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No entry selected for deletion.")
            return
        # Logic to delete the selected entry
        pass

    def generate_report(self):
        try:
            # Fetch all entries from the results tree
            entries = []
            for row in self.results_tree.get_children():
                entries.append(self.results_tree.item(row, 'values'))

            if not entries:
                messagebox.showinfo("No Data", "No entries available to generate a report.")
                return

            # Create a report file
            report_file = "report.txt"
            with open(report_file, "w") as file:
                file.write("Budget Report\n")
                file.write("=" * 50 + "\n")
                file.write(f"{'ID':<5}{'Type':<10}{'Amount':<10}{'Category':<15}{'Date':<15}{'Description':<20}\n")
                file.write("-" * 50 + "\n")

                for entry in entries:
                    file.write(f"{entry[0]:<5}{entry[1]:<10}{entry[2]:<10}{entry[3]:<15}{entry[4]:<15}{entry[5]:<20}\n")

            messagebox.showinfo("Success", f"Report generated successfully and saved as {report_file}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")