import pandas as pd
import yfinance as yf
import talib
import matplotlib.pyplot as plt

def get_data():
    tickerSymbol='EURINR=X'
    tickerData=yf.Ticker(tickerSymbol)
    tickerDf=tickerData.history(period='1d', start='2023-1-1', end='2024-2-16')
    return tickerDf 
def clean_data(df):
    df=df.drop(['Dividends','Stock Splits'],axis=1)
    df=df.dropna()
    return df
def calculate_moving_average(df):
    df['MA_1D']=talib.SMA(df['Close'],timeperiod=2)#for one day we need to consider 2 trading day.
    df['MA_1W']=talib.SMA(df['Close'],timeperiod=5)#for one week we need to consider  5trading day.
    return df
def calculate_bollinger_band(df):
    df['upper_band'],df['middle_band'],df['lower_band']=talib.BBANDS(df['Close'],timeperiod=5)
    return df
def calculate_commodity_channel_index(df):
    df['CCI']=talib.CCI(df['High'],df['Low'],df['Close'],timeperiod=5)
    return df
def calculate_decisions(df):
    df['SMA_Decision'] = 'NEUTRAL'
    df['BB_Decision'] = 'NEUTRAL'
    df['CCI_Decision'] = 'NEUTRAL'
    # Define the conditions for the decisions
    df.loc[df['Close'] > df['MA_1D'], 'SMA_Decision'] = 'SELL'
    df.loc[df['Close'] < df['MA_1D'], 'SMA_Decision'] = 'BUY'

    df.loc[df['Close'] > df['upper_band'], 'BB_Decision'] = 'SELL'
    df.loc[df['Close'] < df['lower_band'], 'BB_Decision'] = 'BUY'

    df.loc[df['CCI'] > 100, 'CCI_Decision'] = 'SELL'
    df.loc[df['CCI'] < -100, 'CCI_Decision'] = 'BUY'
    #creating the table for decision.
    decision_df = df[['SMA_Decision', 'BB_Decision', 'CCI_Decision']]
    print(decision_df.head(50))
    return df
def plot_metrics(df):
    # Plot Close price, SMA and Bollinger Bands
    plt.figure(figsize=(14,7))
    plt.plot(df['Close'], label='Close Price', color='blue')
    plt.plot(df['MA_1D'], label='MA_1D', color='red')
    plt.plot(df['upper_band'], label='Upper Band', color='c')
    plt.plot(df['lower_band'], label='Lower Band', color='c')
    plt.title('Close Price, SMA and Bollinger Bands')
    plt.legend()
    plt.show()
    # Plot CCI
    plt.figure(figsize=(14,7))
    plt.plot(df['CCI'], label='CCI', color='blue')
    plt.axhline(100, color='red') # Sell decision line
    plt.axhline(-100, color='green') # Buy decision line
    plt.title('Commodity Channel Index (CCI)')
    plt.legend()
    plt.show()
    # print(df)
     

df = get_data()
df = clean_data(df)
df = calculate_moving_average(df)
df = calculate_bollinger_band(df)
df = calculate_commodity_channel_index(df)
df = calculate_decisions(df)
plot_metrics(df)



# Utilized yfinance to fetch historical data for the EUR/INR currency pair.
# Implemented a function to retrieve daily historical data within a specified date range.
# Data Cleaning:

# Developed a data cleaning function to remove unnecessary columns (Dividends, Stock Splits) and handle missing values.
# Technical Analysis:

# Calculated moving averages (1-day and 1-week) using TA-Lib to identify trends.
# Implemented Bollinger Bands to analyze price volatility.
# Computed the Commodity Channel Index (CCI) to identify cyclical trends in the market.
# Decision Making:

# Developed a function to calculate trading decisions based on technical indicators.
# Defined conditions for Simple Moving Average (SMA), Bollinger Bands (BB), and Commodity Channel Index (CCI) to generate 'BUY' or 'SELL' signals.
# Created a table to display the decisions for each indicator.
# Data Visualization:

# Used Matplotlib to visualize the calculated technical indicators and historical price data.