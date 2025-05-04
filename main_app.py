import tkinter as tk

#from obj import TableWithInfoAboutStoq


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.title("Stocks in Neighborhood")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Loop through each page class and initialize
        for F in (StartPage, PageOne):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page_class):
        """Raise the selected frame to the top"""
        frame = self.frames[page_class]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Start Page")
        label.pack(pady=10)

        button = tk.Button(self, text="Go to Page One",
                           command=lambda: controller.show_frame(PageOne))
        button.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text="Page One")
        label.pack(pady=10)

        button = tk.Button(self, text="Back to Start",
                           command=lambda: controller.show_frame(StartPage))
        button.pack()


app = App()
app.mainloop()