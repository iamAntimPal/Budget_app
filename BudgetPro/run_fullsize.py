import tkinter as tk
from ttkbootstrap import Window

if __name__ == "__main__":
    root = Window(themename="cosmo")
    root.geometry("1500x1500")  # Set the window size to 1500x1500
    root.title("BudgetPro Full Size Window")

    app = BudgetProApp(root)  # Assuming BudgetProApp is defined in main.py

    root.mainloop()