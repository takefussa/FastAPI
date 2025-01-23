from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base クラスを定義（モデルを定義するためのベースクラス）
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # フロントエンドの "name" に一致
    created_at = Column(DateTime, default=datetime.utcnow)

    # タスクとの関連付け
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, created_at={self.created_at})>"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)  # ForeignKey を追加
    name = Column(String, nullable=False)  # フロントエンドの "name" に一致
    status = Column(String, nullable=False, default="Todo")  # デフォルト値を "Todo" に設定
    created_at = Column(DateTime, default=datetime.utcnow)

    # プロジェクトとの関連付け
    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, status={self.status}, created_at={self.created_at})>"
