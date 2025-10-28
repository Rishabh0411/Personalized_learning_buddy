"""
RAG Pipeline - Person 1's Component
Handles document processing, embedding creation, and retrieval
"""

import os
import pickle
from typing import List, Optional
import PyPDF2
import docx
import pdfplumber
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class RAGPipeline:
    """
    Retrieval-Augmented Generation Pipeline
    Processes documents, creates embeddings, and retrieves relevant content
    """
    
    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG pipeline with embedding model
        
        Args:
            embedding_model_name: Name of the sentence transformer model
        """
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        self.index = None
        self.documents = []
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            # Try with pdfplumber first (better for complex PDFs)
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber failed, trying PyPDF2: {e}")
            # Fallback to PyPDF2
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Error extracting PDF with PyPDF2: {e}")
        
        return text.strip()
    
    def extract_text_from_docx(self, docx_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error reading TXT file: {e}")
            return ""
    
    def process_document(self, file_path: str) -> List[Document]:
        """
        Process uploaded document and split into chunks
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of Document objects with text chunks
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Extract text based on file type
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            text = self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        if not text:
            raise ValueError("No text could be extracted from the document")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects
        documents = [
            Document(page_content=chunk, metadata={"source": file_path, "chunk_id": i})
            for i, chunk in enumerate(chunks)
        ]
        
        return documents
    
    def create_embeddings(self, documents: List[Document]) -> np.ndarray:
        """
        Create embeddings for document chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            Numpy array of embeddings
        """
        texts = [doc.page_content for doc in documents]
        embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
        return embeddings
    
    def build_index(self, documents: List[Document]):
        """
        Build FAISS index from documents
        
        Args:
            documents: List of Document objects
        """
        self.documents.extend(documents)
        embeddings = self.create_embeddings(documents)
        
        if self.index is None:
            # Create new index
            self.index = faiss.IndexFlatL2(self.embedding_dim)
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve most relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            
        Returns:
            List of most relevant Document objects
        """
        if self.index is None or len(self.documents) == 0:
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Get relevant documents
        relevant_docs = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        
        return relevant_docs
    
    def save_vectorstore(self, save_path: str = "embeddings/vectorstore.pkl"):
        """Save the vector store to disk"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        data = {
            'index': faiss.serialize_index(self.index) if self.index else None,
            'documents': self.documents
        }
        
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Vector store saved to {save_path}")
    
    def load_vectorstore(self, load_path: str = "embeddings/vectorstore.pkl"):
        """Load the vector store from disk"""
        if not os.path.exists(load_path):
            print(f"No vector store found at {load_path}")
            return False
        
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
        
        if data['index']:
            self.index = faiss.deserialize_index(data['index'])
        self.documents = data['documents']
        
        print(f"Vector store loaded from {load_path}")
        return True
    
    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        """
        Get concatenated context from retrieved documents
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            Concatenated text from relevant documents
        """
        relevant_docs = self.retrieve(query, top_k)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        return context


# Test function
if __name__ == "__main__":
    # Example usage
    rag = RAGPipeline()
    
    # Test with a sample document
    print("RAG Pipeline initialized successfully!")
    print(f"Embedding dimension: {rag.embedding_dim}")
