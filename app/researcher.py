import os
from typing import List, Dict
from langchain.llms import Together
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import docx

class AcademicResearcher:
    def __init__(self):
        self.llm = Together(
            model=os.getenv("MODEL_NAME"),
            temperature=0.7,
            max_tokens=2048,
            together_api_key=os.getenv("TOGETHER_API_KEY")
        )
        self.embeddings = HuggingFaceEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.vector_store = None

    def process_document(self, file_path: str) -> List[Document]:
        """Process uploaded document and return chunks"""
        text = ""
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as file:
                pdf = PdfReader(file)
                for page in pdf.pages:
                    text += page.extract_text()
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

        documents = self.text_splitter.create_documents([text])
        return documents

    def add_documents(self, documents: List[Document]):
        """Add documents to the vector store"""
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)

    def generate_paper(self, topic: str, keywords: List[str], focus_points: List[str]) -> str:
        """Generate IEEE style paper based on the provided parameters"""
        if not self.vector_store:
            return "No documents have been uploaded for reference."

        paper_template = """
        Write an IEEE style research paper on the topic: {topic}
        
        Consider the following keywords: {keywords}
        Focus on these points: {focus_points}
        
        Use the following relevant information from the source documents:
        {context}
        
        The paper should include:
        1. Abstract
        2. Introduction
        3. Literature Review
        4. Methodology
        5. Results and Discussion
        6. Conclusion
        7. References
        
        Ensure proper citations and maintain academic writing standards.
        """

        prompt = PromptTemplate(
            template=paper_template,
            input_variables=["topic", "keywords", "focus_points", "context"]
        )

        # Retrieve relevant context from vector store
        relevant_docs = self.vector_store.similarity_search(
            f"{topic} {' '.join(keywords)} {' '.join(focus_points)}",
            k=5
        )
        context = "\n".join([doc.page_content for doc in relevant_docs])

        chain = LLMChain(llm=self.llm, prompt=prompt)
        paper = chain.run(
            topic=topic,
            keywords=", ".join(keywords),
            focus_points=", ".join(focus_points),
            context=context
        )
        return paper

    def summarize_paper(self, file_path: str) -> Dict[str, str]:
        """Summarize a paper and extract main points"""
        documents = self.process_document(file_path)
        text = " ".join([doc.page_content for doc in documents])

        summary_template = """
        Please provide a comprehensive summary of the following academic paper:
        {text}
        
        Include:
        1. Main objective
        2. Key findings
        3. Methodology
        4. Conclusions
        5. Important points for quick understanding
        """

        prompt = PromptTemplate(
            template=summary_template,
            input_variables=["text"]
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        summary = chain.run(text=text)

        return {
            "summary": summary,
            "full_text": text
        } 