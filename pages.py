import tkinter as tk

from obj import TableToGetStoqInfo, TableToShowStoqInfo, Summary, GetInfoForMomentum, ShowMomentum
#from simulation_momentum import SimulateMomemntum

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="Main Page", font=("Helvetica", 32)).grid(row=0, column=10, padx=500, pady=20)

        tk.Button(self, text="Check stats about some stock!", font=("Helvetica", 22), command=lambda: controller.show_frame(InfoStock)).grid(row=1, column=0, pady=10)
        tk.Button(self, text="Simulate momentum strategy!", font=("Helvetica", 22), command=lambda: controller.show_frame(MomentumStrategy)).grid(row=1, column=1, pady=10)


class InfoStock(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)


        tk.Label(self, text="Stock Stats", font=("Helvetica", 32)).grid(row=0, column=10, padx=500, pady=5)

        tk.Label(self, text="Go back to main page", font=("Helvetica", 16)).grid(row=0, column=0, padx=0, pady=5)
        tk.Button(self, text="Back to Main Page", command=lambda: controller.show_frame(MainPage)).grid(row=1, column=0, pady=10)


        def show_summary(self, stoq_ticker, info, hist1y):
            try:
                self.show_frame.destroy()
            except:
                pass
            print("B")
            self.show_frame = Summary(self, stoq_ticker, info, hist1y)
            self.show_frame.grid(row=1, column=0)
        def show_basic_info(self, stoq_ticker, info):
            pass
        def show_info(self, stock_code):
            try:
                self.info_frame.destroy()
            except:
                pass
            self.info_frame = TableToShowStoqInfo(self, stock_code, show_summary, show_basic_info)
            self.info_frame.grid(row=1, column=0)

        tableGetInfo = TableToGetStoqInfo(self, show_info)
        tableGetInfo.grid(row=2, column=5)

class MomentumStrategy(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Make the grid expand to fill the space
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)


        tk.Label(self, text="Momentum Strategy", font=("Helvetica", 16)).grid(row=0, column=1)

        tk.Label(self, text="Go back to main page", font=("Helvetica", 16)).grid(row=0, column=0)
        tk.Button(self, text="Back to Main Page", command=lambda: controller.show_frame(MainPage)).grid(row=1, column=0)

        def show_info(self, start, period, stoqs_codes, money, percentile, deposit):
            try:
                self.info_frame.destroy()
            except:
                pass
            
            self.info_frame = ShowMomentum(self, start, period, stoqs_codes, money, percentile, deposit)
            self.info_frame.grid(row=7, column=0)
            print(stoqs_codes)

        infoForMomentum = GetInfoForMomentum(self, show_info)
        infoForMomentum.grid(row=2, column=5)