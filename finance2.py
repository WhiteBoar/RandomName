import time

import pandas as pd
from pandas_datareader import data as web  # Reads stock data
import matplotlib.pyplot as plt  # Plotting
import matplotlib.dates as mdates  # Styling dates

import datetime as dt  # For defining dates


import mplfinance as mpf # Matplotlib finance
#hold stocks not downloaded
stock_not_downloaded = []
missing_stocks = []

def save_to_csv_from_yahoo(folder, ticker, syear, smonth, sday, eyear, emonth, eday):
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)
    try:
        print("get data for: ",ticker)
        df = web.DataReader(ticker, 'yahoo', start, end)['Adj Close']
        time.sleep(10)
        df.to_csv(folder + ticker + '.csv')
    except Exception as ex:
        stock_not_downloaded.append(ticker)
        print("couldnt download ",ticker)





# def get_df_from_csv(ticker):
#     try:
#         df = pd.read_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/Finance2' + ticker + '.csv')
#     except FileNotFoundError:
#         print("file not found")
#     else:
#         return df

def get_stock_and_df_from_csv(folder,ticker):
    try:
        df = pd.read_csv(folder + ticker + '.csv')
    except FileNotFoundError:
        print("file not found")
    else:
        return df

def get_column_from_csv(file, column_name):
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print("file not found")
    else:
        return df[column_name]

tickers = get_column_from_csv(r"C:\Users\KarolUrbanski\Downloads\Wilshire-5000-Stocks-New.csv","Ticker")
folder = "C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python2/"
for x in range (2):
    save_to_csv_from_yahoo(folder,tickers[x],2017,1,1,2020,1,1)
    print("done!")
