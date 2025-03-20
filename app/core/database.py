import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Get database path from environment variable or use default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./papers.db")

# Create a single Base instance
Base = declarative_base()

# Create engine and session factory
try:
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
except Exception as e:
    print(f"Error initializing database: {e}")
    raise

async def get_db():
    """Get database session with error handling"""
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        print(f"Error getting database session: {e}")
        raise

async def init_db():
    """Create tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Association tables for many-to-many relationships
paper_keywords = Table(
    'paper_keywords',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('keyword_id', String, ForeignKey('keywords.id'))
)

paper_references = Table(
    'paper_references',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('reference_id', String, ForeignKey('references.id'))
)

paper_citations = Table(
    'paper_citations',
    Base.metadata,
    Column('paper_id', String, ForeignKey('papers.id')),
    Column('citation_id', String, ForeignKey('citations.id'))
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

class Keyword(Base):
    """SQLAlchemy model for keywords."""
    __tablename__ = "keywords"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = Column(String, nullable=False, unique=True)

class Reference(Base):
    """SQLAlchemy model for references."""
    __tablename__ = "references"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = Column(String, nullable=False, unique=True)

class Citation(Base):
    """SQLAlchemy model for citations."""
    __tablename__ = "citations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    value = Column(String, nullable=False, unique=True) 