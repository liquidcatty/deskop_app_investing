import tkinter as tk

from pages import MainPage, InfoStock


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")  # This makes the window fullscreen
        self.title("Stocks in Neighborhood")

        container = tk.Frame(self) 
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Loop through each page class and initialize
        for F in (MainPage, InfoStock):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, page_class):
        """Raise the selected frame to the top"""
        frame = self.frames[page_class]
        frame.tkraise()

# Run the app
app = App()
app.mainloop()