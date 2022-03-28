from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship  

from app.db.utils import Base

class Event(Base):
    __tablename__ = 'Events'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    location = Column(String(250), nullable=True) 
