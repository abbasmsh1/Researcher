from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session

from app.core.paper_processor import PaperProcessor
from app.core.review_generator import ReviewGenerator
from app.services.citation_service import CitationService
from app.models.paper import Paper
from app.models.review import Review
from app.core.database import get_db, init_db

app = FastAPI(
    title="AI Academic Writing Agent",
    description="An AI-powered system for generating state-of-the-art academic reviews",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    db: Session = Depends(get_db)
):
    """
    Process an uploaded research paper and extract its content.
    """
    try:
        content = await file.read()
        paper = await paper_processor.process(content, file.filename, db)
        return {"paper_id": paper.id, "title": paper.title}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/generate-review")
async def generate_review(
    request: ReviewRequest,
    db: Session = Depends(get_db)
):
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

@app.get("/api/citations/{style}")
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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 