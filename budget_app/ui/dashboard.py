import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# Add the parent directory to the Python path to resolve the 'controllers' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.manager import BudgetManager

class Dashboard(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.manager = BudgetManager()
        self.create_widgets()

    def create_widgets(self):
        # Balance Section
        balance_frame = ttk.LabelFrame(self, text="Current Balance")
        balance_frame.pack(padx=10, pady=10, fill='x')
        
        self.balance_label = ttk.Label(balance_frame, text="₹0.00", font=('Arial', 24))
        self.balance_label.pack(padx=20, pady=20)
        
        # Monthly Summary Chart
        chart_frame = ttk.LabelFrame(self, text="Monthly Summary")
        chart_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Category Breakdown
        category_frame = ttk.LabelFrame(self, text="Category Breakdown")
        category_frame.pack(padx=10, pady=10, fill='x')
        
        self.category_tree = ttk.Treeview(category_frame, columns=('category', 'total'), show='headings')
        self.category_tree.heading('category', text='Category')
        self.category_tree.heading('total', text='Total')
        self.category_tree.pack(fill='both', expand=True)
        
        self.update_content()

    def update_content(self):
        # Update balance
        balance = self.manager.calculate_balance()
        self.balance_label.config(text=f"₹{balance:,.2f}")
        
        # Update monthly chart
        monthly_data = self.manager.get_monthly_summary()
        self.ax.clear()
        if monthly_data:
            try:
                months = [f"{int(m):02d}/{y}" for y, m, i, e in monthly_data]
                income = [i for y, m, i, e in monthly_data]
                expense = [e for y, m, i, e in monthly_data]

                self.ax.bar(months, income, label='Income')
                self.ax.bar(months, [-e for e in expense], label='Expense')
                self.ax.legend()
            except ValueError as e:
                print(f"Error processing monthly data: {e}")
        self.canvas.draw()
        
        # Update category breakdown
        categories = self.manager.get_category_breakdown()
        for row in self.category_tree.get_children():
            self.category_tree.delete(row)
        for category, total in categories.items():
            self.category_tree.insert('', 'end', values=(category, f"₹{total:,.2f}"))