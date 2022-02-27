import websocket, json
from parametros_bot import parametros
from parametros_bot.conexion import cliente2,token_telegram,chat_id
import pandas as pd
import numpy as np
from parametros_bot.sacar_datos_iniciales_multiple_streams2 import datos_inicio
import telepot


socket_tream,df_datos_iniciales,list_simbolos=datos_inicio(2,'1m') #las velas toca cambiar el tiempo desde el archivo

lista1=[]
lista2=[]
lista3=[]
lista4=[]
lista5=[]
lista6=[]
lista7=[]
numarchivo=0
numarchivo_accion=0
#para df_lista
len_listas=500
#para def_datos (rsi, y demas)
#len_closed=38880
#N=100
len_closed=550
N=100
#para df_acciones
#len_acciones=200
#N2=200
len_acciones=5
N2=len_acciones
df_acciones=pd.DataFrame(columns=['Date','symbol','price','accion'])


BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=50
RSI_bot=45
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

 global cuenta_compras, cuenta_ventas, df_datos,lista1,lista2,lista3,lista4,lista5,lista6,df_acciones,numarchivo,numarchivo_candle,numarchivo_accion
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
 lista1.append(tiempo_actual)
 lista2.append(symbol)
 lista3.append(close)
 lista4.append(high_price)
 lista5.append(low_price)
 lista6.append(is_candle_closed)

 #print('symbol: ',symbol)
 #print('close: ',close)
 print('len lista: ', len(lista5))

 if len(lista5)>=len_listas:

     df_lista=pd.DataFrame({'Date': lista1,'symbol': lista2, 'Close': lista3, 'High':lista4, 'Low':lista5,'closed:':lista6})
     df_lista.to_csv('C:\\Users\\ANDRES\\Documents\\cryptobot\\multiples_streams\\datos\\out'+str(numarchivo)+'.csv')
     numarchivo=numarchivo+1
     lista1 = []
     lista2 = []
     lista3 = []
     lista4 = []
     lista5 = []
     lista6 = []

     print(numarchivo)
     print('len lista2: ', len(lista5))


 if is_candle_closed:
      print('len df_datos: ',len(df_datos))
      if len(df_datos)>len_closed:
          # Drop first N rows
          # by selecting all rows from N+1th row onwards
          #N = 135*96

          df_datos = df_datos.iloc[N:, :]
          print('len df_datos2: ', len(df_datos))

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


             print(df_datos['symbol'].iloc[-1],rsi_actual)
             # venta
             if rsi_actual > RSI_top: #and precio_pasado<bb_up_pasado and precio_actual>bb_up_actual:
                j = 'vender: ' + ' moneda: ' + symbol + ' Precio: ' + str(precio_actual)
                print(j)
                bot.sendMessage(chat_id, j)
                link='https://www.binance.com/es-LA/futures/'+symbol
                bot.sendMessage(chat_id, link)
                if len(df_acciones)>=len_acciones:
                    df_acciones['Date'] = pd.to_datetime(df_acciones['Date'], unit='ms')
                    df_acciones['Date'] = df_acciones['Date'].dt.round('min')
                    df_acciones.set_index('Date', inplace=True, drop=True)
                    df_acciones.to_csv('C:\\Users\\ANDRES\\Documents\\cryptobot\\multiples_streams\\datos\\acciones'+str(numarchivo_accion)+'.csv')
                    numarchivo_accion = numarchivo_accion + 1
                    #df_acciones = df_datos.iloc[N2:, :]
                    df_acciones = pd.DataFrame(columns=df_acciones.columns)
                    print('len acciones2: ',len(df_acciones))

                df_acciones=df_acciones.append({'Date':tiempo_actual,'symbol':symbol,'price':precio_actual,'accion':2},ignore_index=True)
                print('len acciones: ', len(df_acciones))



             # compra
             if rsi_actual < RSI_bot: #and precio_pasado>bb_low_pasado and precio_actual<bb_low_actual:
                 j = 'comprar: ' + ' moneda: ' + symbol + ' Precio: ' + str(precio_actual)
                 print(j)
                 bot.sendMessage(chat_id, j)
                 link = 'https://www.binance.com/es-LA/futures/' + symbol
                 bot.sendMessage(chat_id, link)
                 if len(df_acciones) >= len_acciones:
                     df_acciones['Date'] = pd.to_datetime(df_acciones['Date'], unit='ms')
                     df_acciones['Date'] = df_acciones['Date'].dt.round('min')
                     df_acciones.set_index('Date', inplace=True, drop=True)
                     df_acciones.to_csv('C:\\Users\\ANDRES\\Documents\\cryptobot\\multiples_streams\\datos\\acciones'+str(numarchivo_accion) + '.csv')
                     numarchivo_accion=numarchivo_accion+1
                     #a = len_acciones
                     #df_acciones = df_datos.iloc[N2:, :]
                     df_acciones = pd.DataFrame(columns=df_acciones.columns)
                     print('len acciones2: ', len(df_acciones))

                 df_acciones=df_acciones.append({'Date': tiempo_actual, 'symbol': symbol, 'price': precio_actual, 'accion': 1},ignore_index=True)
                 print('len acciones: ', len(df_acciones))
 


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=trade_history)
ws.run_forever()