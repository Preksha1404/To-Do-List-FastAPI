from sqlalchemy import Column, Integer, String
from database import Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    description = Column(String(512))
    completed = Column(Integer, default=0)