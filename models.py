from sqlalchemy import Column, Integer, String, DateTime, ForeignKey  # ForeignKey を追加
from datetime import datetime  # datetime をインポート
from settings import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # フロントエンドの "name" に一致
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Project(name={}, description={}, created_at={})>".format(
            self.name,
            self.description,
            self.created_at
        )

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)  # ForeignKey を追加
    name = Column(String, nullable=False)  # フロントエンドの "name" に合わせて "title" を "name" に変更
    status = Column(String, nullable=False, default='Todo')  # デフォルト値を "Todo" に設定
    priority = Column(Integer, default=2)  # デフォルト値をそのまま保持
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task(name={}, status={}, priority={}, created_at={})>".format(
            self.name,
            self.status,
            self.priority,
            self.created_at
        )
