### create in this file objects for use like labels, buttons etd ###
import yfinance as yf
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

from simulation_momentum import SimulateMomemntum

class TableToGetStoqInfo(tk.LabelFrame):
    def __init__(self, parent, on_submit_callback):
        super().__init__(parent, text="Tell what stock intrests you!", padx=10, pady=10)

        self.on_submit_callback = on_submit_callback
        tk.Label(self, text="Give ticker of stock you want to check!").grid(row=0, column=0, sticky='w')
        self.entry = tk.Entry(self)
        self.entry.grid(row=0, column=1, padx=5, pady=5)


        tk.Button(self, text="Submit", command=self.on_submit).grid(row=2, column=0, columnspan=2, pady=10)

    def on_submit(self):
        stock_code = self.entry.get().strip().upper()
        if stock_code:
            self.on_submit_callback(self, stock_code)

class TableToShowStoqInfo(tk.LabelFrame):
    def __init__(self, parent, stock_code, summary_open, basic_info_open):
        super().__init__(parent, text="Stock Info", padx=10, pady=10)
        self.summary_open = summary_open
        self.basic_info_open = basic_info_open
        self.stock_code = stock_code


        try:
            self.stoq = yf.download(stock_code)
        except:
            print(f"Download failed on attemp ")

        self.stoq_ticker = yf.Ticker(stock_code)


        try:
            self.info = self.stoq_ticker.info
        except:
            print(f".info failed on attemp")

        try:
            self.hist1y = self.stoq_ticker.history(period="1y")
        except Exception as e:
            print(f"History fetch failed: {e}")

        tk.Button(self, text="Summary", command=self.summary_open(self, self.stoq_ticker, self.info, self.hist1y)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(self, text="Basic data", command=self.basic_info_open(self, self.stoq_ticker, self.info)).grid(row=0, column=2, columnspan=2, pady=10)
        
    
class Summary(tk.Frame): 
    def __init__(self, parent, stoq_ticker, info, hist1y):
        super().__init__(parent)
        self.stoq_ticker = stoq_ticker
        self.info = info
        self.hist1y = hist1y
        self.fullhistory = self.stoq_ticker.history()

        # Info Labels
        tk.Label(self, text="Company Name", font=("Helvetica", 16)).grid(row=0, column=0)
        tk.Label(self, text=self.info.get("longName", "N/A"), font=("Helvetica", 16)).grid(row=0, column=1)

        tk.Label(self, text="Exchange Market:", font=("Helvetica", 12)).grid(row=1, column=0, sticky='w')
        tk.Label(self, text=self.info.get("exchange", "N/A"), font=("Helvetica", 12)).grid(row=1, column=1, sticky='w')

        tk.Label(self, text="Previous Close:", font=("Helvetica", 12)).grid(row=2, column=0, sticky='w')
        tk.Label(self, text=f"{self.info.get('previousClose', 'N/A')} {self.info.get('currency', '')}", font=("Helvetica", 12)).grid(row=2, column=1, sticky='w')

        tk.Label(self, text="Opening Price:", font=("Helvetica", 12)).grid(row=3, column=0, sticky='w')
        tk.Label(self, text=f"{self.info.get('open', 'N/A')} {self.info.get('currency', '')}", font=("Helvetica", 12)).grid(row=3, column=1, sticky='w')

        tk.Label(self, text="Max 1D:", font=("Helvetica", 12)).grid(row=4, column=0, sticky='w')
        tk.Label(self, text=f"{self.info.get('dayHigh', 'N/A')} {self.info.get('currency', '')}", font=("Helvetica", 12)).grid(row=4, column=1, sticky='w')

        tk.Label(self, text="Min 1D:", font=("Helvetica", 12)).grid(row=5, column=0, sticky='w')
        tk.Label(self, text=f"{self.info.get('dayLow', 'N/A')} {self.info.get('currency', '')}", font=("Helvetica", 12)).grid(row=5, column=1, sticky='w')

        tk.Label(self, text="Trading Volume:", font=("Helvetica", 12)).grid(row=6, column=0, sticky='w')
        tk.Label(self, text=f"{self.info.get('volume', 'N/A')} pcs", font=("Helvetica", 12)).grid(row=6, column=1, sticky='w')

        tk.Label(self, text="Trading Value:", font=("Helvetica", 12)).grid(row=7, column=0, sticky='w')
        value = self.info.get('volume', 0) * self.info.get('currentPrice', 0)
        tk.Label(self, text=f"{value:,.0f} {self.info.get('currency', '')}", font=("Helvetica", 12)).grid(row=7, column=1, sticky='w')

        tk.Label(self, text="1Y Return:", font=("Helvetica", 12)).grid(row=9, column=0, sticky='w')
        try:
            tk.Label(self, text=f"{100 * (self.hist1y['Open'].iloc[-1] - self.hist1y['Close'].iloc[0]) / self.hist1y['Close'].iloc[0]:.2f} %", font=("Helvetica", 12)).grid(row=9, column=1, sticky='w')
        except Exception:
            tk.Label(self, text="N/A", font=("Helvetica", 12)).grid(row=9, column=1, sticky='w')

        tk.Label(self, text="Max 1Y:", font=("Helvetica", 12)).grid(row=10, column=0, sticky='w')
        tk.Label(self, text=f"{round(self.hist1y['High'].max(), 2)} {self.info.get('currency')}", font=("Helvetica", 12)).grid(row=10, column=1, sticky='w')

        tk.Label(self, text="Min 1Y:", font=("Helvetica", 12)).grid(row=11, column=0, sticky='w')
        tk.Label(self, text=f"{round(self.hist1y['Low'].min(), 2)} {self.info.get('currency')}", font=("Helvetica", 12)).grid(row=11, column=1, sticky='w')

        # Plot stock price history
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(self.hist1y.index, self.hist1y['Close'], label='Close Price', color='blue')
        ax.set_title(f"{self.stoq_ticker} Price History")
        ax.set_xlabel("Date")
        ax.set_ylabel(f"Price ({self.info.get('currency', '')})")
        ax.grid(True)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=12, column=0, columnspan=2, pady=(10, 0), sticky='nsew')

class BasicInfo(tk.Frame):
    def __init__(self, parent):
        pass

class GetInfoForMomentum(tk.Frame):
    def __init__(self, parent, on_submit_callback):
        super().__init__(parent)
        self.on_submit_callback = on_submit_callback

        tk.Label(self, text="Give tickers(seperate them by space)").grid(row=0, column=0, sticky='w')
        self.entry_stoqs = tk.Entry(self)
        self.entry_stoqs.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text="Starting date (YYYY-MM-DD)").grid(row=1, column=0, sticky='w')
        self.entry_start = tk.Entry(self)
        self.entry_start.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="How often change stoqs(in months)").grid(row=2, column=0, sticky='w')
        self.entry_period = tk.Entry(self)
        self.entry_period.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="How much money do you invest").grid(row=3, column=0, sticky='w')
        self.entry_money = tk.Entry(self)
        self.entry_money.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Percentile of the best performing stocks(a decimal fraction)").grid(row=4, column=0, sticky='w')
        self.entry_percentile = tk.Entry(self)
        self.entry_percentile.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Deposit for period").grid(row=5, column=0, sticky='w')
        self.entry_deposit = tk.Entry(self)
        self.entry_deposit.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self, text="Submit", command=self.get_info).grid(row=6, column=0, columnspan=2, pady=10)

    def get_info(self):
        stoqs_codes = self.entry_stoqs.get().split()
        start = self.entry_start.get()
        period = int(self.entry_period.get())
        money = int(self.entry_money.get())
        percentile = float(self.entry_percentile.get())
        deposit = int(self.entry_deposit.get())
        if stoqs_codes:
            self.on_submit_callback(self, start, period, stoqs_codes, money, percentile, deposit)

class ShowMomentum(tk.Frame):
    def __init__(self, parent, start, period, stoqs, money, percentile, deposit_per_period):
        super().__init__(parent)
        simulation_of_momentum_strategy = SimulateMomemntum(start, period, stoqs, money, percentile, deposit_per_period)
        df_of_simulation = simulation_of_momentum_strategy.money_df
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(df_of_simulation.index, df_of_simulation["Worth"], label="Portfolio history", color="green")
        ax.set_title("Portfolio Value Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Worth")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)