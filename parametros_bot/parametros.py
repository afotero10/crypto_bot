import pandas as pd
import numpy as np

def typical_price(bars):
    res = (bars['High'] + bars['Low'] + bars['Close']) / 3.
    return pd.Series(index=bars.index, data=res)

def numpy_rolling_window(data, window):
    shape = data.shape[:-1] + (data.shape[-1] - window + 1, window)
    strides = data.strides + (data.strides[-1],)
    return np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)


def numpy_rolling_mean(data, window, as_source=False):
    return np.mean(numpy_rolling_window(data, window), axis=-1)


def numpy_rolling_std(data, window, as_source=False):
    return np.std(numpy_rolling_window(data, window), axis=-1, ddof=1)


def rolling_mean(series, window=200, min_periods=None):
    min_periods = window if min_periods is None else min_periods
    if min_periods == window and len(series) > window:
        return numpy_rolling_mean(series, window, True)
    else:
        try:
            return series.rolling(window=window, min_periods=min_periods).mean()
        except Exception as e:  # noqa: F841
            return pd.Series(series).rolling(window=window, min_periods=min_periods).mean()


def rolling_std(series, window=200, min_periods=None):
    min_periods = window if min_periods is None else min_periods
    if min_periods == window and len(series) > window:
        return numpy_rolling_std(series, window, True)
    else:
        try:
            return series.rolling(window=window, min_periods=min_periods).std()
        except Exception as e:  # noqa: F841
            return pd.Series(series).rolling(window=window, min_periods=min_periods).std()


def bollinger_bands(series, window=20, stds=2):
    ma = rolling_mean(series, window=window, min_periods=1)
    std = rolling_std(series, window=window, min_periods=1)
    upper = ma + std * stds
    lower = ma - std * stds

    return pd.DataFrame(index=series.index, data={
        'upper': upper,
        'mid': ma,
        'lower': lower
    })



def rsi(close,period=14):
    delta = close.diff()

    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    rsi=round(100 - (100 / (1 + RS)),3)
    return rsi


def initial_margin(qty,entry_price,leverage):

    IMR=1/leverage
    IM=qty*entry_price*IMR
    return IM

def Pnl(entrada,entry_price,exit_price,qty):

    if entrada=='short':
        pnl=(entry_price-exit_price)*qty
    if entrada == 'long':
        pnl = -(entry_price - exit_price) * qty
    return pnl

def ROE(pnl,initial_margin):

    return 100*pnl/initial_margin

# eterle el roe de ganacia y perdida  que determine el precio de salida para ambos casos
#como un target price de la calculadora de binance
#def precio_salida(roe,)