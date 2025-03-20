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