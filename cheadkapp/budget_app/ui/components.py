# ui/components.py

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.currency import CurrencyConverter
from auth import AuthManager

class BaseFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager
        self.currency_converter = CurrencyConverter()
        self.style = ttk.Style()
        
    def apply_theme(self, theme):
        self.style.theme_use(theme)
        
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
    def show_status(self, message, error=False):
        color = 'red' if error else 'green'
        self.status_label.config(foreground=color)
        self.status_var.set(message)
        
class EntryForm(BaseFrame):
    def __init__(self, parent, manager):
        super().__init__(parent, manager)
        self.create_widgets()

    def create_widgets(self):
        # Form Fields
        self.fields = {
            'type': ttk.Combobox(self, values=['income', 'expense']),
            'amount': ttk.Entry(self),
            'currency': ttk.Combobox(self, values=self.currency_converter.get_currencies()),
            'category': ttk.Combobox(self, values=['Food', 'Rent', 'Salary', 'Entertainment']),
            'date': DateEntry(self, date_pattern='yyyy-mm-dd'),
            'description': ttk.Entry(self)
        }
        
        # Layout
        for i, (label, widget) in enumerate(self.fields.items()):
            ttk.Label(self, text=label.capitalize()).grid(row=i, column=0, padx=5, pady=5)
            widget.grid(row=i, column=1, padx=5, pady=5)
            
        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Save", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        self.create_status_bar()

    def save_entry(self):
        try:
            data = {k: v.get() for k, v in self.fields.items()}
            # Add validation and conversion logic
            self.manager.add_entry(**data)
            self.show_status("Entry saved successfully!")
        except Exception as e:
            self.show_status(f"Error: {str(e)}", error=True)
            
    def clear_form(self):
        for widget in self.fields.values():
            widget.delete(0, tk.END)

class NavBar(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        ttk.Button(self, text="Dashboard", command=lambda: self.controller.show_frame('Dashboard')).pack(fill=tk.X, pady=2)
        ttk.Button(self, text="Add Entry", command=lambda: self.controller.show_frame('EntryForm')).pack(fill=tk.X, pady=2)
        ttk.Button(self, text="Reports", command=lambda: self.controller.show_frame('Reports')).pack(fill=tk.X, pady=2)
        ttk.Button(self, text="Logout", command=self.logout).pack(fill=tk.X, pady=2)

    def logout(self):
        AuthManager().current_user = None
        self.controller.show_login()

class ReportChart(ttk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.data = data
        self.create_chart()

    def create_chart(self):
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        categories = self.data.keys()
        amounts = self.data.values()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%')
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class CurrencyDisplay(ttk.Frame):
    def __init__(self, parent, amount, currency):
        super().__init__(parent)
        self.amount = amount
        self.currency = currency
        self.converter = CurrencyConverter()
        self.create_widgets()

    def create_widgets(self):
        self.display_var = tk.StringVar()
        ttk.Label(self, textvariable=self.display_var, font=('Arial', 14)).pack()
        self.update_display()

    def update_display(self):
        converted = self.converter.convert(self.amount, self.currency, 'USD')
        self.display_var.set(f"{self.amount:.2f} {self.currency} ≈ {converted:.2f} USD")
        
class ResponsiveMixin:
    def configure_responsive(self):
        self.bind("<Configure>", self.on_resize)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_resize(self, event):
        width = event.width
        if width < 600:
            self.style.configure('TLabel', font=('Arial', 10))
        else:
            self.style.configure('TLabel', font=('Arial', 12))