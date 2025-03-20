from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.sqlite import JSON
import uuid
from datetime import datetime

# Create SQLite engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./researcher.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create declarative base
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Association tables for many-to-many relationships
paper_keywords = Table(
    'paper_keywords',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('keyword', String)
)

paper_references = Table(
    'paper_references',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('reference', String)
)

paper_citations = Table(
    'paper_citations',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('citation', String)
)

# Database models
class DBPaper(Base):
    """SQLAlchemy model for papers."""
    __tablename__ = "papers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)  # Store as JSON
    abstract = Column(String, nullable=False)
    content = Column(String, nullable=False)
    doi = Column(String)
    url = Column(String)
    publication_date = Column(DateTime)
    journal = Column(String)
    
    # Many-to-many relationships
    keywords = relationship("Keyword", secondary=paper_keywords)
    references = relationship("Reference", secondary=paper_references)
    citations = relationship("Citation", secondary=paper_citations)

class DBReview(Base):
    """SQLAlchemy model for reviews."""
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    abstract = Column(String, nullable=False)
    content = Column(JSON, nullable=False)  # Store sections as JSON
    references = Column(JSON)  # Store as JSON
    generated_date = Column(DateTime, default=datetime.utcnow)
    topic = Column(String, nullable=False)
    paper_ids = Column(JSON)  # Store as JSON array
    citation_style = Column(String, default="ieee")
    word_count = Column(String)

# Create all tables
def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine) 