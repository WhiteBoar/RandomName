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

#delete unnamed columns
def delete_unnamed_columns(df):
    df = df.loc[:,~df.columns.str.contains('^Unnamed')]
    return df

#add daily return to dataframe
def add_daily_return_to_df(df, ticker):
    df['daily_return'] = (df['Adj Close']/df['Adj Close'].shift(1)) -1
    df.to_csv(PATH + ticker + '.csv')
    return df

#calculate investmen over time (investment return without initial investment)
def get_roi_defned_time(df):
    df['Date'] = pd.to_datetime(df['Date'])
    start_val = df[df['Date'] == S_DATE_STR]['Adj Close'][0]
    end_val = df[df['Date'] == E_DATE_STR]['Adj Close'][0]
    print("Initial Price:", start_val)
    print("Final Price", end_val)
    roi = (end_val - start_val) / start_val
    return roi

#coefficient variation to check for risk
def get_cov(df):
    mean = stock_df['Adj Close'].mean()
    sd = stock_df['Adj Close'].std()
    cov = sd/mean
    return cov

# print(tickers[686])
# stock_a = get_df_from_csv(tickers[686])
# add_daily_return_to_df(stock_a,tickers[686])
# stock_a = delete_unnamed_columns(stock_a)
# save_df_to_csv(stock_a, tickers[686])

for ticker in tickers:
    print("Working on:", ticker)
    stock_df = get_df_from_csv(ticker)
    add_daily_return_to_df(stock_df,ticker)
    stock_df = delete_unnamed_columns(stock_df)
    save_df_to_csv(stock_df, ticker)

def get_valid_dates(df, sdate, edate):
    try:
        mask = (df['Date'] > sdate) & (df['Date'] <= edate)
        sm_df = df.loc[mask]
        sm_df = sm_df.set_index(['Date'])
        sm_date = sm_df.index.min()
        last_date = sm_df.index.max()

        date_leading = '-'.join(('0' if len(x) < 2 else '')+x for x in sm_date.split('-'))
        date_ending = '-'.join(('0' if len(x) < 2 else '') + x for x in last_date.split('-'))
    except Exception:
        print("Date corrupted")
    else:
        return date_leading, date_ending


def roi_between_dates(df, sdate, edate):
    try:
        start_val = df.loc[sdate, 'Adj Close']
        end_val = df.loc[edate, 'Adj Close']
        roi = ((end_val-start_val) / start_val)
    except Exception:
        print("data corrupted")



def get_mean_between_dates(df,sdate,edate):
    mask = (df['Date'] > sdate) & (df['Date'] <= edate)
    return df.loc[mask]['Adj Close'].mean()

def get_stdev_between_dates(df,sdate,edate):
    mask = (df['Date'] > sdate) & (df['Date'] <= edate)
    return df.loc[mask]['Adj Close'].std()

def get_cov_between_dates(df,sdate,edate):
    mean = get_mean_between_dates(df,sdate,edate)
    sd = get_stdev_between_dates(df,sdate,edate)
    cov = sd/mean
    return cov

