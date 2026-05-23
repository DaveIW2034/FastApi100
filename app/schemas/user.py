from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # 支持 ORM 自动转换

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
