import tkinter as tk
import os
import sys
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from ui.dashboard import Dashboard

def main():
    root = tk.Tk()
    root.title("Budget Manager")
    root.geometry("800x600")
    root.resizable(True, True)
    
    dashboard = Dashboard(root)
    
    # Add menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="About")
    menubar.add_cascade(label="Help", menu=help_menu)
    
    root.mainloop()

if __name__ == "__main__":
    main()