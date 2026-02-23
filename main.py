from fastapi import FastAPI, Depends, UploadFile, File, Form , Query
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from .model import  BookResponse
from .database import Base , engine , SessionLocal , BookDB

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
      db = SessionLocal()
      try:
            yield db
      finally:
            db.close()

@app.post("/books/", response_model=BookResponse)
def create_book(  name: str = Form(min_length=3, max_length=100  ),
                  author: str = Form(...),
                  year: int = Form(...),
                  image: UploadFile = File(...), db: Session = Depends(get_db)):
    

      ext = os.path.splitext(image.filename)[1]
      filename = f"{name}{ext}"
      path = os.path.join("uploads", filename)
    
      with open(path, "wb") as f:
            shutil.copyfileobj(image.file, f)

      db_book = BookDB(name=name, author = author, year = year, image_url=f"/uploads/{filename}")
      db.add(db_book)
      db.commit()
      db.refresh(db_book)
      return db_book

@app.get("/books/")
def search_books(
      db: Session = Depends(get_db),
    q: str = Query(..., min_length=3, max_length=100),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    query = db.query(BookDB).all()
    filtered = [b for b in query if q.lower() in b.name.lower()]
    start = (page - 1) * size
    return {
        "total": len(filtered),
        "page": page,
        "results": filtered[start:start+size]
    }