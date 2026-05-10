import sys
import os

# Ensure the root of the project is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.phase1_data_pipeline.config import TARGET_URLS
from src.phase1_data_pipeline.ingestion import MutualFundScraper

def test_ingestion():
    # Test with just 1 URL to see metadata
    scraper = MutualFundScraper(urls=TARGET_URLS[:1])
    docs = scraper.load_documents()
    
    if not docs:
        print("No documents loaded!")
        return

    print(f"Loaded {len(docs)} documents.")
    for i, doc in enumerate(docs[:3]):
        print(f"\n--- Document {i} ---")
        print(f"Metadata: {doc.metadata}")
        print(f"Content snippet: {doc.page_content[:200]}")

if __name__ == "__main__":
    test_ingestion()
