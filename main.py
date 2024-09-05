from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
  title: str
  content: str
  published: bool = True
  rating: Optional[int] = None

@app.get('/')
async def root():
  return {'message': "Welcome to my API!"}

@app.get('/posts')
async def get_posts():
  return {'data': 'This is your posts'}

@app.post('/posts')
async def posts(post: Post):
  print(post.model_dump()) # print(post.dict())
  return {'data': "new post"}
