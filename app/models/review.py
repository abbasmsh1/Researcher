from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel

from app.core.database import Base

class Section(BaseModel):
    title: str
    content: str
    subsections: list = []

class ReviewSchema(BaseModel):
    id: int
    paper_id: int
    sections: list
    generated_at: datetime

    class Config:
        from_attributes = True

class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    sections = Column(JSON)  # Store as JSON array
    generated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    paper = relationship("Paper", back_populates="reviews") 