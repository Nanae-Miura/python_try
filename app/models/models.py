from models.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'user_table'
    # 主キー
    id = Column(Integer, primary_key=True)
    user_name = Column(String(128), unique=True)
    hashed_password = Column(String(128))

    def __init__(self, user_name=None, hashed_password=None):
        self.user_name = user_name
        self.hashed_password = hashed_password

        # __repr__(self):オブジェクトの文字列表記(オブジェクトの印字可能な表現を含む文字列）を返すメソッド
    def __repr__(self):
        return '<Name %r>' % (self.user_name)

class API_data(Base):
    __tablename__ = "API_info"
    id = Column(Integer, primary_key=True,autoincrement=True)
    API_key = Column(String(400), unique=True)
    API_secret= Column(String(400),unique=True)

# デフォルト値を設定しない
    def __init__(self, API_key=None, API_secret=None):
        self.API_key = API_key
        self.API_secret = API_secret

#これってなに？
# def __repr__(self):
#         return '<Name %r>' % (self.user_name)