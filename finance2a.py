import time
import os

import pandas as pd
from pandas_datareader import data as web  # Reads stock data
import matplotlib.pyplot as plt  # Plotting
import matplotlib.dates as mdates  # Styling dates

import datetime as dt  # For defining dates
#global variables:
# Start date defaults
PATH = "C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python2/"
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

files = [x for x in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, x))]
tickers = [os.path.splitext(x)[0] for x in files]
stock_df = pd.DataFrame(tickers, columns= ['Ticker'])


#return dataframe from CSV file
def get_df_from_csv(ticker):
    try:
        df = pd.read_csv(PATH + ticker + '.csv')
    except FileNotFoundError:
        print("file not found")
    else:
        return df

def save_df_to_csv(df, ticker):
    df.to_csv(PATH + ticker + '.csv')

