from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.core.database import Base, paper_keywords

class Keyword(Base):
    """SQLAlchemy model for keywords."""
    __tablename__ = "keywords"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    value = Column(String, nullable=False, unique=True)

    # Relationship with papers
    papers = relationship("Paper", secondary=paper_keywords, back_populates="keywords") 