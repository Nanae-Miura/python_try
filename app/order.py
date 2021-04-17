#注文に必要な関数を書くファイル
import pybitflyer
from flask import Flask, render_template,request
import time
from datetime import datetime
import json
from dateutil import parser
from pytz import timezone


#各種定義
BASE_URL =""
url = BASE_URL + ""

API_KEY = "8kfwQnG5Zv6oqcfnfCRsV"
API_SECRET ="qDrCkn7w1l9JI8uWSQNDsLBVIzPBaVssrjxIYwOp+Ew="
api = pybitflyer.API(API_KEY,API_SECRET)

BALANCE_KEYS =["currency_code",
            "amount",
            "available"]
balances =api.getbalance(product_code="BTC_JPY")


nounce =str(int(time.time()))

app = Flask(__name__)

#残高を取得する関数の定義
# def get_balance():
   
    # BALANCE_KEYS =["currency_code",
    #         "amount",
    #         "available"]

    # balances =api.getbalance(product_code="BTC_JPY")
  
    # for balance in balances:
    #     if balance["amount"]==0:
    #         continue
    #     for balance_key in BALANCE_KEYS:
    #         print(balance_key + " : " + str(balance[balance_key]))
    # print("=================================================")

  
#まずは入力された値を受け取る
#成り行き注文のチェックボックスにチェックが入っているかを確認する関数
@app.route("/order",methods=["POST"])
#受け取った値に応じて関数を呼び出し
def receive_market():
    order_type = request.form.get('order_type')
    if order_type == "buy_market": 
        #成行買い注文
        buy_btc=api.sendchildorder(
            #テストなので比較的価格の安いリップルで
                            product_code ="XRP_JPY",
                             child_order_type="MARKET",
                             side="BUY",
                             size=0.1,
                             minute_to_expire=1000,
                             time_in_force="GTC"
                             )

    elif order_type == "sell_market":
         #成り行き売り注文処理を書く
     sell_btc=api.sendchildorder(
            #テストなので比較的価格の安いリップルで
                            product_code ="XRP_JPY",
                             child_order_type="MARKET",
                             side="SELL",
                             size=0.1,
                             minute_to_expire=1000,
                             time_in_force="GTC"
                             )
        #注文動作確認済

    elif order_type =="get_balance":
    # #残高の情報を取得
        for balance in balances:
            if balance["amount"]==0:
                continue
            for balance_key in BALANCE_KEYS:
                print(balance_key + " : " + str(balance[balance_key]))
        print("=================================================")
