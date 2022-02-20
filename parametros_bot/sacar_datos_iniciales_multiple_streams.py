from binance.client import Client

#import mplfinance as mpf
import pandas as pd
from parametros_bot.conexion import cliente2



simbolos=["IOST/USDT",
"AKRO/USDT",
"ENJ/USDT",
"ANKR/USDT",
"CTK/USDT",
"SAND/USDT",
"QTUM/USDT",
"LRC/USDT",
"FTM/USDT",
"CHZ/USDT",
"CVC/USDT",
"MTL/USDT",
"AXS/USDT",
"ALGO/USDT",
"AVAX/USDT",
"XLM/USDT",
"XRP/USDT",
"DOT/USDT",
"BEL/USDT",
"SXP/USDT",
"ZIL/USDT",
"REN/USDT",
"SRM/USDT",
"MANA/USDT",
"DENT/USDT",
"MATIC/USDT",
"NEAR/USDT",
"THETA/USDT",
"SUSHI/USDT",
"SNX/USDT",
"GRT/USDT",
"ONE/USDT",
"CRV/USDT",
"EGLD/USDT",
"EOS/USDT",
"RSR/USDT",
"ZEC/USDT",
"BLZ/USDT",
"HNT/USDT",
"HBAR/USDT",
"TRB/USDT",
"BTT/USDT",
"BTS/USDT",
"RUNE/USDT",
"NKN/USDT",
"YFII/USDT",
"XMR/USDT",
"KSM/USDT",
"BTC/USDT",
"SC/USDT",
"DASH/USDT",
"RVN/USDT",
"KAVA/USDT",
"TOMO/USDT",
"ETC/USDT",
"OMG/USDT",
"DODO/USDT",
"LIT/USDT",
"AAVE/USDT",
"OCEAN/USDT",
"KNC/USDT",
"UNFI/USDT",
"IOTA/USDT",
"LINA/USDT",
"BCH/USDT",
"XTZ/USDT",
"COTI/USDT",
"DGB/USDT",
"UNI/USDT",
"BZRX/USDT",
"ONT/USDT",
"ALICE/USDT",
"SFP/USDT",
"WAVES/USDT",
"ETH/USDT",
"LTC/USDT",
"LINK/USDT",
"CELR/USDT",
"1INCH/USDT",
"COMP/USDT",
"BNB/USDT",
"HOT/USDT",
"FIL/USDT",
"ATOM/USDT",
"BAT/USDT",
"ICX/USDT",
"RLC/USDT",
"FLM/USDT",
"VET/USDT",
"NEO/USDT",
"XEM/USDT",
"LUNA/USDT",
"OGN/USDT",
"BAND/USDT",
"REEF/USDT",
"BAL/USDT",
"ADA/USDT",
"CHR/USDT",
"SOL/USDT",
"TRX/USDT",
"ZRX/USDT",
"ALPHA/USDT",
"STMX/USDT",
"ZEN/USDT",
"YFI/USDT",
"SKL/USDT",
"MKR/USDT",
"STORJ/USDT"
]
df_simbolos=pd.DataFrame(simbolos, columns =['sym'] )

df_simbolos=df_simbolos.replace('/','', regex=True)
#print(df_simbolos)
#ethusdt@kline_1m/btcusdt@kline_1m/shibusdt@kline_1m

#crea el enlace con multiples monedas
simbolos_stream=df_simbolos.copy()
simbolos_stream=df_simbolos['sym'].str.lower()
simbolos_stream=pd.DataFrame(simbolos_stream, columns =['sym'])
socket_stream= "wss://stream.binance.com:9443/stream?streams="

for i in range(len(simbolos_stream)):
    #print(simbolos_stream.iloc[i,0])
    if i<len(simbolos_stream):
     socket_stream =socket_stream + simbolos_stream.iloc[i,0] + "@kline_1m/"
    if i==len(simbolos_stream)-1:
     socket_stream = socket_stream + simbolos_stream.iloc[i, 0] + "@kline_1m"


list_simbolos=df_simbolos['sym'].values.tolist()
simbolos2=['SHIBUSDT','BTCUSDT','ETHUSDT']
client = cliente2
klines=[]

'''
for i in list_simbolos:

 a=client.get_historical_klines(i, Client.KLINE_INTERVAL_1MINUTE, "50 min ago UTC")
 for x in a:
   x.append(i)
 klines.extend(a)
'''
for i in simbolos2:
 a=client.get_historical_klines(i, Client.KLINE_INTERVAL_1MINUTE, "100  min ago UTC")
 for x in a:
   x.append(i)
 klines.extend(a)






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
                                    'Ignore','symbol'])









df_datos_iniciales = df_datos_iniciales.drop(df_datos_iniciales.columns[[1,5,6, 7, 8, 9, 10, 11]], axis=1)
df_datos_iniciales['Date'] = pd.to_datetime(df_datos_iniciales['Date'], unit='ms')
#df_datos_iniciales['Date']=df_datos_iniciales['Date']- pd.Timedelta(hours=5)
df_datos_iniciales.set_index('Date', inplace=True, drop=True)

#df_datos_iniciales['Open']   = df_datos_iniciales['Open'].astype(float)
df_datos_iniciales['High']   = df_datos_iniciales['High'].astype(float)
df_datos_iniciales['Low']    = df_datos_iniciales['Low'].astype(float)
df_datos_iniciales['Close']  = df_datos_iniciales['Close'].astype(float)
#df_datos_iniciales['Volume'] = df_datos_iniciales['Volume'].astype(float)





