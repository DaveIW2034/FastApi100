from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, comment="用户名")
    password = Column(String(100), comment="密码")
