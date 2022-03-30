from pydantic import BaseModel
from typing import List
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str

class Project(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True

class ProjectInDB(Project):
    id: int
    owner_id: int
