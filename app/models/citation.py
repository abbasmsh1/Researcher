from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Citation(Base):
    __tablename__ = "citations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    text = Column(String)
    reference = Column(String)
    context = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    id = Column(String, primary_key=True)
    paper_id = Column(String, ForeignKey("papers.id"))
    bibtex = Column(String)
    style = Column(String, default="ieee")  # ieee, apa, mla

    # Relationship with Paper
    paper = relationship("Paper", back_populates="citations") 