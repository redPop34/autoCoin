import time
import pyupbit
import datetime
import requests

access = "dZWTThOKBIDlTXutNuFgTSQSBJxTJhQ83W03iyxs"
secret = "HEWRGm9rfV43x7j4rM2s48JGnj05K7sKwEVoQaGh"
myToken = "xoxb-1994731863174-2014475700113-QzNtNc1IKmLkfneDPKinAqbQ"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

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
post_message(myToken,"#test", "autotrade start")

lp = 1.02
bisSelled = False
countCrossLimit = 0
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.7)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price and bisSelled == False:
                krw = get_balance("KRW")
                if krw > 5000:                    
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    post_message(myToken,"#test", "BTC buy : " +str(buy_result))
                else:
                    downLimitPrice = target_price * (lp-0.02)
                    upLimitPrice = target_price * lp                    
                    if upLimitPrice < current_price:
                        countCrossLimit = countCrossLimit + 1
                        lp = lp + (0.02*countCrossLimit)
                    elif downLimitPrice > current_price and countCrossLimit > 0:
                        bisSelled = True
                        btc = get_balance("BTC")
                        if btc > 0.00008:
                            upbit.sell_market_order("KRW-BTC", btc*0.9995)
                            post_message(myToken,"#test", "BTC buy : " +str(sell_result))
        else:
            bisSelled = False
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                post_message(myToken,"#test", "BTC buy : " +str(sell_result))
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message(myToken,"#test", e)
        time.sleep(1)
