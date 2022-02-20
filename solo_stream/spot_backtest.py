import talib
from parametros_bot import parametros
import pandas as pd
from parametros_bot.sacar_datos_prueba import df_datos_iniciales
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)

BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=70
RSI_bot=40
symbol='ETHUSDT'
df_datos=pd.DataFrame(df_datos_iniciales)







def cantidad_venta(precio,df_compras):

    #global df_compras

    cantidad=0
    if len(df_compras)>0:

         lista_compras=df_compras.copy()
         try:
            lista_compras=lista_compras[lista_compras['price'] < precio]
            indexes = lista_compras[lista_compras['price'] < precio].index.tolist()
         except:
             indexes=[]
             cantidad=0


         if len(indexes)>0:
             cantidad=lista_compras['qty'].sum()
             df_compras=lista_compras.drop(indexes)

         return cantidad,df_compras
    else:
        return 0,df_compras

def cantidad_compra(x):

    cantidad_disponible=x

    if cantidad_disponible>30:
        cantidad=cantidad_disponible-20

    elif cantidad_disponible<=30 and cantidad_disponible>10 :
        cantidad=10

    else:
        cantidad=0

    return cantidad


def trade_history():

 #debo usar otros datos.....
 df_datos = df_datos_iniciales.copy()

 df_datos['RSI'] = talib.RSI(df_datos['Close'],RSI_PERIOD)



 bollinger = parametros.bollinger_bands(
                     parametros.typical_price(df_datos),
                     window=BB_PERIOD, stds=2)
 df_datos['BB_upper']=bollinger['upper']
 df_datos['BB_mid']=bollinger['mid']
 df_datos['BB_lower']=bollinger['lower']
 bollinger3 = parametros.bollinger_bands(
                     parametros.typical_price(df_datos),
                     window=BB_PERIOD, stds=3)
 df_datos['BB_upper3']=bollinger3['upper']
 df_datos['BB_mid3']=bollinger3['mid']
 df_datos['BB_lower3']=bollinger3['lower']
 bollinger4 = parametros.bollinger_bands(
                     parametros.typical_price(df_datos),
                     window=BB_PERIOD, stds=4)
 df_datos['BB_upper4']=bollinger4['upper']
 df_datos['BB_mid4']=bollinger4['mid']
 df_datos['BB_lower4']=bollinger4['lower']
 df_datos.to_csv('parametros.csv')

 return df_datos

def realizar_prueba(df_datos):

 buy_price = []
 sell_price = []
 bb_signal = []
 cuenta_ventas = []
 cuenta_compras = []
 bolsa_venta=[]
 bolsa_compra = []

 signal = 0
 qty_compra=100
 qty_venta=0
 ventas=0
 compras=0

 max_cv=4

 df_compras = pd.DataFrame()
 cantidad=[]


 for i in range(len(df_datos)):

     precio_actual=df_datos.loc[df_datos.index[i], 'Close']
     precio_pasado = df_datos.loc[df_datos.index[i-1], 'Close']

     #condicion venta
     if df_datos.loc[df_datos.index[i],'RSI']>RSI_top and precio_actual>df_datos.loc[df_datos.index[i],'BB_mid4'] and df_datos.loc[df_datos.index[i-1], 'Close']<df_datos.loc[df_datos.index[i-1],'BB_mid4']:


            if qty_venta>0 and ventas<max_cv  :


               if i==191:
                   print(i)

               p = 0
               #a = cantidad_venta(precio_actual, d_compras)
               a,df_compras_actual = cantidad_venta(precio_actual,df_compras)
               df_compras=df_compras_actual

               if a>0:
                    buy_price.append(np.nan)
                    sell_price.append(precio_actual)
                    signal = 1
                    bb_signal.append(signal)
                    signal = 0
                    qty_compra = qty_compra + a * precio_actual
                    bolsa_compra.append(qty_compra)
                    qty_venta = qty_venta - a
                    ventas = ventas + 1
                    bolsa_venta.append(qty_venta)
                    cuenta_ventas.append(ventas)

                    if compras > 0:
                        compras = compras - 1

                    cuenta_compras.append(compras)
                    cantidad.append(np.nan)
               else:
                   buy_price.append(np.nan)
                   sell_price.append(np.nan)
                   bb_signal.append(0)
                   bolsa_compra.append(qty_compra)
                   cuenta_compras.append(compras)
                   cuenta_ventas.append(ventas)
                   bolsa_venta.append(qty_venta)
                   cantidad.append(np.nan)

            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append(0)
                bolsa_compra.append(qty_compra)
                cuenta_compras.append(compras)
                cuenta_ventas.append(ventas)
                bolsa_venta.append(qty_venta)
                cantidad.append(np.nan)


     #condicion compra
     elif df_datos.loc[df_datos.index[i],'RSI']<RSI_bot and precio_actual<df_datos.loc[df_datos.index[i], 'BB_lower'] and precio_pasado>df_datos.loc[df_datos.index[i-1], 'BB_lower']:


         #quan_buy=cantidad_compra()
         #if quan_buy>0:
            #poner_orden(symbol,'BUY', quan_buy, precio_actual)
             #guardar_trades(symbol)



             if qty_compra > 0 and compras<max_cv:

                 a=cantidad_compra(qty_compra)
                 if i==18:
                     print(i)
                 if a>0:

                     buy_price.append(precio_actual)
                     sell_price.append(np.nan)
                     signal = -1
                     bb_signal.append(signal)
                     signal = 0
                     qty_venta =qty_venta+a/ precio_actual
                     bolsa_venta.append(qty_venta)
                     qty_compra =qty_compra-a
                     compras=compras+1
                     bolsa_compra.append(qty_compra)
                     cuenta_compras.append(compras)

                     datos_compra={'price':precio_actual,'qty':a/ precio_actual}
                     df_ultimos_datos = pd.DataFrame(datos_compra, index=[0])
                     df_compras=df_compras.append(df_ultimos_datos,ignore_index=True)
                     cantidad.append(a/ precio_actual)
                     #d_compras.append(datos_compra)


                     if ventas>0:
                         ventas=ventas-1

                     cuenta_ventas.append(ventas)
                 else:
                     buy_price.append(np.nan)
                     sell_price.append(np.nan)
                     bb_signal.append(0)
                     bolsa_compra.append(qty_compra)
                     cuenta_compras.append(compras)
                     cuenta_ventas.append(ventas)
                     bolsa_venta.append(qty_venta)
                     cantidad.append(np.nan)


             else:
                 buy_price.append(np.nan)
                 sell_price.append(np.nan)
                 bb_signal.append(0)
                 bolsa_compra.append(qty_compra)
                 bolsa_venta.append(qty_venta)
                 cuenta_compras.append(compras)
                 cuenta_ventas.append(ventas)
                 cantidad.append(np.nan)






     else:

         buy_price.append(np.nan)
         sell_price.append(np.nan)
         bb_signal.append(0)
         cuenta_compras.append(compras)
         cuenta_ventas.append(ventas)
         bolsa_venta.append(qty_venta)
         bolsa_compra.append(qty_compra)
         cantidad.append(np.nan)




 df_datos['buy_price']=buy_price
 df_datos['sell_price'] = sell_price
 df_datos['bb_signal'] = bb_signal
 df_datos['cuenta_compras'] =cuenta_compras
 df_datos['cuenta_ventas'] =cuenta_ventas
 df_datos['cantidad'] =cantidad
 df_datos['bolsa_venta'] =bolsa_venta
 df_datos['bolsa_compra'] =bolsa_compra
 print(qty_compra/100)



 return df_datos


#b=trade_history()
#b.to_csv('datos_prueba.csv')
b2=pd.read_csv('../datos_prueba.csv')

a=realizar_prueba(b2)
b3=pd.read_csv('../parametros.csv')
a['sell_price'].plot(label = 'CLOSE PRICES', alpha = 0.3)
b3['BB_upper'].plot(label = 'UPPER BB', linestyle = '--', linewidth = 1, color = 'black')
b3['BB_mid'].plot(label = 'MIDDLE BB 20', linestyle = '--', linewidth = 1.2, color = 'grey')
b3['BB_lower'].plot(label = 'LOWER BB', linestyle = '--', linewidth = 1, color = 'black')
plt.scatter(a.index, a['buy_price'], marker = '^', color = 'green', label = 'BUY', s = 200)
plt.scatter(a.index, a['sell_price'], marker = 'v', color = 'red', label = 'SELL', s = 200)
plt.title('ETH BB STRATEGY TRADING SIGNALS')
plt.legend(loc = 'upper left')
plt.show()


#a.to_csv('resultados_prueba.csv')
