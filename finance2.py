import time
import os

import pandas as pd
from pandas_datareader import data as web  # Reads stock data
import matplotlib.pyplot as plt  # Plotting
import matplotlib.dates as mdates  # Styling dates

import datetime as dt  # For defining dates
#global variables:
# Start date defaults
S_YEAR = 2017
S_MONTH = 1
S_DAY = 3
S_DATE_STR = f"{S_YEAR}-{S_MONTH}-{S_DAY}"
S_DATE_DATETIME = dt.datetime(S_YEAR, S_MONTH, S_DAY)

# End date defaults
E_YEAR = 2021
E_MONTH = 8
E_DAY = 19
E_DATE_STR = f"{E_YEAR}-{E_MONTH}-{E_DAY}"
E_DATE_DATETIME = dt.datetime(E_YEAR, E_MONTH, E_DAY)

folder = "C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python2/"

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

for x in range (500):
    save_to_csv_from_yahoo(folder,tickers[x],2017,1,1,2021,1,1)
print("finished")


for x in stock_not_downloaded:
    save_to_csv_from_yahoo(folder,x,2017,1,1,2021,1,1)
print("done")
print(stock_not_downloaded)

files = [x for x in listdir(folder) if isfile(join(folder, x))]

# Remove extension from file names
# Splitext splits the file name into 2 parts being the name and extension
# We say get all file names and then store just the name in our list named files
tickers = [os.path.splitext(x)[0] for x in files]
tickers

