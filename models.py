from sqlalchemy import Column, Integer, String, DateTime  # DateTime をインポート
from datetime import datetime  # datetime をインポート

from settings import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Project(name={}, description={})>".format(
            self.name,
            self.description,
            self.created_at
        )

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False, default='todo')  # default値を追加
    priority = Column(Integer, default=2)  # default値を追加
    created_at = Column(DateTime, default=datetime.utcnow)  # created_at を追加

    def __repr__(self):
        return "<Task(title={}, status={}, created_at={})>".format(
            self.title,
            self.status,
            self.created_at
        )