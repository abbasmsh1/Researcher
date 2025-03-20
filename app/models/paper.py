from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class Author(BaseModel):
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None

class Paper(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    authors: List[Author]
    abstract: str
    content: str
    doi: Optional[str] = None
    url: Optional[str] = None
    publication_date: Optional[datetime] = None
    journal: Optional[str] = None
    keywords: List[str] = []
    references: List[str] = []
    citations: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Deep Learning: A Comprehensive Survey",
                "authors": [
                    {
                        "name": "Abbas Mustafa",
                        "affiliation": "IMT Atlantique",
                        "email": "abbasmsh1@gmail.com"
                    }
                ],
                "abstract": "This paper provides a comprehensive survey of deep learning techniques...",
                "doi": "10.1234/example.2024",
                "keywords": ["deep learning", "artificial intelligence", "neural networks"]
            }
        } 