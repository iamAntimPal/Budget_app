import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BaseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.style = ttk.Style()
        self.load_styles()

    def load_styles(self):
        self.style.theme_use('clam')
        self.style.configure('TButton', padding=5, relief="flat")
        self.style.map('TButton', background=[('active', '#4CAF50')])

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        ttk.Label(self, textvariable=self.status_var).pack(side=tk.BOTTOM, fill=tk.X)

class LoginForm(BaseFrame):
    def __init__(self, parent, auth_manager):
        super().__init__(parent)
        self.auth_manager = auth_manager
        self.create_widgets()

    def create_widgets(self):
        # Username and password fields
        ttk.Label(self, text="Username:").pack(pady=5)
        self.username = ttk.Entry(self)
        self.username.pack(pady=5)
        
        ttk.Label(self, text="Password:").pack(pady=5)
        self.password = ttk.Entry(self, show="*")
        self.password.pack(pady=5)
        
        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=self.register).pack(pady=5)
        
        self.create_status_bar()

    def login(self):
        if self.auth_manager.login(self.username.get(), self.password.get()):
            self.master.show_main()
        else:
            self.status_var.set("Login failed")

    def register(self):
        try:
            self.auth_manager.register(self.username.get(), self.password.get())
            self.status_var.set("Registration successful")
        except:
            self.status_var.set("Registration failed")