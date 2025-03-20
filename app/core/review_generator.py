from typing import List, Optional
from sqlalchemy.orm import Session
from langchain.llms import Together
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

from models.review import Review, Section
from core.database import DBReview, DBPaper

# Load environment variables
load_dotenv()

class ReviewGenerator:
    def __init__(self):
        """Initialize the review generator with Together AI LLM."""
        self.llm = Together(
            together_api_key=os.getenv("TOGETHER_API_KEY"),
            model="mistralai/Mixtral-8x7B-Instruct-v0.1"
        )
        
        # Define prompts for different sections
        self.intro_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write an introduction for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The introduction should:
            1. Provide background context
            2. Explain the importance of the topic
            3. Outline the structure of the review
            """
        )
        
        self.methodology_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write a methodology section for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The methodology section should:
            1. Explain the review process
            2. Describe the paper selection criteria
            3. Outline the analysis approach
            """
        )
        
        self.results_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write a results section for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The results section should:
            1. Present key findings from the papers
            2. Compare different approaches
            3. Highlight trends and patterns
            """
        )
        
        self.discussion_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write a discussion section for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The discussion section should:
            1. Analyze the implications of findings
            2. Identify challenges and limitations
            3. Suggest future research directions
            """
        )
        
        self.conclusion_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write a conclusion section for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The conclusion should:
            1. Summarize key findings
            2. Highlight contributions
            3. Suggest future directions
            """
        )
    
    async def generate(
        self,
        paper_ids: List[str],
        topic: str,
        max_length: Optional[int] = 3000,
        db: Optional[Session] = None
    ) -> Review:
        """Generate a state-of-the-art review based on the provided papers."""
        # Fetch papers from database
        papers = db.query(DBPaper).filter(DBPaper.id.in_(paper_ids)).all()
        if not papers:
            raise ValueError("No papers found with the provided IDs")
        
        # Prepare paper information for prompts
        papers_info = "\n".join([
            f"- {paper.title} by {', '.join(author['name'] for author in paper.authors)}"
            for paper in papers
        ])
        
        # Generate sections using LLM chains
        intro_chain = LLMChain(llm=self.llm, prompt=self.intro_prompt)
        methodology_chain = LLMChain(llm=self.llm, prompt=self.methodology_prompt)
        results_chain = LLMChain(llm=self.llm, prompt=self.results_prompt)
        discussion_chain = LLMChain(llm=self.llm, prompt=self.discussion_prompt)
        conclusion_chain = LLMChain(llm=self.llm, prompt=self.conclusion_prompt)
        
        # Generate content for each section
        intro_content = await intro_chain.arun(topic=topic, papers=papers_info)
        methodology_content = await methodology_chain.arun(topic=topic, papers=papers_info)
        results_content = await results_chain.arun(topic=topic, papers=papers_info)
        discussion_content = await discussion_chain.arun(topic=topic, papers=papers_info)
        conclusion_content = await conclusion_chain.arun(topic=topic, papers=papers_info)
        
        # Create sections
        sections = [
            Section(title="Introduction", content=intro_content),
            Section(title="Methodology", content=methodology_content),
            Section(title="Results", content=results_content),
            Section(title="Discussion", content=discussion_content),
            Section(title="Conclusion", content=conclusion_content)
        ]
        
        # Generate abstract
        abstract = await self._generate_abstract(topic, papers_info)
        
        # Create database record
        db_review = DBReview(
            title=f"State-of-the-Art Review: {topic}",
            abstract=abstract,
            content=[section.dict() for section in sections],
            references=[paper.doi for paper in papers if paper.doi],
            topic=topic,
            paper_ids=paper_ids,
            word_count=str(sum(len(section.content.split()) for section in sections))
        )
        
        # Save to database
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        # Convert to Pydantic model for response
        return Review(
            id=db_review.id,
            title=db_review.title,
            abstract=db_review.abstract,
            introduction=Section(**db_review.content[0]),
            methodology=Section(**db_review.content[1]),
            results=Section(**db_review.content[2]),
            discussion=Section(**db_review.content[3]),
            conclusion=Section(**db_review.content[4]),
            references=db_review.references,
            generated_date=db_review.generated_date,
            topic=db_review.topic,
            paper_ids=db_review.paper_ids,
            citation_style="ieee",
            word_count=int(db_review.word_count)
        )
    
    async def _generate_abstract(self, topic: str, papers_info: str) -> str:
        """Generate an abstract for the review."""
        abstract_prompt = PromptTemplate(
            input_variables=["topic", "papers"],
            template="""
            Write an abstract for a state-of-the-art review paper on {topic}.
            Use the following papers as references:
            {papers}
            
            The abstract should:
            1. Provide a brief overview of the topic
            2. Explain the purpose of the review
            3. Summarize key findings
            4. Highlight implications
            """
        )
        
        abstract_chain = LLMChain(llm=self.llm, prompt=abstract_prompt)
        return await abstract_chain.arun(topic=topic, papers=papers_info) 