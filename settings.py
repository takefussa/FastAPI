import os

from sqlalchemy import create_engine

# PostgreSQL の接続情報を環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables.")

# エンジンの作成（データベースに接続するためのエンジン）
Engine = create_engine(
    DATABASE_URL,  # 接続するデータベースのURL
    echo=False,  # SQLの実行内容を表示しない
)
