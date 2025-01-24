from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True)
    description = Column(Text)
    reviews = relationship("ReviewHistory", back_populates="category")

class ReviewHistory(Base):
    __tablename__ = 'review_histories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=True)
    stars = Column(Integer, nullable=False)
    review_id = Column(String(255))
    tone = Column(String(255), nullable=True)
    sentiment = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    category = relationship("Category", back_populates="reviews")

class AccessLog(Base):
    __tablename__ = 'access_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)