from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from app.core.database import Base, paper_keywords, paper_references, paper_citations

class Paper(Base):
    """SQLAlchemy model for papers."""
    __tablename__ = "papers"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)  # Store as JSON
    abstract = Column(Text, nullable=False)
    content = Column(Text)
    doi = Column(String)
    url = Column(String)
    publication_date = Column(DateTime)
    journal = Column(String)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Many-to-many relationships using association tables
    keywords = relationship("Keyword", secondary=paper_keywords, back_populates="papers")
    references = relationship("Reference", secondary=paper_references, back_populates="papers")
    citations = relationship("Citation", secondary=paper_citations, back_populates="papers")
    reviews = relationship("Review", back_populates="paper") 