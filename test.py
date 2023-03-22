# import requests
#
# data = requests.get('https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=647a628341514ce6955f0fac91e685a1')
# print(data.json())

import yfinance as yf
import pandas as pd
import os
from yahoo_fin.stock_info import *


import requests
import pandas as pd
import plotly


# class ScriptData:
#     def __init__(self):
#         self.api_key = 'JRSQ3SX94LAY4LRK'
#         self.data = {}
#
#     def fetch_intraday_data(self, script):
#         response = requests.get(
#             f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={script}&interval=1min&apikey={self.api_key}")
#         self.data[script] = response.json()
#
#     def convert_intraday_data(self, script):
#         time_series = self.data[script]["Time Series (1min)"]
#         data = []
#         for timestamp, values in time_series.items():
#             data.append([timestamp, float(values["1. open"]), float(values["2. high"]), float(values["3. low"]),
#                          float(values["4. close"]), int(values["5. volume"])])
#         df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
#         print(df)
#         df["timestamp"] = pd.to_datetime(df["timestamp"])
#         self.data[script] = df
#
#     def __getitem__(self, script):
#         return self.data[script]
#
#     def __setitem__(self, script, value):
#         self.data[script] = value
#
#     def __contains__(self, script):
#         return script in self.data
#
#
# script_data = ScriptData()
# script_data.fetch_intraday_data('GOOGL')
# script_data.convert_intraday_data('GOOGL')
# print(script_data['GOOGL'])
# print(type(script_data.fetch_intraday_data('AAPL')))
# script_data.convert_intraday_data('AAPL')
# print(script_data['AAPL'])


# def indicator1(df, timeperiod):
#     df["indicator"] = df["close"].rolling(window=timeperiod).mean()
#     return df[["timestamp", "indicator"]]


# indicator1(script_data['AAPL'], timeperiod=5)


class Strategy:
    def __init__(self, df):
        # self.script = script
        # self.script_data = ScriptData()
        # self.script_data.fetch_intraday_data(self.script)
        # self.script_data.convert_intraday_data(self.script)
        self.close_data = df['Close']
        self.df=df
        # print(self.close_data)
        # self.df = self.script_data[self.script]

    def indicator1(self):
        self.df['indicator'] = self.close_data.rolling(window=10).mean()
        self.indicator_data = self.df['indicator']

        print(self.indicator_data)
        #

    def generate_signals(self):
        self.indicator1()
        signals = []
        # print(self.df)
        for i in range(0, len(self.close_data)):
            # print(i)
            if (self.indicator_data[i] > self.close_data[i]
                    and self.indicator_data[i - 1] <= self.close_data[i - 1]):
                # print("BUY")
                signals.append("BUY")
            elif (self.indicator_data[i] < self.close_data[i]
                  and self.indicator_data[i - 1] >= self.close_data[i - 1]):
                signals.append("SELL")
                # print("SELL")
            else:
                signals.append("NO_SIGNAL")
                # print("NO_SIGNAL")
        # print(len(signals))
        self.df['signal'] = signals
        return self.df[self.df['signal'] != 'NO_SIGNAL']


sp500 = yf.Ticker('AAPL')
sp500 = sp500.history(period="max")
# sp500.to_csv(f"{}.csv")

# sp500.index = pd.to_datetime(sp500.index)
print(sp500)
strategy = Strategy(sp500)

# Generate signals for the AAPL script
data = strategy.generate_signals()

# Print the signals DataFrame
print(data)
print(data["signal"].iloc[-1])
