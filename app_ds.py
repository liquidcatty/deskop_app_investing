import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.state("zoomed")
root.title("Sigma")
root.geometry("300x200")


label = tk.Label(root, text="Hello Tkinter!", font=("Arial", 16))
label.pack(pady=20)



root.mainloop()