import yfinance as yf
import pandas as pd

class StoqInfo:
    def __init__(self, stock_code="AAPL", start="2020-01-01", end="2024-12-31"):
        self.stock_code = stock_code
        self.stoq = yf.download(stock_code, start=start, end=end)
        stoq_ticker = yf.Ticker(stock_code)
        self.info = stoq_ticker.info
        self.start = start
        self.end = end

        self.stoq["Change", stock_code] = 100 * (self.stoq["Close"]-self.stoq["Open"])/self.stoq["Open"]

        print(self.stoq.columns)

    def return_price(self):
        pass


apple = StoqInfo()