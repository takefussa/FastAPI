from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Project, Task  # Task モデルもインポート
from settings import Engine  # SQLAlchemy エンジンのインポート
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
def create_project(name: str, description: str = "", db: Session = Depends(get_db)):
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

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
def create_task(project_id: int, title: str, status: str = "todo", priority: int = 2, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(project_id=project_id, title=title, status=status, priority=priority)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

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
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = status
    db.commit()
    db.refresh(task)
    return task
