from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None

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
  for p in my_posts:
    if p['id'] == id:
      return p

def find_index_post(id):
  for i, p in enumerate(my_posts):
    if p['id'] == id:
      return i

@app.get('/')
async def root():
  return {'message': "Welcome to my API!"}

@app.get('/posts')
async def posts():
  return {'data': my_posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def posts(post: Post):
  post_dict = post.model_dump()
  post_dict['id'] = randrange(0, 10000000)
  my_posts.append(post_dict)
  return {'data': post_dict}

@app.get('/posts/{id}')
async def get_post(id: int):
  post = find_post(int(id))
  if not post:
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'message': f"Post with id: {id} not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Post with id: {id} not found")
  return {'post': post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index = find_index_post(int(id))
    if index is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
  index = find_index_post(int(id))
  if index is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
  post_dict = post.model_dump()
  post_dict['id'] = id
  my_posts[index] = post_dict
  return {'data': post_dict}
