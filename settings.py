from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# PostgreSQLの接続情報
# ここは実際の接続先情報に合わせてください
path = 'postgresql+psycopg2://postgres:mysecretpassword@localhost:5433/study_management'

# エンジンの作成（データベースに接続するためのエンジン）
Engine = create_engine(
    path,  # 接続するデータベースのURL
    echo=False  # SQLの実行内容を表示しない
)

# Baseクラスを定義（モデルを定義するためのベースクラス）
Base = declarative_base()
