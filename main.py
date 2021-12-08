# Provides ways to work with large multidimensional arrays
import numpy as np
# Allows for further data manipulation and analysis
import pandas as pd
from pandas_datareader import data as web  # Reads stock data
import matplotlib.pyplot as plt  # Plotting
import matplotlib.dates as mdates  # Styling dates

import datetime as dt  # For defining dates


import mplfinance as mpf # Matplotlib finance

def save_to_csv_from_yahoo(ticker, syear, smonth, sday, eyear, emonth, eday):
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)

    df = web.DataReader(ticker, 'yahoo', start, end)

    df.to_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/' + ticker + '.csv')
    return df


def get_df_from_csv(ticker):
    try:
        df = pd.read_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/' + ticker + '.csv')
    except FileNotFoundError:
        print("file not found")
    else:
        return df


def daily_return_to_df(df, ticker):
    df['Daily return'] = (df['Adj Close'] / df['Adj Close'].shift(1)) - 1
    df.to_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/' + ticker + '.csv')
    return df


def get_return_defined_time(df, syear, smonth, sday, eyear, emonth, eday):
    # Create string representations for the dates
    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"
    df['Date'] = pd.to_datetime(df['Date'])

    # Use a mask to grab data between defined dates
    mask = (df['Date'] >= start) & (df['Date'] <= end)

    # Get the mean of the column named daily return
    daily_ret = df.loc[mask]['Daily return'].mean()

    # Get the number of days between 2 dates
    df2 = df.loc[mask]
    days = df2.shape[0]

    # Return the total return between 2 dates
    return (days * daily_ret)


def mplfinance_plot(ticker, chart_type, syear, smonth, sday, eyear, emonth, eday):
    # Create string representations for the dates
    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"

    try:
        # For Windows
        df = pd.read_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/' + ticker + '.csv',index_col=0,parse_dates=True)

    except FileNotFoundError:
        print("File Doesn't Exist")
    else:

        # Set data.index as DatetimeIndex
        df.index = pd.DatetimeIndex(df['Date'])

        # Define to only use data between provided dates
        df_sub = df.loc[start:end]

        # A candlestick chart demonstrates the daily open, high, low and closing price of a stock
        mpf.plot(df_sub, type='candle')

        # Plot price changes
        mpf.plot(df_sub, type='line')

        # Moving averages provide trend information (Average of previous 4 observations)
        mpf.plot(df_sub, type='ohlc', mav=4)



def price_plot(ticker, syear, smonth, sday, eyear, emonth, eday):
    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"
    try:
        df = pd.read_csv('C:/Users/KarolUrbanski/OneDrive - northvolt.com/Documents/Finance Python/' + ticker + '.csv')
    except FileNotFoundError:
        print("file not found dummy")
    else:
        # Set data.index as DatetimeIndex
        df.index = pd.DatetimeIndex(df['Date'])

        # Define to only use data between provided dates
        df_sub = df.loc[start:end]

        # Convert to Numpy array
        df_np = df_sub.to_numpy()

        # Get adjusted close data from the 5th column
        np_adj_close = df_np[:, 5]

        # Get date from the 1st
        date_arr = df_np[:, 1]

        # Defines area taken up by the plot
        fig = plt.figure(figsize=(12, 8), dpi=100)
        axes = fig.add_axes([0, 0, 1, 1])

        # Define the plot line color as navy
        axes.plot(date_arr, np_adj_close, color='navy')

        # Set max ticks on the x axis
        axes.xaxis.set_major_locator(plt.MaxNLocator(8))

        # Add a grid, color, dashes(5pts 1 pt dashes separated by 2pt space)
        axes.grid(True, color='0.6', dashes=(5, 2, 1, 2))

        # Set grid background color
        axes.set_facecolor('#FAEBD7')

def download_multiple_stocks(syear, smonth, sday, eyear, emonth, eday, ticks):
    for x in ticks:
        save_to_csv_from_yahoo(x, syear, smonth, sday, eyear, emonth, eday)


def merge_df_by_column_name(col_name, syear, smonth, sday, eyear, emonth, eday, *ticks):
    # Will hold data for all dataframes with the same column name
    mult_df = pd.DataFrame()

    start = f"{syear}-{smonth}-{sday}"
    end = f"{eyear}-{emonth}-{eday}"

    for x in ticks:
        mult_df[x] = web.DataReader(x, 'yahoo', start, end)[col_name]

    return mult_df

def plot_return_mult_stocks(investment, stock_df):
    (stock_df / stock_df.iloc[0] * investment).plot(figsize = (15,6))
    plt.grid(True)
    plt.show()









save_to_csv_from_yahoo('TSLA', 2017, 1, 1, 2021, 1, 1)
TSLA = get_df_from_csv('TSLA')
daily_return_to_df(TSLA, 'TSLA')
tot_ret = get_return_defined_time(TSLA, 2017, 1, 1, 2021, 1, 1)
print(tot_ret)
#mplfinance_plot('TSLA','ohlc', 2020, 1, 1, 2021, 1, 1)
#price_plot('TSLA',2020,1,1,2021,1,1)
tickers = ['AAPL','GOOG','NFLX','FB','TSLA']

download_multiple_stocks(2017,1,1,2021,1,1,tickers)
mult_df = merge_df_by_column_name('Adj Close', 2017,1,1,2021,1,1,tickers)
plot_return_mult_stocks(100, mult_df)
print("wtf")