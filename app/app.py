# Flaskとrender_template(HTMLを表示させるための関数をインポート)
from flask import Flask, request, Response, abort, render_template
from datetime import datetime
import requests,time
from datetime import datetime
#タイムゾーンの読み込み
from pytz import timezone
import requests,time


#外部ファイルの読み込み
#from ファイル名、import 関数名
from app.chart import chart1
from app.order import receive_market
# from app.get_price import get_price


# flaskオブジェクトの生成
app = Flask(__name__)

# ルーティングを統一

@app.route("/")
def home():
        #竹内追加開始
    if not is_login():
        return """
        <h1>Please login.</h2>
        <p><a href="/login">Login</a></p>
        """
    #竹内追加終了
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


#チャートを表示させるためのコード
#/chartから/に変更したが変化なし
@app.route('/')
def chart_show():
    chart1()
    #ここをchart→indexに変更した
    return render_template('index.html')



@app.route('/login/')
def login():
    return render_template('login.html')



#ルートに/indexを書いたら正常に遷移するようになった！
#APIのキーを入力したらindexのページに戻る
@app.route("/index")
def back_to_top():
    #竹内追加開始
    if not is_login():
        return """
        <h1>Please login.</h2>
        <p><a href="/login">Login</a></p>
        """
    #竹内追加終了
    return render_template("index.html")
    
  

# @app.route("/index")
# #1.外部ファイルの価格を取得する関数を呼び出す
# #2,価格を表示させる
# def show_price():
   
#     return render_template("index.html")


#indexページから注文を出す
@app.route("/order",methods=['POST'])
def order_btc():
    receive_market()
    return render_template("index.html")




# ここから下は竹内追加の簡易ログイン・ログアウト機能

from flask import Flask, request, session, redirect
app.secret_key = 'secretkeyyyyy'

USERLIST = {
    'taro': 'aaa',
    'jiro': 'bbb',
    'saburo': 'ccc',
}

@app.route('/check_login', methods=['POST'])
def check_login():
    user, pw = (None, None)
    if 'user' in request.form:
        user = request.form['user']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (user is None) or (pw is None):
        return redirect("/login")

    if try_login(user, pw) == False:
        return """
        <h1> Incorrect username or password </h1>
        <p><a href="/login">Return</a></p>
        """     
    return redirect('/index')

@app.route('/logout/')
def logout_page():
    try_logout()
    return """
    <h1>You are logged out.</h1>
    <p><a href="/">Return</a></p>
    """
def is_login():
    if 'login' in session:
        return True
    return False

def try_login(user, password):
    if not user in USERLIST:
        return False
    if USERLIST[user] != password:
        return False
    session['login'] = user
    return True

def try_logout():
    session.pop('login', None)
    return True

# 竹内追加終了