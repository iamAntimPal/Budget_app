import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from controllers.manager import BudgetManager

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.manager = BudgetManager()
        self.create_widgets()

    def create_widgets(self):
        # Balance Frame
        balance_frame = ttk.LabelFrame(self.root, text="Current Balance")
        balance_frame.pack(padx=10, pady=10, fill='x')
        
        self.balance_label = ttk.Label(balance_frame, text="₹0.00", font=('Arial', 24))
        self.balance_label.pack(padx=20, pady=20)
        
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Add Entry")
        input_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(input_frame, text="Type:").grid(row=0, column=0)
        self.type_var = tk.StringVar(value='income')
        ttk.Radiobutton(input_frame, text="Income", variable=self.type_var, value='income').grid(row=0, column=1)
        ttk.Radiobutton(input_frame, text="Expense", variable=self.type_var, value='expense').grid(row=0, column=2)
        
        ttk.Label(input_frame, text="Amount:").grid(row=1, column=0)
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, columnspan=2)
        
        ttk.Label(input_frame, text="Category:").grid(row=2, column=0)
        self.category_entry = ttk.Combobox(input_frame, values=["Food", "Rent", "Salary", "Entertainment"])
        self.category_entry.grid(row=2, column=1, columnspan=2)
        
        ttk.Label(input_frame, text="Date:").grid(row=3, column=0)
        self.date_entry = DateEntry(input_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=3, column=1, columnspan=2)
        
        ttk.Label(input_frame, text="Description:").grid(row=4, column=0)
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=4, column=1, columnspan=2)
        
        ttk.Button(input_frame, text="Submit", command=self.submit_entry).grid(row=5, column=0, columnspan=3, pady=5)
        
        # Status Bar
        self.status_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.status_var).pack(padx=10, pady=5, anchor='w')
        
        self.update_balance()

    def submit_entry(self):
        try:
            self.manager.add_entry(
                self.type_var.get(),
                float(self.amount_entry.get()),
                self.category_entry.get(),
                self.date_entry.get(),
                self.desc_entry.get()
            )
            self.clear_form()
            self.update_balance()
            self.status_var.set("Entry added successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

    def clear_form(self):
        self.amount_entry.delete(0, 'end')
        self.category_entry.set('')
        self.desc_entry.delete(0, 'end')

    def update_balance(self):
        balance = self.manager.calculate_balance()
        self.balance_label.config(text=f"₹{balance:,.2f}")