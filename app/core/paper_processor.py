import fitz  # PyMuPDF
import pdfplumber
from typing import List, Tuple, Optional
import re
from datetime import datetime
import spacy
from transformers import pipeline
from sqlalchemy.orm import Session

from app.models.paper import Paper, Author
from app.core.database import DBPaper

class PaperProcessor:
    def __init__(self):
        """Initialize the paper processor with required models and tools."""
        # Load spaCy model for NER and text processing
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize the summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
    async def process(self, content: bytes, filename: str, db: Session) -> Paper:
        """Process a PDF paper and extract structured information."""
        # Extract text using both PyMuPDF and PDFPlumber for robustness
        text = await self._extract_text(content)
        
        # Extract metadata
        title = await self._extract_title(text)
        authors = await self._extract_authors(text)
        abstract = await self._extract_abstract(text)
        doi = await self._extract_doi(text)
        
        # Extract references
        references = await self._extract_references(text)
        
        # Extract keywords
        keywords = await self._extract_keywords(text)
        
        # Create database record
        db_paper = DBPaper(
            title=title,
            authors=[author.dict() for author in authors],
            abstract=abstract,
            content=text,
            doi=doi,
            keywords=keywords,
            references=references
        )
        
        # Save to database
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        
        # Convert to Pydantic model for response
        return Paper(
            id=db_paper.id,
            title=db_paper.title,
            authors=[Author(**author) for author in db_paper.authors],
            abstract=db_paper.abstract,
            content=db_paper.content,
            doi=db_paper.doi,
            keywords=db_paper.keywords,
            references=db_paper.references
        )
    
    async def _extract_text(self, content: bytes) -> str:
        """Extract text from PDF using multiple libraries for better accuracy."""
        text_mupdf = ""
        text_plumber = ""
        
        # PyMuPDF extraction
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            text_mupdf = " ".join([page.get_text() for page in doc])
        except Exception as e:
            print(f"PyMuPDF extraction failed: {str(e)}")
        
        # PDFPlumber extraction
        try:
            with pdfplumber.open(content) as pdf:
                text_plumber = " ".join([page.extract_text() or "" for page in pdf.pages])
        except Exception as e:
            print(f"PDFPlumber extraction failed: {str(e)}")
        
        # Use the better quality text or combine them
        return text_mupdf if len(text_mupdf) > len(text_plumber) else text_plumber
    
    async def _extract_title(self, text: str) -> str:
        """Extract the paper title using heuristics and NLP."""
        # Get the first few lines
        lines = text.split("\n")[:10]
        
        # Look for the longest line in the first few lines that doesn't look like author names
        title_candidates = [
            line.strip() for line in lines
            if len(line.strip()) > 20
            and not re.search(r"@|University|Institute|Abstract", line)
        ]
        
        return title_candidates[0] if title_candidates else "Untitled Paper"
    
    async def _extract_authors(self, text: str) -> List[Author]:
        """Extract author information using NLP and pattern matching."""
        authors = []
        # Get text before abstract
        pre_abstract = text.split("Abstract")[0] if "Abstract" in text else text[:1000]
        
        # Use spaCy to identify person names
        doc = self.nlp(pre_abstract)
        person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Extract emails and affiliations using regex
        email_pattern = r'[\w\.-]+@[\w\.-]+'
        emails = re.findall(email_pattern, pre_abstract)
        
        # Create Author objects
        for i, name in enumerate(person_names):
            email = emails[i] if i < len(emails) else None
            authors.append(Author(name=name, email=email))
        
        return authors
    
    async def _extract_abstract(self, text: str) -> str:
        """Extract the abstract section from the paper."""
        # Look for abstract section
        abstract_match = re.search(r"Abstract[:\s]+(.*?)(?=\n\n|\d\.|\bIntroduction\b)", 
                                 text, re.DOTALL | re.IGNORECASE)
        
        if abstract_match:
            return abstract_match.group(1).strip()
        
        # If no abstract found, use the summarizer to generate one
        return self.summarizer(text[:1000], 
                             max_length=150, 
                             min_length=50, 
                             do_sample=False)[0]['summary_text']
    
    async def _extract_doi(self, text: str) -> Optional[str]:
        """Extract DOI from the paper text."""
        doi_pattern = r"10.\d{4,9}/[-._;()/:\w]+"
        doi_match = re.search(doi_pattern, text)
        return doi_match.group(0) if doi_match else None
    
    async def _extract_references(self, text: str) -> List[str]:
        """Extract references from the paper."""
        # Look for references section
        references_section = re.split(r"References|Bibliography", text)[-1]
        
        # Split into individual references
        references = []
        for line in references_section.split("\n"):
            if re.match(r"^\[\d+\]|^\d+\.", line.strip()):
                references.append(line.strip())
        
        return references
    
    async def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from the paper."""
        # Look for keywords section
        keywords_match = re.search(r"Keywords?[:\s]+(.*?)(?=\n\n)", text, re.IGNORECASE)
        if keywords_match:
            keywords_text = keywords_match.group(1)
            return [k.strip() for k in keywords_text.split(",")]
        
        # If no keywords section, extract key phrases using NLP
        doc = self.nlp(text[:2000])  # Process first 2000 chars
        return [chunk.text for chunk in doc.noun_chunks][:5]  # Return top 5 noun phrases 