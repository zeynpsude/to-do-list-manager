from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, database
from .models import TodoItem  # Bu pydantic modelimiz (şemamız) olacak

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="To-Do List Manager API")

# Dependency: Her istekte yeni bir DB oturumu açar
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos", response_model=models.TodoItem)
def create_todo(todo: models.TodoItem, db: Session = Depends(get_db)):
    db_todo = models.Todo(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[models.TodoItem])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Todo).offset(skip).limit(limit).all()

@app.get("/todos/{todo_id}", response_model=models.TodoItem)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=models.TodoItem)
def update_todo(todo_id: int, updated_todo: models.TodoItem, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = updated_todo.title
    db_todo.description = updated_todo.description
    db_todo.completed = updated_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}