import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controllers.manager import BudgetManager

class Reports(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.manager = BudgetManager()
        self.create_widgets()

    def create_widgets(self):
        # Date Range Selector
        date_frame = ttk.Frame(self)
        date_frame.pack(padx=10, pady=10, fill='x')
        
        ttk.Label(date_frame, text="From:").pack(side=tk.LEFT)
        self.start_date = DateEntry(date_frame, date_pattern='yyyy-mm-dd')
        self.start_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(date_frame, text="To:").pack(side=tk.LEFT)
        self.end_date = DateEntry(date_frame, date_pattern='yyyy-mm-dd')
        self.end_date.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(date_frame, text="Generate Report", command=self.generate_report).pack(side=tk.LEFT, padx=10)
        
        # Report Content
        self.report_frame = ttk.Frame(self)
        self.report_frame.pack(fill=tk.BOTH, expand=True)
        
        # Chart
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.report_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Data Table
        self.tree = ttk.Treeview(self.report_frame, columns=('date', 'type', 'amount', 'category'), show='headings')
        self.tree.heading('date', text='Date')
        self.tree.heading('type', text='Type')
        self.tree.heading('amount', text='Amount')
        self.tree.heading('category', text='Category')
        self.tree.pack(fill=tk.BOTH, expand=True)

    def generate_report(self):
        start = self.start_date.get()
        end = self.end_date.get()
        entries = self.manager.get_entries(start, end)
        
        # Update chart
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        categories = {}
        for entry in entries:
            categories[entry.category] = categories.get(entry.category, 0) + entry.amount
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        self.canvas.draw()
        
        # Update table
        for row in self.tree.get_children():
            self.tree.delete(row)
        for entry in entries:
            self.tree.insert('', 'end', values=(entry.date, entry.type, f"₹{entry.amount:,.2f}", entry.category))