import pandas as pd
import glob
from parametros_bot import parametros

BB_PERIOD=20
RSI_PERIOD = 14
path ='C:\\Users\\ANDRES\\Documents\\cryptobot\\multiples_streams\\datos' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, float_precision='high')
    #df = df.drop(df.columns[[0]], axis=1)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=False)
frame['Date'] = pd.to_datetime(frame['Date'], unit='ms')
frame['Date']=frame['Date'].dt.round('s')
frame= frame.drop(frame.columns[[0]], axis=1)
frame['High']   = frame['High'].astype(float)
frame['Low']    = frame['Low'].astype(float)
frame['Close']  = frame['Close'].astype(float)
frame = frame.sort_values(by = ['symbol','Date'])
#rsi1 = parametros.rsi(a, RSI_PERIOD)
a=0