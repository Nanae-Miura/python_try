from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# データベースの接続情報を定義
# databese.pyと同じパスにonegai.dbというファイルを絶対パスで定義
database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             'users.db')
# SQliteを利用して、１で定義した絶対パスにDBを構築
print(database_file)
engine = create_engine('sqlite:///' + database_file, convert_unicode=True)
# DB接続用インスタンスを生成
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))
# Baseオブジェクトを生成して
# BaseオブジェクトをOnegaiContentクラスの引数に渡す構造
Base = declarative_base()
# そこにDBの情報を流し込む
Base.query = db_session.query_property()
# DBの初期化の関数
# 初期化対象のテーブルを指定

# テーブル作成


def init_db():
    from models import models
    Base.metadata.create_all(bind=engine)

