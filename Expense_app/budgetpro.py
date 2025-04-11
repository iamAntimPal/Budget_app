import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib
import os
from datetime import datetime

# Configuration
CSV_DIR = "data"
TRANSACTIONS_FILE = os.path.join(CSV_DIR, "transactions.csv")
BUDGETS_FILE = os.path.join(CSV_DIR, "budgets.csv")
USERS_FILE = os.path.join(CSV_DIR, "users.csv")

class BudgetProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgetPro")
        self.style = ttk.Style("cosmo")
        
        # Initialize data
        self.create_data_directory()
        self.load_data()
        
        # UI Setup
        self.create_header()
        self.create_sidebar()
        self.create_action_bar()
        self.create_content_frame()  # Ensure content_frame is created before check_first_run
        
        # Check first run
        self.check_first_run()
        
        # Show login screen
        #self.show_login()
    def create_data_directory(self):
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)
            
    def load_data(self):
        # Load transactions
        if os.path.exists(TRANSACTIONS_FILE):
            self.transactions = pd.read_csv(TRANSACTIONS_FILE)
        else:
            self.transactions = pd.DataFrame(columns=[
                'date', 'category', 'type', 'amount', 'description'
            ])
            
        # Load budgets
        if os.path.exists(BUDGETS_FILE):
            self.budgets = pd.read_csv(BUDGETS_FILE)
        else:
            self.budgets = pd.DataFrame(columns=['category', 'monthly_limit'])
            
        # Load users
        if os.path.exists(USERS_FILE):
            self.users = pd.read_csv(USERS_FILE)
        else:
            self.users = pd.DataFrame(columns=['username', 'password_hash'])

    def check_first_run(self):
        if self.users.empty:
            self.show_initial_setup()

    def create_header(self):
        header = ttk.Frame(self.root)
        header.pack(fill=X)
        
        # Title
        title = ttk.Label(header, text="BudgetPro", font=("Helvetica", 20, "bold"))
        title.pack(side=LEFT, padx=20, pady=10)
        
        # Logout button
        self.logout_btn = ttk.Button(header, text="Logout", command=self.confirm_logout)
        self.logout_btn.pack(side=RIGHT, padx=20, pady=10)

    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, width=250)
        sidebar.pack(side=LEFT, fill=Y)
        
        # Main Menu
        main_menu_btn = ttk.Button(sidebar, text="Main Menu", command=self.show_main_menu)
        main_menu_btn.pack(fill=X, padx=10, pady=5)

        # Dashboard Menu
        menu_items = ["Dashboard", "Analysis", "Income", "Expense", "Budget Planner"]
        for item in menu_items:
            btn = ttk.Button(sidebar, text=item, command=lambda i=item: self.show_page(i))
            btn.pack(fill=X, padx=10, pady=5)
            
        # Theme toggle
        theme_frame = ttk.Frame(sidebar)
        theme_frame.pack(pady=20)
        self.theme_var = tk.StringVar(value="cosmo")
        light_btn = ttk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, 
                                  value="cosmo", command=self.change_theme)
        dark_btn = ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, 
                                 value="cyborg", command=self.change_theme)
        light_btn.pack(side=LEFT)
        dark_btn.pack(side=LEFT)

    def create_action_bar(self):
        action_bar = ttk.Frame(self.root)
        action_bar.pack(fill=X, padx=20, pady=10)
        
        # Search bar
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(action_bar, textvariable=self.search_var)
        search_entry.pack(side=LEFT, padx=5)

        # Add search icon button
        search_icon = ttk.Button(action_bar, text="🔍", command=self.perform_search)
        search_icon.pack(side=LEFT, padx=5)
        
        # Month/Year selector
        months = [f"{i:02d}" for i in range(1,13)]
        years = [str(y) for y in range(2020, 2031)]
        
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        month_menu = ttk.Combobox(action_bar, textvariable=self.month_var, values=months, width=5)
        year_menu = ttk.Combobox(action_bar, textvariable=self.year_var, values=years, width=5)
        month_menu.pack(side=LEFT, padx=5)
        year_menu.pack(side=LEFT, padx=5)
        
        # Delete button
        delete_btn = ttk.Button(action_bar, text="Delete", bootstyle=DANGER, command=self.delete_entry)
        delete_btn.pack(side=RIGHT)

    def create_content_frame(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def show_login(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=50)
        
        ttk.Label(frame, text="Password:").grid(row=0, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=0, column=1, padx=5, pady=5)
        
        login_btn = ttk.Button(frame, text="Login", command=self.verify_password)
        login_btn.grid(row=1, column=0, columnspan=2, pady=10)

    def verify_password(self):
        entered_pass = self.password_entry.get()
        if not self.users.empty:
            stored_hash = self.users.iloc[0]['password_hash']
            if hashlib.sha256(entered_pass.encode()).hexdigest() == stored_hash:
                self.show_dashboard()
                return
        messagebox.showerror("Error", "Invalid password")

    def show_initial_setup(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=50)
        
        ttk.Label(frame, text="Set New Password:").grid(row=0, column=0, padx=5, pady=5)
        self.new_pass = ttk.Entry(frame, show="*")
        self.new_pass.grid(row=0, column=1, padx=5, pady=5)
        
        confirm_btn = ttk.Button(frame, text="Confirm", command=self.save_new_password)
        confirm_btn.grid(row=1, column=0, columnspan=2, pady=10)

    def save_new_password(self):
        new_pass = self.new_pass.get()
        hashed = hashlib.sha256(new_pass.encode()).hexdigest()
        self.users = pd.DataFrame([{"username": "admin", "password_hash": hashed}])
        self.users.to_csv(USERS_FILE, index=False)
        messagebox.showinfo("Success", "Password set successfully")
        self.show_login()

    def show_page(self, page):
        self.clear_content()
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Analysis":
            self.show_analysis()
        # Add other pages similarly

    def show_dashboard(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=BOTH, expand=True)
        
        # Total Balance
        total_income = self.transactions[self.transactions['type']=='Income']['amount'].sum()
        total_expense = self.transactions[self.transactions['type']=='Expense']['amount'].sum()
        balance = total_income - total_expense
        
        balance_frame = ttk.LabelFrame(frame, text="Total Balance", bootstyle=SUCCESS)
        balance_frame.pack(pady=20, fill=X)
        ttk.Label(balance_frame, text=f"${balance:.2f}", font=("Helvetica", 24)).pack(padx=20, pady=20)
        
        # Charts
        fig = plt.Figure(figsize=(10, 4))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Monthly trend
        monthly = self.transactions.groupby(self.transactions['date'].str[:7]).sum(numeric_only=True)
        monthly['amount'].plot(ax=ax1, title="Monthly Trend")
        
        # Category distribution
        categories = self.transactions.groupby('category')['amount'].sum()
        categories.plot.pie(ax=ax2, title="Category Distribution")
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def show_analysis(self):
        # Similar implementation to dashboard with different charts
        pass

    def confirm_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.show_login()

    def change_theme(self):
        self.style.theme_use(self.theme_var.get())

    def delete_entry(self):
        # Implement delete functionality
        pass

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def save_data(self):
        self.transactions.to_csv(TRANSACTIONS_FILE, index=False)
        self.budgets.to_csv(BUDGETS_FILE, index=False)

    def perform_search(self):
        # Implement search functionality
        pass

    def show_main_menu(self):
        # Implement main menu functionality
        pass

if __name__ == "__main__":
    root = ttk.Window()
    app = BudgetProApp(root)
    root.mainloop()