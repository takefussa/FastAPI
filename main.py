from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Project, Task
from settings import Engine
from sqlalchemy.orm import sessionmaker

# FastAPI アプリケーションの作成
app = FastAPI()

# CORS ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

# データベース接続を取得する依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydanticモデル: プロジェクトの作成
class ProjectCreate(BaseModel):
    name: str

# Pydanticモデル: タスクの作成
class TaskCreate(BaseModel):
    name: str
    status: str = "Todo"

# タスクの更新用スキーマを追加
class UpdateTaskStatus(BaseModel):
    status: str

# ルートエンドポイント
@app.get("/")
async def root():
    return {"message": "Hello World From Fast API!"}

# プロジェクト一覧を取得するエンドポイント
@app.get("/projects/")
def read_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

# 新しいプロジェクトを作成するエンドポイント
@app.post("/projects/")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    project_data = Project(name=project.name)
    db.add(project_data)
    db.commit()
    db.refresh(project_data)
    return project_data

# プロジェクトを削除するエンドポイント
@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project {project_id} has been deleted."}

# プロジェクトに関連するタスク一覧を取得するエンドポイント
@app.get("/projects/{project_id}/tasks/")
def read_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    return tasks

# 新しいタスクを作成するエンドポイント
@app.post("/projects/{project_id}/tasks/")
def create_task(project_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    task_data = Task(project_id=project_id, name=task.name, status=task.status)
    db.add(task_data)
    db.commit()
    db.refresh(task_data)
    return task_data

# タスクを削除するエンドポイント
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} has been deleted."}

# タスクの状態を更新するエンドポイント
@app.put("/tasks/{task_id}")
def update_task_status(task_id: int, task_update: UpdateTaskStatus, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task
