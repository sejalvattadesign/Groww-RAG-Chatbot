import re
from typing import List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentCleaner:
    """
    Data Cleaning & Chunking Engine for Phase 1.3
    Responsible for removing boilerplate text and chunking documents.
    """
    
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Context-aware chunking strategy using LangChain
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def clean_text(self, text: str) -> str:
        """
        Clean raw scraped text by removing excessive whitespace, 
        disclaimers, or irrelevant navigation remnants.
        """
        # Remove excessive newlines and spaces
        cleaned_text = re.sub(r'\n+', '\n', text)
        cleaned_text = re.sub(r' +', ' ', cleaned_text)
        
        # Optional: Remove standard warning text if it creates noise
        disclaimer_pattern = r'Mutual Fund investments are subject to market risks, read all scheme related documents carefully.'
        cleaned_text = re.sub(disclaimer_pattern, '', cleaned_text, flags=re.IGNORECASE)
        
        return cleaned_text.strip()

    def clean_and_chunk(self, documents: List[Any]) -> List[Any]:
        """
        Takes a list of LangChain Document objects, cleans their content,
        and splits them into smaller chunks while preserving metadata.
        """
        cleaned_documents = []
        
        # Step 1: Clean the text
        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)
            cleaned_documents.append(doc)
            
        # Step 2: Split the documents into chunks
        print(f"Splitting {len(cleaned_documents)} documents into chunks...")
        chunked_documents = self.text_splitter.split_documents(cleaned_documents)
        
        print(f"Generated {len(chunked_documents)} chunks from original documents.")
        return chunked_documents

# Example usage for testing
if __name__ == "__main__":
    from src.phase1_data_pipeline.ingestion import MutualFundScraper
    from src.phase1_data_pipeline.config import TARGET_URLS
    
    # Run the full Phase 1 pipeline
    print("Testing Phase 1 Pipeline on a single URL...")
    scraper = MutualFundScraper(TARGET_URLS[:1])  # Test with just 1 URL
    docs = scraper.load_documents()
    
    cleaner = DocumentCleaner()
    chunks = cleaner.clean_and_chunk(docs)
    
    if chunks:
        print(f"\n--- Example Chunk [1/{len(chunks)}] ---")
        print(f"Scheme: {chunks[0].metadata.get('scheme_name')}")
        print(f"Content:\n{chunks[0].page_content}")
        print(f"Metadata: {chunks[0].metadata}")
