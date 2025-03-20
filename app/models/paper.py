from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Paper(Base):
    __tablename__ = "papers"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(JSON)  # Store as JSON array
    abstract = Column(String)
    keywords = Column(JSON)  # Store as JSON array
    references = Column(JSON)  # Store as JSON array
    citations = Column(JSON)  # Store as JSON array
    file_path = Column(String)
    processed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    reviews = relationship("Review", back_populates="paper")
    citations = relationship("Citation", back_populates="paper") 