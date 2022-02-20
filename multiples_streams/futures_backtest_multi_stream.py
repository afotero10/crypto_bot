from parametros_bot import parametros
import pandas as pd
from parametros_bot.sacar_datos_prueba_multi_stream import datos_inicio
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['figure.figsize'] = (20, 10)


df_datos_iniciales,list_simbolos=datos_inicio(2,'15m') #las velas toca cambiar el tiempo desde el archivo
df_datos_iniciales=pd.read_csv('datos_ini.csv')
#df_datos_iniciales.set_index('Date', inplace=True, drop=True)

BB_PERIOD=20
RSI_PERIOD = 14
RSI_top=70
RSI_bot=40


df_datos=df_datos_iniciales.copy()
df_datos['RSI']=np.nan
df_datos['BB_upper'] = np.nan
#df_datos['BB_mid'] = np.nan
df_datos['BB_lower'] = np.nan


def cantidad(x):

    cantidad_disponible=x

    if cantidad_disponible>30:
        cantidad=cantidad_disponible-20

    elif cantidad_disponible<=30 and cantidad_disponible>10 :
        cantidad=10

    else:
        cantidad=0

    return cantidad

#returna rsi y bollinger bands de los datos pero falta hacerlo por cada moenda
def trade_history():

#shib no esta teniendo la resolucion decimal adecuada
 rsi = []
 bu=[]
 bl=[]
 #debo usar otros datos.....
 #df_datos = df_datos_iniciales.copy()
 for i in list_simbolos:
     df_sym_actual = df_datos[df_datos['symbol'].str.contains(i)]
     a = df_sym_actual.loc[:, ['Close']]
     b= parametros.rsi(a, RSI_PERIOD)
     c=b['Close'].values.tolist()
     rsi.extend(c)

     bollinger = parametros.bollinger_bands(
                         parametros.typical_price(df_sym_actual),
                         window=BB_PERIOD, stds=2)
     d=bollinger['upper'].values.tolist()
     e=bollinger['lower'].values.tolist()
     bu.extend(d)
     bl.extend(e)


 df_datos['RSI'] = rsi
 df_datos['BB_upper'] = bu
 df_datos['BB_lower'] = bl


 return df_datos




def realizar_prueba(df_datos):

 buy_price = []
 sell_price = []
 bb_signal = []
 bolsa =[]


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
     if df_datos.loc[df_datos.index[i],'RSI']>RSI_top and precio_actual>df_datos.loc[df_datos.index[i],'BB_mid'] and df_datos.loc[df_datos.index[i-1], 'Close']<df_datos.loc[df_datos.index[i-1],'BB_mid']:


            if qty_venta>0 and ventas<max_cv  :


               a = cantidad(qty_compra)
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


b=trade_history()
b.to_csv('datos_prueba.csv')
b2=pd.read_csv('../datos_prueba.csv')

'''a=realizar_prueba(b2)
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
'''

#a.to_csv('resultados_prueba.csv')
