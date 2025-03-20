from typing import List, Dict
from sqlalchemy.orm import Session
from core.database import DBPaper

class CitationService:
    def __init__(self):
        """Initialize the citation service."""
        self.citation_styles = {
            "ieee": self._format_ieee,
            "apa": self._format_apa,
            "mla": self._format_mla
        }
    
    async def format_citations(
        self,
        paper_ids: List[str],
        style: str,
        db: Session
    ) -> List[str]:
        """Format citations for the specified papers in the requested style."""
        # Fetch papers from database
        papers = db.query(DBPaper).filter(DBPaper.id.in_(paper_ids)).all()
        if not papers:
            raise ValueError("No papers found with the provided IDs")
        
        # Get the citation formatter for the requested style
        formatter = self.citation_styles.get(style.lower())
        if not formatter:
            raise ValueError(f"Unsupported citation style: {style}")
        
        # Format citations for each paper
        citations = []
        for paper in papers:
            citation = formatter(paper)
            citations.append(citation)
        
        return citations
    
    def _format_ieee(self, paper: DBPaper) -> str:
        """Format citation in IEEE style."""
        authors = [author['name'] for author in paper.authors]
        if len(authors) > 6:
            authors = authors[:6] + ["et al."]
        
        author_str = ", ".join(authors)
        year = paper.publication_date.year if paper.publication_date else "n.d."
        
        citation = f"{author_str}, \"{paper.title},\""
        if paper.journal:
            citation += f" {paper.journal},"
        if paper.doi:
            citation += f" doi: {paper.doi},"
        citation += f" {year}."
        
        return citation
    
    def _format_apa(self, paper: DBPaper) -> str:
        """Format citation in APA style."""
        authors = [author['name'] for author in paper.authors]
        if len(authors) > 20:
            authors = authors[:19] + ["..."]
        
        if len(authors) == 1:
            author_str = authors[0]
        elif len(authors) == 2:
            author_str = f"{authors[0]} & {authors[1]}"
        else:
            author_str = f"{authors[0]} et al."
        
        year = paper.publication_date.year if paper.publication_date else "n.d."
        
        citation = f"{author_str} ({year}). {paper.title}."
        if paper.journal:
            citation += f" {paper.journal}."
        if paper.doi:
            citation += f" https://doi.org/{paper.doi}"
        
        return citation
    
    def _format_mla(self, paper: DBPaper) -> str:
        """Format citation in MLA style."""
        authors = [author['name'] for author in paper.authors]
        if len(authors) > 3:
            authors = authors[:3] + ["et al."]
        
        author_str = ", ".join(authors)
        year = paper.publication_date.year if paper.publication_date else "n.d."
        
        citation = f"{author_str}. \"{paper.title}.\""
        if paper.journal:
            citation += f" {paper.journal},"
        citation += f" {year}."
        if paper.doi:
            citation += f" doi: {paper.doi}."
        
        return citation 