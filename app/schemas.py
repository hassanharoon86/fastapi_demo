from pydantic import BaseModel
from typing import Optional

# class Post(BaseModel):

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True
  # rating: Optional[int] = None

class PostCreate(PostBase):
  pass
