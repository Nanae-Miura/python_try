# ライブラリの読み込み
# 関数だけ書いてappで呼び出すという形ならflaskのインポートとか要らない？
from flask import Flask, render_template, make_response, jsonify
from io import BytesIO
import urllib
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import requests
import time
from datetime import datetime
import datetime as dt
import pandas as pd
import pandas_datareader.data as dr
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import mplfinance.original_flavor as mpf
from mplfinance.original_flavor import candlestick_ohlc


app = Flask(__name__)


def chart1():
    # １データからチャートをplotする
    def get_OHLC(before, after):
        # ここからデータ取得
        url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'
        query = {
            'periods': 60,
            'before': before,
            'after': after,
        }
        res = requests.get(url, params=query).json()['result']['60']
        return res

    # UNIX時間に変換するためのもの
    # ４取得した現在時刻をUNIX時間に変換
    def unixTime(y, m, d, h): return int(
        time.mktime(datetime(y, m, d, h).timetuple()))

    # ３現在時刻を取得
    now = datetime.now()
    y, m, d, h = now.year, now.month, now.day, now.hour

    # ５直近１時間の間のデータを取得する
    data = get_OHLC(unixTime(y, m, d, h), unixTime(y, m, d, h - 1))

    # 空リスト
    Time, Open, High, Low, Close = [], [], [], [], []

    # 6取得したデータをfor文で仕分ける
    for i in data:
        Time.append(datetime.fromtimestamp(i[0]))
        Open.append(i[1])
        High.append(i[2])
        Low.append(i[3])
        Close.append(i[4])

    # 7取得したデータを表示
    pd.DataFrame({'date': Time, 'open': Open,
                  'high': High, 'low': Low, 'close': Close})

    # チャートに描画
    Date = [datetime(y, m, d, h - 1) + dt.timedelta(minutes=mi)
            for mi in range(60)]
    ohlc = zip(mdates.date2num(Date), Open, High, Low, Close)
    ax = plt.subplot()

    # 時間を15分単位で区切る
    ax.xaxis.set_major_locator(mdates.MinuteLocator([0, 15, 30, 45]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    # mpl_financeのメソッドを仕様。（描画幅やチャートの色などを指定。デフォルトは赤黒）
    # 上昇の時は緑、下落は赤
    candlestick_ohlc(ax, ohlc, width=(1 / 24 / 60) * 0.7,
                     colorup='g', colordown='r')
    # チャートタイトルのテキスト
    plt.title('BTC / JPY  by Cryptowatch API')
    plt.savefig('app/static/price.png')


