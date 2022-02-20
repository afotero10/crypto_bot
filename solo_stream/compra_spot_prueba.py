import websocket, json, talib
import pandas as pd
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from parametros_bot.conexion import cliente2
from parametros_bot.sacar_datos_iniciales import df_datos_iniciales
from pathlib import Path

client =cliente2


#print('data:',type(client.get_account())) #devuelve dictionary
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=77
RSI_bot=75
Trade_quantity=0.05
symbol='ETHUSDT'
cuenta_ventas=0
cuenta_compras=0
df_datos=pd.DataFrame(df_datos_iniciales)


def cantidad_venta(symbol,precio):
    #falta filtrar que todos los datos sean de compras
    orders=client.get_my_trades(symbol=symbol)
    path= '../tabla_compras.csv'
    my_file = Path(path)

    if my_file.is_file():

        lista=pd.read_csv(path)
        lista = lista.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'isBuyer'], axis=1)
        lista['price'] = lista['price'].astype(float)
        lista['qty'] = lista['qty'].astype(float)
        #lista['time'] = pd.to_datetime(lista['time'], unit='ms')
        lista = lista[lista['isBuyer'] == True]
        lista_compras = lista.copy()
        try:
            lista_compras = lista_compras[lista_compras['price'] < precio]
            indexes = lista_compras[lista_compras['price'] < precio].index.tolist()
        except:
            cantidad=0
        if len(indexes) > 0:
            cantidad = lista_compras['qty'].sum()
            lista_compras = lista_compras.drop(indexes)
            lista_compras.to_csv('tabla_compras.csv')
        else:
            cantidad = 0
        return cantidad

    else:

        if len(orders)>0:
         lista= pd.DataFrame(orders)
         lista = lista.filter(['orderId', 'time', 'price','qty', 'symbol', 'isBuyer'],  axis=1)
         lista['price'] = lista['price'].astype(float)
         lista['qty'] = lista['qty'].astype(float)
         lista['time'] = pd.to_datetime(lista['time'], unit='ms')
         lista=lista[lista['isBuyer']==False]
         lista_compras=lista.copy()
         try:
             lista_compras = lista_compras[lista_compras['price'] < precio+200]
             indexes = lista_compras[lista_compras['price'] < precio+200].index.tolist()
         except:
             cantidad = 0
         if len(indexes) > 0:
             cantidad = lista_compras['qty'].sum()
             lista_compras = lista_compras.drop(indexes)
             lista_compras.to_csv('tabla_compras.csv')
         else:
             cantidad=0
         return cantidad

         #if not lista_compras.empty:

            #lista_compras.to_csv('tabla_compras.csv')





def poner_orden(symbols, side,cantidad,preciomoneda,order_type=ORDER_TYPE_LIMIT):
    try:
        buy_limit = client.create_order(
            symbol=symbols,
            side=side,
            type=order_type,
            timeInForce='GTC',
            quantity=cantidad,
            price=preciomoneda)

    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)




def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')



def generar_tabla_compras(symbol, precio, cuenta, cuenta2):
    orders = client.get_my_trades(symbol=symbol)
    path = '../tabla_compras.csv'
    my_file = Path(path)
    lista = pd.DataFrame(orders)
    agregar = False
    cuenta_v = 0
    cuenta_c = 0

    if len(orders) > 0:

        lista = lista.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'isBuyer'], axis=1)
        lista['price'] = lista['price'].astype(float)
        lista['qty'] = lista['qty'].astype(float)
        lista['time'] = pd.to_datetime(lista['time'], unit='ms')
        lista = lista.iloc[-2:]
        if lista.loc[lista.index[-2], 'price'] == 4784.29:
            agregar = True
            cuenta_c = cuenta + 1
            if cuenta2 > 0:
                cuenta_v = cuenta2 - 1
        else:
            cuenta_v = cuenta2
            cuenta_c = cuenta

    if my_file.is_file() and agregar:
        lista2 = pd.read_csv(path)
        lista2 = lista2.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'side'], axis=1)
        lista2['price'] = lista2['price'].astype(float)
        lista2['qty'] = lista2['qty'].astype(float)
        # lista2['time'] = pd.to_datetime(lista2['time'], unit='ms')
        lista2 = lista2.append(lista, ignore_index=True)
        lista2.to_csv('tabla_compras.csv')

    return cuenta_c, cuenta_v


def verificar_venta(symbol, precio, cuenta, cuenta2):
    orders = client.get_my_trades(symbol=symbol)
    lista = pd.DataFrame(orders)
    cuenta_v = 0
    cuenta_c = 0

    if len(orders) > 0:

        lista = lista.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'isBuyer'], axis=1)
        lista['price'] = lista['price'].astype(float)
        lista['qty'] = lista['qty'].astype(float)
        lista['time'] = pd.to_datetime(lista['time'], unit='ms')
        lista = lista.iloc[-1:]
        if lista.loc[lista.index[-1], 'price'] == 4796.95:

            cuenta_v = cuenta2 + 1
            if cuenta2 > 0:
                cuenta_c = cuenta - 1

        else:
            cuenta_v = cuenta2
            cuenta_c = cuenta

    return cuenta_c, cuenta_v

def trade_history(ws,msg):


 json_msg=json.loads(msg)
 global cuenta_compras, cuenta_ventas,df_datos

 candle=json_msg['k']
 tiempo_actual =candle['T']
 is_candle_closed=candle['x']
 low_price=candle['l']
 high_price = candle['h']
 close=candle['c']


 if is_candle_closed:

      ultimos_datos = {'Date': tiempo_actual, 'Close': float(close), 'High': float(high_price), 'Low': float(low_price)}
      df_ultimos_datos=pd.DataFrame(ultimos_datos,index=[0])
      df_ultimos_datos['Date'] = pd.to_datetime(df_ultimos_datos['Date'], unit='ms')
      df_ultimos_datos['Date']=df_ultimos_datos['Date'].dt.round('min')
      df_ultimos_datos.set_index('Date', inplace=True, drop=True)
      df_datos=df_datos.append(df_ultimos_datos, ignore_index=False)
      print('len', len(df_datos))

      if len(df_datos)>RSI_PERIOD:


             df_datos['RSI'] = talib.RSI(df_datos['Close'],RSI_PERIOD)
             rsi_actual=df_datos.loc[df_datos.index[-1],'RSI']
             print('rsi', rsi_actual)
             print('precio', close)
      #





      #precio_actual=df_datos.loc[df_datos.index[-1],'Close']
      #precio_actual=round(precio_actual,3)
      #quan_buy=11

      '''print('comprar')
      print('quan', round(quan_buy/precio_actual,5))
      print('precio', precio_actual)
      #poner_orden(symbol,'BUY', round(quan_buy/precio_actual,4), precio_actual-50)
      poner_orden(symbol, 'SELL', round(0.0021, 4), precio_actual  )
      if quan_buy==11:
          cc, cv = verificar_venta(symbol, precio_actual, cuenta_compras, cuenta_ventas)
          cuenta_ventas = cv
          cuenta_compras = cc
          quan_buy=12


      if quan_buy==12:

          cc, cv = generar_tabla_compras(symbol, precio_actual, cuenta_compras, cuenta_ventas)
          cuenta_ventas = cv
          cuenta_compras = cc
          quan_buy = 11'''






# init and start the WebSocket
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=trade_history)
ws.run_forever()


