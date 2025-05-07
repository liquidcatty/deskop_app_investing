import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
from time import sleep

class SimulateMomemntum:
    def __init__(self, start, period, stoqs_to_download, money, best_percent_of_stoqs):
        self.start = pd.to_datetime(start)
        self.period = period
        self.stoqs_to_download = stoqs_to_download

        downloaded = {}
        for ticker in self.stoqs_to_download:
            df = yf.download(ticker, auto_adjust=True)
            downloaded[ticker] = df
            sleep(1)

        self.data = pd.concat(downloaded, axis=1)
        self.prices = self.data.drop(columns=self.generate_columns_to_delete())
        self.prices.index = pd.to_datetime(self.prices.index)
        self.money = money
        self.best_percent_of_stoqs = 1 - best_percent_of_stoqs

        


        self.point = self.next_opened_stock_market_day(self.start)

        self.simulate_periods()
    def next_opened_stock_market_day(self, day):
        future=self.prices.index[self.prices.index>=day]
        if not future.empty:
            return future[0]
        else:
            return None
        
    def get_row(self, point):
        nearest_day = self.prices.index.get_indexer([point], method="nearest")
        row = self.prices.iloc[nearest_day[0]]
        return row
    
    def simulate_periods(self):
        self.nextpoint = self.next_opened_stock_market_day(self.point + pd.DateOffset(months=self.period))
        while self.point is not None and self.nextpoint is not None:
            self.prepoint = self.point
            self.point = self.next_opened_stock_market_day(self.point + pd.DateOffset(months=self.period))
            self.nextpoint = self.next_opened_stock_market_day(self.point + pd.DateOffset(months=self.period))
            if self.point is not None and self.nextpoint is not None:
                print(self.money)
                self.simulate_one_period(self.prepoint, self.point, self.nextpoint)
        future=self.prices.index[self.prices.index>=self.prices.index[-2]]
        self.simulate_one_period(self.prepoint, self.point, future[-2])
        print(self.money)
    
    def generate_columns_to_delete(self):
        par_to_remove = ["Close", "High", "Low", "Volume"]
        columns_to_delete = []
        for parameter in par_to_remove:
            for stoq in self.stoqs_to_download:
                columns_to_delete.append(tuple([stoq, parameter]))
        return columns_to_delete
    
    def calculate_the_return_on_stoqs(self, point, nextpoint, rows_to_pick):
        point_row = self.get_row(point)
        nextpoint_row = self.get_row(nextpoint)
        df_future_change_in_prices = pd.DataFrame(np.ceil(((nextpoint_row-point_row)/point_row)*10**5)/10**5)
        self.money*=(1+df_future_change_in_prices.loc[rows_to_pick].mean().iloc[0])
        self.money=int(self.money)

    def simulate_one_period(self, prepoint, point, nextpoint):
        prepoint_row = self.get_row(prepoint)
        point_row = self.get_row(point)
        df_change_in_prices = pd.DataFrame(np.ceil(((point_row-prepoint_row)/prepoint_row)*10**5)/10**5)
        df_change_in_prices["Percentile"] = df_change_in_prices.rank(pct=True) >= self.best_percent_of_stoqs
        chosen_stoqs = df_change_in_prices[df_change_in_prices["Percentile"]]
        self.calculate_the_return_on_stoqs(point, nextpoint, chosen_stoqs.index)
        return df_change_in_prices
        
    

SimulateMomemntum("1990-12-13", 3, ["TLT", "AAPL", "AAP"], 1000, 0.3)