import websocket, json, talib, numpy
from parametros_bot import parametros
import pandas as pd
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from parametros_bot.conexion import cliente2
from parametros_bot.sacar_datos_iniciales import df_datos_iniciales
from pathlib import Path
import numpy as np

client =cliente2


#print('data:',type(client.get_account())) #devuelve dictionary
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=99
RSI_bot=10
Trade_quantity=0.05
symbol='ETHUSDT'
cuenta_ventas=0
cuenta_compras=0
df_datos=pd.DataFrame(df_datos_iniciales)
df_datos['RSI']=np.nan
closes=[]
rsis=[]

open_orders=client.get_open_orders(symbol=symbol)


def guardar_trades(symbols):
    trades = client.get_my_trades(symbol=symbols)
    df_trades=pd.DataFrame(trades)
    df_trades['time'] = pd.to_datetime(df_trades['time'], unit='ms')
    df_trades['time'] = df_trades['time']# - pd.Timedelta(hours=5)
    df_trades.to_csv('trades.csv')


def num_open_orders(opens,side):

    if len(opens)>0:
        lista_ordenes = pd.DataFrame(opens)
        lista_ordenes = lista_ordenes.filter(['orderId', 'time', 'symbol','side'], axis=1)
        lista_ordenes['time'] = pd.to_datetime(lista_ordenes['time'], unit='ms')
        lista_ordenes['time']=lista_ordenes['time']#-pd.Timedelta(hours=5)
        indexes = lista_ordenes[lista_ordenes['side'].str.contains(side)].index.tolist()
        return len(indexes)
    else:
        return 0

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
        lista=lista[lista['isBuyer']==True]
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
         lista=lista[lista['isBuyer']==True]
         lista_compras=lista.copy()
         try:
             lista_compras = lista_compras[lista_compras['price'] < precio]
             indexes = lista_compras[lista_compras['price'] < precio].index.tolist()
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







def verificar_orden(opens,tiempo_actual):
    # hacer un data frame
    lista_ordenes = pd.DataFrame(opens)
    lista_ordenes = lista_ordenes.filter(['orderId', 'time', 'symbol'], axis=1)
    lista_ordenes['time'] = pd.to_datetime(lista_ordenes['time'], unit='ms')
    lista_ordenes['minutos sin ejecutar'] = ((tiempo_actual - lista_ordenes['time']).dt.total_seconds() / 60) #+ 300
    indexes = lista_ordenes[lista_ordenes['minutos sin ejecutar'] >= 15].index.tolist()
    result = []
    if len(indexes) > 0:
        for i in indexes:
            result = client.cancel_order(
                symbol=lista_ordenes.loc[indexes[i], 'symbol'],
                orderId=lista_ordenes.loc[indexes[i], 'orderId'])
            print('se elimino orden', lista_ordenes.loc[indexes[i], 'orderId'])


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


def cantidad_compra():

    wallet=client.get_asset_balance(asset='USDT')
    cantidad_disponible=float(wallet['free'])

    if cantidad_disponible>30:
        #cantidad=cantidad_disponible-20
        cantidad =  20

    elif cantidad_disponible<=30 and cantidad_disponible>12 :
        cantidad=10

    else:
        cantidad=10

    return cantidad

def generar_tabla_compras(symbol,precio,cuenta,cuenta2):

    orders = client.get_my_trades(symbol=symbol)
    path = '../tabla_compras.csv'
    my_file = Path(path)
    lista = pd.DataFrame(orders)
    agregar=False
    cuenta_v=0
    cuenta_c=0

    if len(orders) > 0:

        lista = lista.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'isBuyer'], axis=1)
        lista['price'] = lista['price'].astype(float)
        lista['qty'] = lista['qty'].astype(float)
        lista['time'] = pd.to_datetime(lista['time'], unit='ms')
        lista=lista.iloc[-1:]
        if lista.loc[lista.index[-1],'price']==precio:
            agregar=True
            cuenta_c=cuenta+1
            if cuenta2>0:
                cuenta_v=cuenta2-1
        else:
            cuenta_v=cuenta2
            cuenta_c=cuenta



    if my_file.is_file()and agregar:

        lista2 = pd.read_csv(path)
        lista2 = lista2.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'side'], axis=1)
        lista2['price'] = lista2['price'].astype(float)
        lista2['qty'] = lista2['qty'].astype(float)
        #lista2['time'] = pd.to_datetime(lista2['time'], unit='ms')
        lista2=lista2.append(lista,ignore_index=True)
        lista2.to_csv('tabla_compras.csv')

    return cuenta_c, cuenta_v


def verificar_venta(symbol,precio,cuenta,cuenta2):
    orders = client.get_my_trades(symbol=symbol)
    lista = pd.DataFrame(orders)
    cuenta_v = 0
    cuenta_c = 0


    if len(orders) > 0:

        lista = lista.filter(['orderId', 'time', 'price', 'qty', 'symbol', 'isBuyer'], axis=1)
        lista['price'] = lista['price'].astype(float)
        lista['qty'] = lista['qty'].astype(float)
        lista['time'] = pd.to_datetime(lista['time'], unit='ms')
        lista=lista.iloc[-1:]
        if lista.loc[lista.index[-1],'price']==precio:

            cuenta_v=cuenta2+1
            if cuenta2>0:
                cuenta_c=cuenta-1

        else:
            cuenta_v=cuenta2
            cuenta_c=cuenta


    return cuenta_c, cuenta_v





def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')


def trade_history(ws,msg):

 global cuenta_compras, cuenta_ventas, df_datos
 json_msg=json.loads(msg)


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
      dt_actual =df_ultimos_datos.loc[df_ultimos_datos.index[-1],'Date']
      df_ultimos_datos.set_index('Date', inplace=True, drop=True)
      df_datos=df_datos.append(df_ultimos_datos, ignore_index=False)
      #print('lendf', len(df_datos))


      if len(df_datos)>RSI_PERIOD:




             v_closes=df_datos['Close']#.tail(15)
             v_closes=numpy.array(v_closes)
             rsi1=talib.RSI(v_closes,RSI_PERIOD)

             df_datos.loc[df_datos.index[-1],'RSI']=rsi1[-1]
             rsi_actual=df_datos.loc[df_datos.index[-1],'RSI']
             precio_actual=df_datos.loc[df_datos.index[-1],'Close']
             precio_actual=round(precio_actual,3)
             precio_pasado = df_datos.loc[df_datos.index[-2], 'Close']

             print('rsidf: ', rsi_actual)
             print('time: ', dt_actual)

             if len(df_datos)>BB_PERIOD:
                 bollinger = parametros.bollinger_bands(
                     parametros.typical_price(df_datos),
                     window=BB_PERIOD, stds=2)
                 df_datos['BB_upper']=bollinger['upper']
                 df_datos['BB_mid']=bollinger['mid']
                 df_datos['BB_lower']=bollinger['lower']
                 bb_up_pasado = df_datos['BB_upper'].iloc[-2]
                 bb_up_actual = df_datos['BB_upper'].iloc[-1]
                 bb_low_pasado = df_datos['BB_lower'].iloc[-2]
                 bb_low_actual = df_datos['BB_lower'].iloc[-1]

                 #print('tail ',df_datos.tail())



             #venta
             if rsi_actual>RSI_top:#and precio_pasado<bb_up_pasado and precio_actual>bb_up_actual:


                if num_open_orders(open_orders,'SELL')<4 and cuenta_ventas<4 :

                    quan_sell=cantidad_venta(symbol, precio_actual)

                    if quan_sell>0:
                        poner_orden(symbol, 'SELL', quan_sell, precio_actual)
                        cc,cv=verificar_venta(symbol,round(precio_actual,4),cuenta_compras,cuenta_ventas)
                        cuenta_ventas = cv
                        cuenta_compras = cc
                        print('orden venta')
                        print('quan',quan_sell)
                        print('precio',precio_actual)
                        guardar_trades(symbol)

             #compra
             if rsi_actual<RSI_bot :#and precio_pasado>bb_low_pasado and precio_actual<bb_low_actual:
                 print('len: ',num_open_orders(open_orders, 'BUY'))
                 if num_open_orders(open_orders, 'BUY') < 4 and cuenta_compras<4:

                    quan_buy=cantidad_compra()
                    if quan_buy>0:
                        print('comprar')
                        print('quan', quan_buy)
                        print('precio', precio_actual)
                        poner_orden(symbol,'BUY', round(quan_buy/precio_actual,4), precio_actual)
                        cc,cv=generar_tabla_compras(symbol,precio_actual,cuenta_compras,cuenta_ventas)
                        cuenta_ventas=cv
                        cuenta_compras=cc
                        guardar_trades(symbol)



#mira el estado de los open orders
 if len(open_orders)>0:
    #print('entro open')
    verificar_orden(open_orders,dt_actual)
my_trades=client.get_my_trades(symbol=symbol)
df_my_trades=pd.DataFrame(my_trades)
df_my_trades.to_csv('mis_trades')

# init and start the WebSocket
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=trade_history)
ws.run_forever()


