import pyupbit
import pandas as pd
import time

access = "lszD4xAHjFxO5wG2PpjzPGr43t0aTlPmOCbNM4ZV"
secret = "BfhPxYHUyWB3pkYrisK9gTmsf8vbdLcHS0NbElla"
upbit = pyupbit.Upbit(access, secret)


def get_cci():
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute5")
    pt = (df['high'] + df['low'] + df['close']) / 3
    sma = pt.rolling(14).mean()
    mad = pt.rolling(14).apply(lambda x: pd.Series(x).mad())
    cci = (pt - sma) / (0.015 * mad)
    return cci[-3:]


def get_balance(ticker):
    """์๊ณ  ์กฐํ"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


buy_count = 0

while True:
    try:
        time.sleep(1)
        temp = get_cci().astype(float)
        if temp is not None:
            a = temp
        else:
            pass
        if a[-1] < -150:
            krw = get_balance("KRW")
            if krw > 5000 and buy_count != 1:
                upbit.buy_market_order("KRW-BTC", krw * 0.333)
                buy_count = 1
        if a[-1] > 150:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc * 0.333)
        if a[-2] > -100 and buy_count == 1:
            buy_count = 0
    except Exception as e:
        print(e)
        time.sleep(1)
