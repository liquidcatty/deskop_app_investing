### create in this file objects for use like labels, buttons etd ###

import tkinter as tk


class TableToGetStoqInfo(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Tell what stock intrests you!", padx=10, pady=10)

        tk.Label(self, text="Give ticker of stock you want to check!").grid(row=0, column=0, sticky='w')
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=5, pady=5)


        tk.Button(self, text="Submit", command=self.on_submit).grid(row=2, column=0, columnspan=2, pady=10)

    def on_submit(self):
        print(f"Name: {self.entry.get()}")

class TableToShowStoqInfo(tk.LabelFrame):
    def __init__(self, parent, stoq_code):
        super().__init__(parent, text="User Input Section", padx=10, pady=10)