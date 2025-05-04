import yfinance as yf
import pandas as pd

def necessary_info_about_stoq(start="2020-01-01", end="2024-12-31", stoq="AAPL"):
    stock = yf.Ticker(stoq)
    info = stock.info
    data = yf.download(stoq, start=start, end=end)
    data["Change"]=100*(data["Close"]-data["Open"])/data["Open"]

    print(data)

necessary_info_about_stoq()