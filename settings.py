import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env ファイルから環境変数を読み込む
load_dotenv()

# PostgreSQL の接続情報を環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file.")

# エンジンの作成（データベースに接続するためのエンジン）
Engine = create_engine(
    DATABASE_URL,  # 接続するデータベースのURL
    echo=False,  # SQLの実行内容を表示しない
)
