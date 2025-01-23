from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from settings import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # フロントエンドの "name" に一致
    created_at = Column(DateTime, default=datetime.utcnow)

    # タスクとの関連付け
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, created_at={self.created_at})>"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)  # ForeignKey を追加
    name = Column(String, nullable=False)  # フロントエンドの "name" に一致
    status = Column(String, nullable=False, default='Todo')  # デフォルト値を "Todo" に設定
    created_at = Column(DateTime, default=datetime.utcnow)

    # プロジェクトとの関連付け
    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, status={self.status}, created_at={self.created_at})>"
