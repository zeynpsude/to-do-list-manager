from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from typing import Optional
from .database import Base

# --- SQLAlchemy Modeli (Veritabanı Tablosu) ---
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# --- Pydantic Modelleri (API Şemaları) ---
# Kullanıcının veri gönderirken (POST/PUT) kullanacağı yapı
class TodoItem(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

    # Veritabanından veri dönerken id bilgisini de içermesi için
    class Config:
        from_attributes = True

class TodoResponse(TodoItem):
    id: int