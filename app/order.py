#注文に必要な関数を書くファイル
import pybitflyer
from flask import Flask, render_template,request
import time
from datetime import datetime
import json


#各種定義
BASE_URL ="https://api.bitflyer.jp"
url = BASE_URL + "POST /v1/me/sendchildorder"

api_key = ""
api_secret =""
api = pybitflyer.API(api_key,api_secret)

nounce =str(int(time.time()))

app = Flask(__name__)

#まずは入力された値を受け取るのが先なのでは?
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

#注文確認しました
