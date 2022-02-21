import websocket, json
from parametros_bot import parametros
from parametros_bot.conexion import cliente2,token_telegram,chat_id
import pandas as pd
import numpy as np
from parametros_bot.sacar_datos_iniciales_multiple_streams2 import datos_inicio
import telepot

socket_tream,df_datos_iniciales,list_simbolos=datos_inicio(1,'15m') #las velas toca cambiar el tiempo desde el archivo
SOCKET=socket_tream
lista1=[]
lista2=[]
lista3=[]
lista4=[]
lista5=[]
numarchivo=0
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def trade_history(ws,msg):

 global lista1,lista2,lista3,lista4,lista5,numarchivo
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
 #print('len: ',len(lista5))
 print('symbol: ',symbol)
 print('close: ',close)

 if len(lista5)==20:


     df_lista=pd.DataFrame({'Date': lista1,'symbol': lista2, 'Close': lista3, 'High':lista4, 'Low':lista5,'closed:':is_candle_closed})
     #df_lista.to_csv('C:\\Users\\ANDRES\\Documents\\cryptobot\\multiples_streams\\datos\\out'+str(numarchivo)+'.csv')
     numarchivo=numarchivo+1
     lista1 = []
     lista2 = []
     lista3 = []
     lista4 = []
     lista5 = []
     #print(numarchivo)
     #print(tiempo_actual)








ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=trade_history)
ws.run_forever()