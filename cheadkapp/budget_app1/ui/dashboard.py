from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utils.currency import CurrencyConverter

class Dashboard(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)
        self.manager = manager
        self.currency_converter = CurrencyConverter()
        self.create_widgets()

    def create_widgets(self):
        # Balance display
        balance_frame = ttk.LabelFrame(self, text="Current Balance")
        balance_frame.pack(padx=10, pady=10, fill='x')
        
        self.balance_label = ttk.Label(balance_frame, text="₹0.00", font=('Arial', 24))
        self.balance_label.pack(padx=20, pady=20)
        
        # Monthly summary chart
        chart_frame = ttk.LabelFrame(self, text="Monthly Summary")
        chart_frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Category breakdown
        category_frame = ttk.LabelFrame(self, text="Category Breakdown")
        category_frame.pack(padx=10, pady=10, fill='x')
        
        self.category_tree = ttk.Treeview(category_frame, columns=('category', 'total'))
        self.category_tree.heading('category', text='Category')
        self.category_tree.heading('total', text='Total')
        self.category_tree.pack(fill='both', expand=True)
        
        self.update_content()

    def update_content(self):
        # Update balance display
        balance = self.manager.get_balance()
        converted = self.currency_converter.convert(balance, 'USD', 'INR')
        self.balance_label.config(text=f"₹{converted:,.2f}")
        
        # Update charts and tables
        # (Add data visualization implementation here)