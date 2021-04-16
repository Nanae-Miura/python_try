from flask import Flask, render_template,request
from flask import Flask, request, Response, abort, render_template
from datetime import datetime
#タイムゾーンの読み込み
from pytz import timezone
import requests,time

app = Flask(__name__)

# ページにアクセスしたらbitflyerのビットコインの現在の価格を取得＆表示する

def get_price():

    url = "https://api.bitflyer.jp/v1/ticker"
    cc = requests.get(url).json()
    cc_last ='{:,}'.format(int(cc['ltp']))
    btc_price = ("Bitflyer＝",cc_last,"円です")
    

    now = str(datetime.now())
    get_time =("取得時刻" + now)

    url = 'https://coincheck.com/api/ticker'
    cc = requests.get(url).json()
    cc_last = '{:,}'.format(int(cc['last']))
    coincheck_price = ("Coincheck =", cc_last, "円です")
    return render_template("index.html", btc_price=btc_price,now=now, coincheck_price=coincheck_price)