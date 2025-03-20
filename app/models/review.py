from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4

class Section(BaseModel):
    title: str
    content: str
    subsections: List['Section'] = []
    citations: List[str] = []

class Review(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    abstract: str
    introduction: Section
    methodology: Section
    results: Section
    discussion: Section
    conclusion: Section
    references: List[str]
    generated_date: datetime = Field(default_factory=datetime.now)
    topic: str
    paper_ids: List[str]
    citation_style: str = "ieee"
    word_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Recent Advances in Deep Learning: A State-of-the-Art Review",
                "abstract": "This review synthesizes recent developments in deep learning...",
                "introduction": {
                    "title": "Introduction",
                    "content": "Deep learning has revolutionized artificial intelligence...",
                    "citations": ["doe2024deep", "smith2023neural"]
                },
                "topic": "deep learning advances",
                "citation_style": "ieee",
                "word_count": 5000
            }
        } 