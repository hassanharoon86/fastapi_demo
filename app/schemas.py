from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# class Post(BaseModel):

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  # rating: Optional[int] = None

class PostCreate(PostBase):
  pass

class PostResponse(PostBase):
  id: int
  created_at: datetime

  class Config:
    orm_mode = True
