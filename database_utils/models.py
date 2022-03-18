from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True)
    password = Column(String(50))
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % (self.username)

