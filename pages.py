import tkinter as tk

from obj import TableToGetStoqInfo

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Make the grid expand to fill the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Label centered in the frame
        label = tk.Label(self, text="Main Page", font=("Helvetica", 32))
        label.grid(row=0, column=10, padx=500, pady=20)

        # Button below the label
        button = tk.Button(self, text="Check stats about some stock!", font=("Helvetica", 22),
                           command=lambda: controller.show_frame(InfoStock))
        button.grid(row=1, column=0, pady=10)

class InfoStock(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Make the grid expand to fill the space
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)

        label = tk.Label(self, text="Go back to main page", font=("Helvetica", 16))
        label.grid(row=0, column=0, padx=0, pady=5)

        button = tk.Button(self, text="Back to Main Page",
                           command=lambda: controller.show_frame(MainPage))
        button.grid(row=1, column=0, pady=10)

        labelmain = tk.Label(self, text="Stock Stats", font=("Helvetica", 32))
        labelmain.grid(row=0, column=10, padx=500, pady=5)

        tableGetInfo = TableToGetStoqInfo(self)
        tableGetInfo.grid(row=2, column=5)