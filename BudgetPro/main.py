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
        
        # Initialize data directory and data files
        self.create_data_directory()
        self.load_data()
        
        # UI Setup
        self.create_header()
        self.create_sidebar()
        self.create_action_bar()
        self.create_content_frame()  # Content frame must exist before checking first run
        
        # Make the root window and content frame responsive
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        # Bind the resize event to adjust UI dynamically
        self.root.bind("<Configure>", self.on_resize)

        # Check if this is the first run (i.e., if any user exists)
        self.check_first_run()

        # For an existing user, start with the login screen
        self.show_login()

    def create_data_directory(self):
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)

    def load_data(self):
        # Load transactions data; create an empty DataFrame if file does not exist
        if os.path.exists(TRANSACTIONS_FILE):
            self.transactions = pd.read_csv(TRANSACTIONS_FILE)
        else:
            self.transactions = pd.DataFrame(columns=['date', 'category', 'type', 'amount', 'description'])
            
        # Load budgets data
        if os.path.exists(BUDGETS_FILE):
            self.budgets = pd.read_csv(BUDGETS_FILE)
        else:
            self.budgets = pd.DataFrame(columns=['category', 'monthly_limit'])
            
        # Load user data (for login purposes)
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
        
        # Main Menu button
        main_menu_btn = ttk.Button(sidebar, text="Main Menu", command=self.show_main_menu)
        main_menu_btn.pack(fill=X, padx=10, pady=5)

        # Dashboard and other page options
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

        # Search icon button
        search_icon = ttk.Button(action_bar, text="🔍", command=self.perform_search)
        search_icon.pack(side=LEFT, padx=5)
        
        # Month and Year selectors
        months = [f"{i:02d}" for i in range(1, 13)]
        years = [str(y) for y in range(2020, 2031)]
        
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        month_menu = ttk.Combobox(action_bar, textvariable=self.month_var, values=months, width=5)
        year_menu = ttk.Combobox(action_bar, textvariable=self.year_var, values=years, width=5)
        month_menu.pack(side=LEFT, padx=5)
        year_menu.pack(side=LEFT, padx=5)
        
        # Delete button (functionality to be implemented as needed)
        delete_btn = ttk.Button(action_bar, text="Delete", bootstyle=DANGER, command=self.delete_entry)
        delete_btn.pack(side=RIGHT)

    def create_content_frame(self):
        self.content_frame = ttk.Frame(self.root)
        self.content_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    def show_login(self):
        self.clear_content()  # Ensure all previous widgets are cleared
        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=50)

        ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        login_btn = ttk.Button(frame, text="Login", command=self.verify_password)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

        register_btn = ttk.Button(frame, text="Register", command=self.show_register)
        register_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def show_register(self):
        self.clear_content()  # Ensure all previous widgets are cleared
        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=50)

        ttk.Label(frame, text="Email:").grid(row=0, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(frame)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Username:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_username_entry = ttk.Entry(frame)
        self.reg_username_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Password:").grid(row=3, column=0, padx=5, pady=5)
        self.reg_password_entry = ttk.Entry(frame, show="*")
        self.reg_password_entry.grid(row=3, column=1, padx=5, pady=5)

        register_btn = ttk.Button(frame, text="Register", command=self.register_user)
        register_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def register_user(self):
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        username = self.reg_username_entry.get().strip()
        password = self.reg_password_entry.get().strip()

        if not email or not phone or not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        new_user = {"username": username, "password_hash": hashed_password, "email": email, "phone": phone}

        if self.users.empty:
            self.users = pd.DataFrame([new_user])
        else:
            self.users = self.users.append(new_user, ignore_index=True)

        self.users.to_csv(USERS_FILE, index=False)
        messagebox.showinfo("Success", "Registration successful! You can now log in.")
        self.show_login()

    def verify_password(self):
        username = self.username_entry.get().strip()
        entered_pass = self.password_entry.get().strip()

        if not username or not entered_pass:
            messagebox.showerror("Error", "Username and password are required!")
            return

        user = self.users[self.users['username'] == username]
        if not user.empty:
            stored_hash = user.iloc[0]['password_hash']
            if hashlib.sha256(entered_pass.encode()).hexdigest() == stored_hash:
                self.show_dashboard()
                return

        messagebox.showerror("Error", "Invalid username or password")

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
        if (page == "Dashboard"):
            self.show_dashboard()
        elif (page == "Analysis"):
            self.show_analysis()
        elif (page == "Income"):
            self.show_income()
        elif (page == "Expense"):
            self.show_expense()
        elif (page == "Budget Planner"):
            self.show_budget_planner()

    def show_dashboard(self):
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=BOTH, expand=True)
        
        # Calculate balance (Income - Expense)
        total_income = self.transactions[self.transactions['type'] == 'Income']['amount'].sum()
        total_expense = self.transactions[self.transactions['type'] == 'Expense']['amount'].sum()
        balance = total_income - total_expense
        
        balance_frame = ttk.LabelFrame(frame, text="Total Balance", bootstyle=SUCCESS)
        balance_frame.pack(pady=20, fill=X)
        ttk.Label(balance_frame, text=f"${balance:.2f}", font=("Helvetica", 24)).pack(padx=20, pady=20)
        
        # Create sample charts using matplotlib
        fig = plt.Figure(figsize=(10, 4))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        
        # Monthly trend of amounts
        if not self.transactions.empty:
            self.transactions['year_month'] = self.transactions['date'].str[:7]
            monthly = self.transactions.groupby('year_month').sum(numeric_only=True)
            if "amount" in monthly.columns:
                monthly['amount'].plot(ax=ax1, title="Monthly Trend")
            
            # Category distribution as a pie chart
            if not self.transactions.groupby('category').sum().empty:
                categories = self.transactions.groupby('category')['amount'].sum()
                categories.plot.pie(ax=ax2, title="Category Distribution", autopct="%.1f%%")
        else:
            ax1.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')
            ax2.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def show_analysis(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(fill=BOTH, expand=True)
        ttk.Label(frame, text="Analysis Page - Coming Soon", font=("Helvetica", 16)).pack(pady=20)

    def show_income(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Input fields for income entry
        ttk.Label(frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.income_date_entry = ttk.Entry(frame)
        self.income_date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Fix for calendar button to show a calendar popup
        def select_income_date():
            import calendar
            from tkinter import Toplevel

            def set_date():
                selected_date = f"{cal.get_date()}"
                self.income_date_entry.delete(0, tk.END)
                self.income_date_entry.insert(0, selected_date)
                date_window.destroy()

            date_window = Toplevel(self.root)
            date_window.title("Select Date")
            cal = calendar.Calendar(date_window)
            cal.pack(pady=20)
            ttk.Button(date_window, text="Set Date", command=set_date).pack(pady=10)

        ttk.Button(frame, text="📅", command=select_income_date).grid(row=0, column=2, padx=5, pady=5)

        # Set default date to current date
        self.income_date_entry.insert(0, "2025-04-11")

        ttk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.income_category_entry = ttk.Entry(frame)
        self.income_category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.income_amount_entry = ttk.Entry(frame)
        self.income_amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.income_desc_entry = ttk.Entry(frame)
        self.income_desc_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons for income actions
        add_btn = ttk.Button(frame, text="Add Income", command=self.add_income)
        add_btn.grid(row=4, column=0, pady=10)

        update_btn = ttk.Button(frame, text="Update Income", command=self.update_income)
        update_btn.grid(row=4, column=1, pady=10)

        reset_btn = ttk.Button(frame, text="Reset", command=self.reset_income_fields)
        reset_btn.grid(row=5, column=0, pady=10)

        delete_btn = ttk.Button(frame, text="Delete Income", command=self.delete_income)
        delete_btn.grid(row=5, column=1, pady=10)

        # Right-side frame to display income data
        self.income_data_frame = ttk.Frame(self.content_frame)
        self.income_data_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        self.display_income_data()

    def show_expense(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Input fields for expense entry
        ttk.Label(frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.expense_date_entry = ttk.Entry(frame)
        self.expense_date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Add a calendar button to select a date
        def select_expense_date():
            from tkcalendar import Calendar, DateEntry
            date_window = tk.Toplevel(self.root)
            date_window.title("Select Date")
            cal = DateEntry(date_window, selectmode='day', year=2025, month=4, day=11)
            cal.pack(pady=20)

            def set_date():
                self.expense_date_entry.delete(0, tk.END)
                self.expense_date_entry.insert(0, cal.get_date().strftime('%Y-%m-%d'))
                date_window.destroy()

            ttk.Button(date_window, text="Set Date", command=set_date).pack(pady=10)

        ttk.Button(frame, text="📅", command=select_expense_date).grid(row=0, column=2, padx=5, pady=5)

        # Set default date to current date
        self.expense_date_entry.insert(0, "2025-04-11")

        ttk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.expense_category_entry = ttk.Entry(frame)
        self.expense_category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.expense_amount_entry = ttk.Entry(frame)
        self.expense_amount_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.expense_desc_entry = ttk.Entry(frame)
        self.expense_desc_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons for expense actions
        add_btn = ttk.Button(frame, text="Add Expense", command=self.add_expense)
        add_btn.grid(row=4, column=0, pady=10)

        update_btn = ttk.Button(frame, text="Update Expense", command=self.update_expense)
        update_btn.grid(row=4, column=1, pady=10)

        reset_btn = ttk.Button(frame, text="Reset", command=self.reset_expense_fields)
        reset_btn.grid(row=5, column=0, pady=10)

        delete_btn = ttk.Button(frame, text="Delete Expense", command=self.delete_expense)
        delete_btn.grid(row=5, column=1, pady=10)

        # Right-side frame to display expense data
        self.expense_data_frame = ttk.Frame(self.content_frame)
        self.expense_data_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
        self.display_expense_data()

    # Fix for pandas DataFrame append deprecation
    def add_income(self):
        # Retrieve income details from user input
        date_str = self.income_date_entry.get().strip()
        category = self.income_category_entry.get().strip()
        amount_str = self.income_amount_entry.get().strip()
        description = self.income_desc_entry.get().strip()

        try:
            # Validate date and amount formats
            datetime.strptime(date_str, '%Y-%m-%d')
            amount = float(amount_str)

            # Create new record and append to transactions
            new_record = {
                "date": date_str,
                "category": category,
                "type": "Income",
                "amount": amount,
                "description": description
            }
            self.transactions = pd.concat([self.transactions, pd.DataFrame([new_record])], ignore_index=True)
            self.save_data()
            messagebox.showinfo("Success", "Income added successfully!")
            self.show_dashboard()  # Optionally redirect to dashboard
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def update_income(self):
        # Logic to update income
        pass

    def reset_income_fields(self):
        # Logic to reset income fields
        self.income_date_entry.delete(0, tk.END)
        self.income_category_entry.delete(0, tk.END)
        self.income_amount_entry.delete(0, tk.END)
        self.income_desc_entry.delete(0, tk.END)

    def delete_income(self):
        # Logic to delete income
        pass

    def display_income_data(self):
        # Logic to display income data in the right-side frame
        pass

    def add_expense(self):
        # Retrieve expense details from user input
        date_str = self.expense_date_entry.get().strip()
        category = self.expense_category_entry.get().strip()
        amount_str = self.expense_amount_entry.get().strip()
        description = self.expense_desc_entry.get().strip()
        
        try:
            # Validate date and amount formats
            datetime.strptime(date_str, '%Y-%m-%d')
            amount = float(amount_str)
            
            # Create new record and append to transactions
            new_record = {
                "date": date_str,
                "category": category,
                "type": "Expense",
                "amount": amount,
                "description": description
            }
            self.transactions = self.transactions.append(new_record, ignore_index=True)
            self.save_data()
            messagebox.showinfo("Success", "Expense added successfully!")
            self.show_dashboard()  # Optionally redirect to dashboard
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def update_expense(self):
        # Logic to update an existing expense
        selected_date = self.expense_date_entry.get().strip()
        selected_category = self.expense_category_entry.get().strip()
        selected_amount = self.expense_amount_entry.get().strip()
        selected_description = self.expense_desc_entry.get().strip()

        if not selected_date or not selected_category or not selected_amount:
            messagebox.showerror("Error", "Date, Category, and Amount are required to update an expense!")
            return

        try:
            # Validate date and amount
            datetime.strptime(selected_date, '%Y-%m-%d')
            selected_amount = float(selected_amount)

            # Find and update the expense in the DataFrame
            for index, row in self.transactions.iterrows():
                if row['date'] == selected_date and row['category'] == selected_category and row['type'] == 'Expense':
                    self.transactions.at[index, 'amount'] = selected_amount
                    self.transactions.at[index, 'description'] = selected_description
                    self.save_data()
                    messagebox.showinfo("Success", "Expense updated successfully!")
                    self.display_expense_data()
                    return

            messagebox.showerror("Error", "Expense not found!")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def delete_expense(self):
        # Logic to delete an expense
        selected_date = self.expense_date_entry.get().strip()
        selected_category = self.expense_category_entry.get().strip()

        if not selected_date or not selected_category:
            messagebox.showerror("Error", "Date and Category are required to delete an expense!")
            return

        try:
            # Validate date
            datetime.strptime(selected_date, '%Y-%m-%d')

            # Find and delete the expense in the DataFrame
            self.transactions = self.transactions[~((self.transactions['date'] == selected_date) &
                                                     (self.transactions['category'] == selected_category) &
                                                     (self.transactions['type'] == 'Expense'))]
            self.save_data()
            messagebox.showinfo("Success", "Expense deleted successfully!")
            self.display_expense_data()
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")

    def display_expense_data(self):
        # Logic to display expense data in the right-side frame
        for widget in self.expense_data_frame.winfo_children():
            widget.destroy()

        if self.transactions.empty:
            ttk.Label(self.expense_data_frame, text="No expense data available.").pack(pady=10)
            return

        # Filter only expense data
        expense_data = self.transactions[self.transactions['type'] == 'Expense']

        # Create a treeview to display the data
        columns = ('date', 'category', 'amount', 'description')
        tree = ttk.Treeview(self.expense_data_frame, columns=columns, show='headings')
        tree.heading('date', text='Date')
        tree.heading('category', text='Category')
        tree.heading('amount', text='Amount')
        tree.heading('description', text='Description')

        for _, row in expense_data.iterrows():
            tree.insert('', tk.END, values=(row['date'], row['category'], row['amount'], row['description']))

        tree.pack(fill=BOTH, expand=True)

    def show_budget_planner(self):
        self.clear_content()
        frame = ttk.Frame(self.content_frame)
        frame.pack(pady=20)
        ttk.Label(frame, text="Budget Planner Page - Coming Soon", font=("Helvetica", 16)).pack(pady=20)

    def confirm_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.show_login()

    def change_theme(self):
        self.style.theme_use(self.theme_var.get())

    def delete_entry(self):
        # Placeholder for delete functionality
        messagebox.showinfo("Delete", "Delete functionality is not implemented yet.")

    def clear_content(self):
        # Properly destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def save_data(self):
        self.transactions.to_csv(TRANSACTIONS_FILE, index=False)
        self.budgets.to_csv(BUDGETS_FILE, index=False)

    def perform_search(self):
        # Placeholder for search functionality
        query = self.search_var.get().strip()
        messagebox.showinfo("Search", f"Search functionality is not implemented yet.\nQuery: {query}")

    def show_main_menu(self):
        # Placeholder for main menu functionality
        messagebox.showinfo("Menu", "Main menu functionality is not implemented yet.")

    def on_resize(self, event):
        # Dynamically adjust font sizes and padding based on window dimensions
        new_width = event.width
        new_height = event.height

        # Scale font sizes based on window width
        font_size = max(10, int(new_width / 100))
        self.style.configure("TLabel", font=("Helvetica", font_size))
        self.style.configure("TButton", font=("Helvetica", font_size))
        self.style.configure("TEntry", font=("Helvetica", font_size))

        # Adjust padding for the content frame
        if hasattr(self, 'content_frame'):
            self.content_frame.pack_configure(padx=int(new_width * 0.02), pady=int(new_height * 0.02))

if __name__ == "__main__":
    root = ttk.Window()
    app = BudgetProApp(root)
    root.mainloop()
