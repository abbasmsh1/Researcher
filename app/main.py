from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.paper_processor import PaperProcessor
from app.core.review_generator import ReviewGenerator
from app.core.citation_service import CitationService
from app.models.paper import Paper
from app.models.review import Review
from app.models.citation import Citation
from app.core.database import get_db, init_db
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Validate required environment variables
if not os.getenv("TOGETHER_API_KEY"):
    raise ValueError("TOGETHER_API_KEY environment variable is not set")

app = FastAPI(
    title="AI Academic Writing Agent",
    description="An AI-powered system for generating state-of-the-art academic reviews",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
paper_processor = PaperProcessor()
review_generator = ReviewGenerator()
citation_service = CitationService()

# Initialize database
init_db()

class ReviewRequest(BaseModel):
    papers: List[str]  # List of paper IDs or URLs
    topic: str
    max_length: Optional[int] = 3000
    citation_style: Optional[str] = "ieee"

@app.post("/api/process-paper")
async def process_paper(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        paper = await paper_processor.process_paper(file, db)
        return {"message": "Paper processed successfully", "paper_id": paper.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-review/{paper_id}")
async def generate_review(
    paper_id: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        review = await review_generator.generate_review(paper_id, db)
    """
    Generate a state-of-the-art review based on processed papers.
    """
    try:
        review = await review_generator.generate(
            paper_ids=request.papers,
            topic=request.topic,
            max_length=request.max_length,
            db=db
        )
        return review
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@get("/api/citations/{style}")
async def get_citations(
    style: str,
    paper_ids: List[str],
    db: Session = Depends(get_db)
):
    """
    Get formatted citations for the specified papers.
    """
    try:
        citations = await citation_service.format_citations(paper_ids, style, db)
        return {"citations": citations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 