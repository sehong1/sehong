import pyupbit
import pandas as pd
import time

access = "lszD4xAHjFxO5wG2PpjzPGr43t0aTlPmOCbNM4ZV"
secret = "BfhPxYHUyWB3pkYrisK9gTmsf8vbdLcHS0NbElla"
upbit = pyupbit.Upbit(access, secret)


def get_cci():
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute5")
    pt = (df['high'] + df['low'] + df['close']) / 3
    sma = pt.rolling(20).mean()
    mad = pt.rolling(20).apply(lambda x: pd.Series(x).mad())
    cci = (pt - sma) / (0.015 * mad)
    return cci[-1]


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


a = []
is_ms = 0

while True:
    try:
        temp = get_cci().astype(float)
        time.sleep(1)
        if temp is not None:
            a.append(temp)
        else:
            pass

        if len(a) > 5:
            a.__delitem__(0)
            delta = a[-1] - a[-2]
            print(a, delta)
            if is_ms == 0 and a[-3] < -100 < a[-2] and -100 < a[-1]:
                krw = get_balance("KRW")
                upbit.buy_market_order("KRW-BTC", krw * 0.9995)
                is_ms = 1
            if is_ms == 1 and a[-3] > 100 > a[-2] and a[-1] < 100:
                btc = get_balance("BTC")
                upbit.sell_market_order("KRW-BTC", btc * 0.9995)
                is_ms = 0

    except Exception as e:
        print(e)
        time.sleep(1)
