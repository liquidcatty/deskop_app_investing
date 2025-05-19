import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np
from time import sleep

class SimulateMomemntum:
    def __init__(self, start, period, stoqs_to_download, money, best_percent_of_stoqs, deposit_per_period):
        self.start = pd.to_datetime(start)
        self.period = period
        self.stoqs_to_download = stoqs_to_download
        self.deposit_per_period = deposit_per_period

        downloaded = {}
        for ticker in self.stoqs_to_download:
            df = yf.download(ticker, auto_adjust=True)
            downloaded[ticker] = df
            sleep(0.5)

        self.data = pd.concat(downloaded, axis=1)
        self.prices = self.data.drop(columns=self.generate_columns_to_delete())
        self.ROC_prices = self.prices.pct_change().shift(-1)
        self.ROC_prices.columns = pd.MultiIndex.from_tuples(
            [(lvl0, lvl1, lvl2) for lvl0, lvl1, lvl2 in self.prices.columns],
            names=self.prices.columns.names)
        

        self.prices.index = pd.to_datetime(self.prices.index)
        self.money_df = pd.DataFrame([money], columns=["Worth"], index=[self.start])
        
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
        while self.nextpoint is not None:
            self.prepoint = self.point
            self.point = self.next_opened_stock_market_day(self.point + pd.DateOffset(months=self.period))
            self.nextpoint = self.next_opened_stock_market_day(self.point + pd.DateOffset(months=self.period))
            if self.nextpoint is not None:
                self.simulate_one_period(self.prepoint, self.point, self.nextpoint)
        future=self.prices.index[self.prices.index>=self.prices.index[-2]]
        self.simulate_one_period(self.prepoint, self.point, future[-2])
    
    def generate_columns_to_delete(self):
        par_to_remove = ["Close", "High", "Low", "Volume"]
        columns_to_delete = []
        for parameter in par_to_remove:
            for stoq in self.stoqs_to_download:
                columns_to_delete.append(tuple([stoq, parameter]))
        return columns_to_delete
    
    def calculate_the_return_on_stoqs(self, point, nextpoint, rows_to_pick):
        period_range = self.ROC_prices[point:nextpoint]

        if rows_to_pick is None:
            periods_change_in_prices = pd.DataFrame(0, index=period_range.index, columns=[0])
        else:
            periods_change_in_prices = period_range.loc[:, rows_to_pick]

        avg_returns = periods_change_in_prices.mean(axis=1)
        last_money = self.money_df["Worth"].iloc[-1]
        worth_series = (1 + avg_returns).cumprod() * last_money
        self.money_df = pd.concat([self.money_df, worth_series.to_frame(name="Worth")])
        self.money_df.iloc[-1] += self.deposit_per_period



    def simulate_one_period(self, prepoint, point, nextpoint):
        prepoint_row = self.get_row(prepoint)
        point_row = self.get_row(point)
        df_change_in_prices = pd.DataFrame((point_row-prepoint_row)/prepoint_row, columns=["Return"])
        df_change_in_prices = df_change_in_prices.dropna(subset=["Return"])
        df_change_in_prices["Chosen"] = df_change_in_prices.rank(pct=True) >= self.best_percent_of_stoqs 

        if df_change_in_prices[df_change_in_prices["Chosen"]].empty:
            chosen_stoqs = None
        else:
            chosen_stoqs = df_change_in_prices[df_change_in_prices["Chosen"]]
        self.calculate_the_return_on_stoqs(point, nextpoint, chosen_stoqs.index)
        return df_change_in_prices