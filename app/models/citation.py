from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.core.database import Base, paper_citations

class Citation(Base):
    """SQLAlchemy model for citations."""
    __tablename__ = "citations"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    value = Column(String, nullable=False, unique=True)
    bibtex = Column(String)
    style = Column(String, default="ieee")  # ieee, apa, mla
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with papers
    papers = relationship("Paper", secondary=paper_citations, back_populates="citations") 