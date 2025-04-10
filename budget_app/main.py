import tkinter as tk
from tkinter import ttk
from ui.dashboard import Dashboard
from database.db_handler import DBHandler

class BudgetApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Budget Manager")
        self.geometry("800x600")
        
        # Create the shared database handler
        self.db_handler = DBHandler()

        # Setup container for different frames (dashboard, forms, etc.)
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Dictionary for frames
        self.frames = {}
        for F in (Dashboard,):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Dashboard)

    def show_frame(self, frame_class):
        '''Raise the frame to the top.'''
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
