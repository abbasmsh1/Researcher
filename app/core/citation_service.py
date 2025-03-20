from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.models.paper import Paper
from app.models.citation import Citation
from app.core.database import Base

class CitationService:
    def __init__(self):
        self.citation_styles = {
            "ieee": self._format_ieee,
            "apa": self._format_apa,
            "mla": self._format_mla,
            "chicago": self._format_chicago
        }

    async def get_citations(self, paper_id: str, db: AsyncSession) -> List[Dict[str, str]]:
        """Get formatted citations for the specified paper"""
        try:
            # Get paper from database
            paper = await self._get_paper(paper_id, db)
            if not paper:
                raise ValueError(f"Paper with ID {paper_id} not found")

            # Parse citations from paper
            citations = json.loads(paper.citations)

            # Format citations in different styles
            formatted_citations = {}
            for style in self.citation_styles:
                formatted_citations[style] = [
                    self.citation_styles[style](citation)
                    for citation in citations
                ]

            return formatted_citations

        except Exception as e:
            raise Exception(f"Error getting citations: {str(e)}")

    async def _get_paper(self, paper_id: str, db: AsyncSession) -> Paper:
        """Get paper from database"""
        query = select(Paper).where(Paper.id == paper_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    def _format_ieee(self, citation: Dict[str, str]) -> str:
        """Format citation in IEEE style"""
        # Example: [1] J. Doe, "Title of the paper," Journal Name, vol. X, no. Y, pp. Z-ZZ, Year.
        return f"[{citation.get('text', '')}] {citation.get('reference', '')}"

    def _format_apa(self, citation: Dict[str, str]) -> str:
        """Format citation in APA style"""
        # Example: Doe, J. (Year). Title of the paper. Journal Name, X(Y), Z-ZZ.
        return citation.get('reference', '')

    def _format_mla(self, citation: Dict[str, str]) -> str:
        """Format citation in MLA style"""
        # Example: Doe, John. "Title of the Paper." Journal Name, vol. X, no. Y, Year, pp. Z-ZZ.
        return citation.get('reference', '')

    def _format_chicago(self, citation: Dict[str, str]) -> str:
        """Format citation in Chicago style"""
        # Example: Doe, John. "Title of the Paper." Journal Name X, no. Y (Year): Z-ZZ.
        return citation.get('reference', '') 