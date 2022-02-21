import websocket, json
from parametros_bot import parametros
from parametros_bot.conexion import cliente2,token_telegram,chat_id
import pandas as pd
import numpy as np
from parametros_bot.sacar_datos_iniciales_multiple_streams2 import datos_inicio
import telepot
#import pandas_ta as ta

socket_tream,df_datos_iniciales,list_simbolos=datos_inicio(1,'15m') #las velas toca cambiar el tiempo desde el archivo



BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=70
RSI_bot=30
client =cliente2
df_datos=pd.DataFrame(df_datos_iniciales)
df_datos['RSI']=np.nan
df_datos['BB_upper'] = np.nan
#df_datos['BB_mid'] = np.nan
df_datos['BB_lower'] = np.nan
#df_datos['EMA200']= np.nan

#print('data:',type(client.get_account())) #devuelve dictionary

SOCKET=socket_tream
bot=telepot.Bot(token_telegram)


def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def trade_history(ws,msg):

 global cuenta_compras, cuenta_ventas, df_datos,lista1,lista2,lista3,lista4,lista5,numarchivo
 json_msg=json.loads(msg)
 #print(json_msg)
 json_msg=json_msg['data']

 candle = json_msg['k']
 tiempo_actual = candle['T']
 symbol = json_msg['s']
 is_candle_closed = candle['x']
 low_price = candle['l']
 high_price = candle['h']
 close = candle['c']
 #print('symbol: ',symbol)
 #print('close: ',close)


 if is_candle_closed:
      print('len: ',len(df_datos))
      if len(df_datos)>38880:
          # Drop first N rows
          # by selecting all rows from N+1th row onwards
          N = 135*96
          df_datos = df_datos.iloc[N:, :]
          print('len2: ', len(df_datos))

      ultimos_datos = {'Date': tiempo_actual,'symbol': symbol, 'Close': float(close), 'High': float(high_price), 'Low': float(low_price)}
      df_ultimos_datos=pd.DataFrame(ultimos_datos,index=[0])
      df_ultimos_datos['Date'] = pd.to_datetime(df_ultimos_datos['Date'], unit='ms')
      df_ultimos_datos['Date']=df_ultimos_datos['Date'].dt.round('min')
      dt_actual =df_ultimos_datos.loc[df_ultimos_datos.index[-1],'Date']
      df_ultimos_datos.set_index('Date', inplace=True, drop=True)
      df_datos=df_datos.append(df_ultimos_datos, ignore_index=False)

      if len(df_datos) > RSI_PERIOD*len(list_simbolos): #cambiar 3 por len simbolos

         df_sym_actual=df_datos[df_datos['symbol'].str.contains(symbol)]
         a=df_sym_actual.loc[:,['Close']] #para mantener el dataframe
         rsi1 = parametros.rsi(a, RSI_PERIOD)
         df_datos[ 'RSI'].iloc[-1] = rsi1['Close'][-1]
         rsi_actual=rsi1['Close'][-1]
         precio_actual = float(close) #df_datos.loc[df_datos.index[-1], 'Close']
         precio_actual = precio_actual
         precio_pasado = df_sym_actual['Close'].iloc[-2]




         if len(df_datos) > BB_PERIOD*len(list_simbolos):
             #df_sym_actual2 = df_datos[df_datos['symbol'].str.contains(symbol)]
             bollinger = parametros.bollinger_bands(
                 parametros.typical_price(df_datos[df_datos['symbol'].str.contains(symbol)]),
                 window=BB_PERIOD, stds=2)

             df_datos['BB_upper'].iloc[-1] = bollinger['upper'].iloc[-1]
             #df_datos['BB_mid'].loc[-1] = bollinger['mid'].iloc[-1]
             df_datos['BB_lower'].iloc[-1] = bollinger['lower'].iloc[-1]
             #print('len', len(df_datos), 'rsi', rsi_actual, 'sym', symbol, 'dt ', dt_actual, 'bb up',bollinger['upper'].iloc[-1],'bb dwn',bollinger['lower'].iloc[-1])

             bb_up_pasado = bollinger['upper'].iloc[-2]
             bb_up_actual = df_datos['BB_upper'].iloc[-1]
             bb_low_pasado = bollinger['lower'].iloc[-2]
             bb_low_actual = df_datos['BB_lower'].iloc[-1]


             #print(df_datos['symbol'].iloc[-1],rsi_actual)
             # venta
             if rsi_actual > RSI_top and precio_pasado<bb_up_pasado and precio_actual>bb_up_actual:
                j = 'vender: ' + ' moneda: ' + symbol + ' Precio: ' + str(precio_pasado)
                print(j)
                bot.sendMessage(chat_id, j)
                link='https://www.binance.com/es-LA/futures/'+symbol
                bot.sendMessage(chat_id, link)



             # compra
             if rsi_actual < RSI_bot and precio_pasado>bb_low_pasado and precio_actual<bb_low_actual:
                 j = 'comprar: ' + ' moneda: ' + symbol + ' Precio: ' + str(precio_pasado)
                 print(j)
                 bot.sendMessage(chat_id, j)
                 link = 'https://www.binance.com/es-LA/futures/' + symbol
                 bot.sendMessage(chat_id, link)




ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=trade_history)
ws.run_forever()