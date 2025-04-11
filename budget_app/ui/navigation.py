import tkinter as tk
from tkinter import ttk
from ui.dashboard import Dashboard
from ui.forms import EntryForm
from ui.reports import Reports

class Navigation(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Sidebar
        sidebar = ttk.Frame(self, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        ttk.Button(sidebar, text="Dashboard", command=self.show_dashboard).pack(fill=tk.X, pady=2)
        ttk.Button(sidebar, text="Add Entry", command=self.show_entry_form).pack(fill=tk.X, pady=2)
        ttk.Button(sidebar, text="Reports", command=self.show_reports).pack(fill=tk.X, pady=2)
        
        # Content Frame
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_content()
        self.dashboard = Dashboard(self.content_frame)
        self.dashboard.pack(fill=tk.BOTH, expand=True)

    def show_entry_form(self):
        self.clear_content()
        self.entry_form = EntryForm(self.content_frame)
        self.entry_form.pack(fill=tk.BOTH, expand=True)

    def show_reports(self):
        self.clear_content()
        self.reports = Reports(self.content_frame)
        self.reports.pack(fill=tk.BOTH, expand=True)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()