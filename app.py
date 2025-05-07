import tkinter as tk

from pages import MainPage, InfoStock, MomentumStrategy


from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("Stocks in Neighborhood")

        canvas = tk.Canvas(self, borderwidth=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
 
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True) 

        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Enter>", lambda e: self._bind_mouse(canvas))
        self.scrollable_frame.bind("<Leave>", lambda e: self._unbind_mouse(canvas))

        self.frames = {}
        for F in (MainPage, InfoStock, MomentumStrategy):
            frame = F(parent=self.scrollable_frame, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def on_close(self):
        import matplotlib.pyplot as plt
        plt.close('all')  
        self.destroy()

    def show_frame(self, page_class):
        self.frames[page_class].tkraise()

    def _bind_mouse(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def _unbind_mouse(self, canvas):
        canvas.unbind_all("<MouseWheel>")
        
app = App()
app.mainloop()