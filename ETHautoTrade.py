import time
import pyupbit
import datetime

access = "dZWTThOKBIDlTXutNuFgTSQSBJxTJhQ83W03iyxs"
secret = "HEWRGm9rfV43x7j4rM2s48JGnj05K7sKwEVoQaGh"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

lp = 1.02
bisSelled = True
sleepTime = 1
bisFinished = False
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-ETH")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-ETH", 0.5)
            current_price = get_current_price("KRW-ETH")

            if target_price < current_price and bisSelled == False:
                krw = get_balance("KRW")
                if krw > 5000 and bisFinished == False:                    
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)
                    sleepTime = 5
                else:
                    bisFinished = True
                    downLimitPrice = target_price * (lp-0.02)
                    upLimitPrice = target_price * lp                    
                    if upLimitPrice < current_price:
                        lp = lp + 0.02
                    elif downLimitPrice > current_price and lp > 1.02:
                        bisSelled = True
                        lp = 1.02
                        sleepTime = 1
                        btc = get_balance("ETH")
                        if btc > 0.00008:
                            upbit.sell_market_order("KRW-ETH", btc*0.9995)
        else:
            bisSelled = False
            bisFinished = False
            sleepTime = 1
            lp = 1.02
            btc = get_balance("ETH")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(sleepTime)
    except Exception as e:
        print(e)
        time.sleep(1)