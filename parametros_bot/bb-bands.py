import pandas as pd
import matplotlib.pyplot as plt
import requests
import math
from termcolor import colored as cl
import numpy as np
import parametros
import talib

plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

'''
def get_historic_data(symbol):
    ticker = symbol
    iex_api_key = 'Tsk_30a2677082d54c7b8697675d84baf94b'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{ticker}/chart/max?token={iex_api_key}'
    df = requests.get(api_url).json()

    date = []
    open = []
    high = []
    low = []
    close = []

    for i in range(len(df)):
        date.append(df[i]['date'])
        open.append(df[i]['open'])
        high.append(df[i]['high'])
        low.append(df[i]['low'])
        close.append(df[i]['close'])

    date_df = pd.DataFrame(date).rename(columns={0: 'date'})
    open_df = pd.DataFrame(open).rename(columns={0: 'open'})
    high_df = pd.DataFrame(high).rename(columns={0: 'high'})
    low_df = pd.DataFrame(low).rename(columns={0: 'low'})
    close_df = pd.DataFrame(close).rename(columns={0: 'close'})
    frames = [date_df, open_df, high_df, low_df, close_df]
    df = pd.concat(frames, axis=1, join='inner')
    return df


tsla = get_historic_data('TSLA')
tsla = tsla.set_index('date')
tsla = tsla[tsla.index >= '2020-01-01']
tsla.to_csv('tsla.csv')
'''
tsla = pd.read_csv('../tsla.csv').set_index('date')
tsla.index = pd.to_datetime(tsla.index)



def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma

tsla['sma_20'] = sma(tsla['close'], 20)


def bb(data, sma, window):
    std = data.rolling(window = window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb



tsla['upper_bb'], tsla['lower_bb'] = bb(tsla['close'], tsla['sma_20'], 20)
tsla['RSI']=talib.RSI(tsla['close'],14)
#bol= parametros.bollinger_bands(parametros.typical_price(tsla), window=20, stds=2)

#print('bol')
#print(bol.tail())
print('tsla')
print(tsla.tail())




def implement_bb_strategy(data, lower_bb, upper_bb,RSI):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0

    for i in range(len(data)):
        if data[i - 1] > lower_bb[i - 1] and data[i] < lower_bb[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        elif data[i - 1] < upper_bb[i - 1] and data[i] > upper_bb[i] and RSI[i]>54:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append(0)

    return buy_price, sell_price, bb_signal


buy_price, sell_price, bb_signal = implement_bb_strategy(tsla['close'], tsla['lower_bb'], tsla['upper_bb'],tsla['RSI'])
'''
tsla['close'].plot(label = 'CLOSE PRICES', color = 'skyblue')
tsla['upper_bb'].plot(label = 'UPPER BB 20', linestyle = '--', linewidth = 1, color = 'black')
tsla['sma_20'].plot(label = 'MIDDLE BB 20', linestyle = '--', linewidth = 1.2, color = 'grey')
tsla['lower_bb'].plot(label = 'LOWER BB 20', linestyle = '--', linewidth = 1, color = 'black')
bol['upper'].plot(label = 'UPPER2 BB 20', linestyle = '--', linewidth = 1, color = 'red')
bol['lower'].plot(label = 'LOWER2 BB 20', linestyle = '--', linewidth = 1, color = 'red')

plt.legend(loc = 'upper left')
plt.title('TSLA BOLLINGER BANDS')
plt.show()
'''


tsla['close'].plot(label = 'CLOSE PRICES', alpha = 0.3)
tsla['upper_bb'].plot(label = 'UPPER BB', linestyle = '--', linewidth = 1, color = 'black')
tsla['RSI'].plot(label = 'RSI', linestyle = '--', linewidth = 1.2, color = 'grey')
tsla['lower_bb'].plot(label = 'LOWER BB', linestyle = '--', linewidth = 1, color = 'black')
plt.scatter(tsla.index, buy_price, marker = '^', color = 'green', label = 'BUY', s = 200)
plt.scatter(tsla.index, sell_price, marker = 'v', color = 'red', label = 'SELL', s = 200)
plt.title('TSLA BB STRATEGY TRADING SIGNALS')
plt.legend(loc = 'upper left')
plt.show()