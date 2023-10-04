import time

from binance.client import Client
import keys
import pandas as pd
import talib
import numpy as np
import requests

client = Client(keys.api_key, keys.api_secret)
df = pd.DataFrame(client.get_ticker())
am = 0.001

coin = 'BTCUSDT'


def lastData(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    # frame['EMA'] = ta.ema(frame['Close'], length=45)
    return frame


def getData(symbol, interval, limit):
    url = 'https://api.binance.com/api/v3/klines?symbol={}&interval={}&limit={}'.format(symbol, interval, limit)
    res = requests.get(url)
    return_data = []
    for each in res.json():
        return_data.append(float(each[4]))
    return np.array(return_data)


def placeOrder(order_type):
    if (order_type == 'buy'):
        order = client.create_order(coin='BTCUSDT', side='BUY', type='MARKET', amount=am)
        print("Open position", order)
    else:
        order = client.create_order(coin='BTCUSDT', side='SELL', type='MARKET', amount=am)
        print("Open position", order)


def main():
    buy = False
    sell = True
    ema8 = None
    ema45 = None
    last_ema8 = None
    last_ema45 = None

    while True:
        close_data = getData('BTCUSDT', '1m', '200')  # or lastData() method
        ema8 = talib.EMA(close_data, 8)
        ema45 = talib.EMA(close_data, 45)
        if (ema8 > ema45 and last_ema8):
            if (last_ema8 < last_ema45 and not buy):
                print('BUY!')
                placeOrder('buy')
                buy = True
                sell = False

        if (ema8 < ema45 and last_ema8):
            if (last_ema8 > last_ema45 and not sell):
                print('SELL!')
                placeOrder('sell')
                buy = False
                sell = True

        last_ema8 = ema8
        last_ema45 = ema45
        time.sleep(1)


if __name__ == '__main__':
    main()
