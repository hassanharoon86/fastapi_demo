from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
  try:
    conn = psycopg.connect(host='localhost', dbname='fastapi_demo', user='postgres', 
                          password='postgres', row_factory=dict_row)
    cursor = conn.cursor()
    print("Database connection was successfull!")
    break
  except Exception as error:
    print("Connecting to database failed")
    print(error)
    time.sleep(2)


my_posts = [
  {"title": "Post 1", "content": "Post 1 content", "id": 1}, 
  {"title": "Post 2", "content": "Post 2 content", "id": 2}
]

def find_post(id):
  cursor.execute('SELECT * FROM posts WHERE id = %s;', (id,))
  post = cursor.fetchone()
  return post

@app.get('/')
async def root():
  return {'message': "Welcome to my API!"}

@app.get('/posts', response_model=List[schemas.PostResponse])
async def posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  return posts

@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
  post = models.Post(**post.model_dump())
  
  db.add(post)
  db.commit()
  db.refresh(post)
  return post

@app.get('/posts/{id}', response_model=schemas.PostResponse)
async def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id == id).one()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Post with id: {id} not found")
  return post

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
  posts = db.query(models.Post).filter(models.Post.id == id)
  if posts.first() is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  posts.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', response_model=schemas.PostResponse)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
  post_query = db.query(models.Post).filter(models.Post.id == id)

  post = post_query.first()

  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not updated")

  post_query.update(updated_post.model_dump(), synchronize_session=False)
  db.commit()
  db.refresh(post)
  return post

@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  user = models.User(**user.model_dump())

  db.add(user)
  db.commit()
  db.refresh(user)
  return user
