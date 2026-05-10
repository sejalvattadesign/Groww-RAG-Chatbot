import sys
import os

# Ensure the root of the project is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.pipeline.config import TARGET_URLS
from backend.pipeline.ingestion import MutualFundScraper
from backend.pipeline.cleaner import DocumentCleaner
from backend.database.vector_store import MutualFundVectorStore

def run_pipeline():
    print("=== Starting Mutual Fund Data Ingestion Pipeline ===")
    
    # 1. Scrape Documents (Phase 1.2)
    print("\n[1/3] Scraping URLs using Playwright...")
    scraper = MutualFundScraper(urls=TARGET_URLS)
    raw_docs = scraper.load_documents()
    
    # 2. Clean and Chunk Documents (Phase 1.3)
    print("\n[2/3] Cleaning and Chunking text...")
    cleaner = DocumentCleaner()
    cleaned_chunks = cleaner.clean_and_chunk(raw_docs)
    
    # 3. Embed and Store in ChromaDB (Phase 2)
    print("\n[3/3] Embedding chunks and storing in Vector Database...")
    vector_store = MutualFundVectorStore()
    vector_store.add_documents(cleaned_chunks)
    
    print("\n=== Pipeline Complete! ===")
    print(f"Your data is now stored locally in the 'chroma_db' folder.")

if __name__ == "__main__":
    run_pipeline()
