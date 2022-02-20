from binance.client import Client

#import mplfinance as mpf
import pandas as pd
from parametros_bot.conexion import cliente2

symbol='ETHUSDT'
client = cliente2
klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "14  min ago UTC")

df_datos_iniciales = pd.DataFrame(klines,  columns=['Date',
                                    'Open',
                                    'High',
                                    'Low',
                                    'Close',
                                    'Volume',
                                    'Close time',
                                    'Quote asset volume',
                                    'Number of trades',
                                    'Taker buy base asset volume',
                                    'Taker buy quote asset volume',
                                    'Ignore'])









df_datos_iniciales = df_datos_iniciales.drop(df_datos_iniciales.columns[[1,5,6, 7, 8, 9, 10, 11]], axis=1)
df_datos_iniciales['Date'] = pd.to_datetime(df_datos_iniciales['Date'], unit='ms')
#df_datos_iniciales['Date']=df_datos_iniciales['Date']- pd.Timedelta(hours=5)
df_datos_iniciales.set_index('Date', inplace=True, drop=True)

#df_datos_iniciales['Open']   = df_datos_iniciales['Open'].astype(float)
df_datos_iniciales['High']   = df_datos_iniciales['High'].astype(float)
df_datos_iniciales['Low']    = df_datos_iniciales['Low'].astype(float)
df_datos_iniciales['Close']  = df_datos_iniciales['Close'].astype(float)
#df_datos_iniciales['Volume'] = df_datos_iniciales['Volume'].astype(float)

b=df_datos_iniciales['Close'].tolist()
datos_c=[k for k in b]


