import datetime
from typing import List, Dict, Any
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

from backend.pipeline.config import TARGET_URLS, DATA_SOURCE_CONFIG

class MutualFundScraper:
    """
    Ingestion Engine for Phase 1.2
    Responsible for scraping dynamic web pages and tagging them with metadata.
    """
    
    def __init__(self, urls: List[str]):
        self.urls = urls

    def extract_metadata(self, url: str) -> Dict[str, str]:
        """
        Extract metadata from the given URL based on the URL structure.
        """
        # Example URL: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
        scheme_slug = url.split('/')[-1]
        scheme_name = scheme_slug.replace('-', ' ').title()
        
        return {
            "source_url": url,
            "doc_type": "scheme_web_page",
            "scheme_name": scheme_name,
            "last_updated_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "amc": DATA_SOURCE_CONFIG["amc"]
        }

    def load_documents(self) -> List[Any]:
        """
        Scrape dynamic web pages using PlaywrightURLLoader.
        Returns a list of LangChain Document objects with attached metadata.
        """
        print(f"Starting to load {len(self.urls)} URLs using Playwright (AsyncChromium)...")
        
        # We use AsyncChromiumLoader because Groww is a dynamic SPA
        loader = AsyncChromiumLoader(self.urls)
        docs = loader.load()
        
        # Use BeautifulSoupTransformer to clean standard boilerplate selectors
        bs_transformer = BeautifulSoupTransformer()
        docs_transformed = bs_transformer.transform_documents(
            docs,
            unnecessary_lines_from_tags=["nav", "footer", "script", "style", "noscript", "iframe", "svg"]
        )
        
        # Tag each document with essential metadata
        for doc in docs_transformed:
            source_url = doc.metadata.get("source")
            if source_url:
                metadata = self.extract_metadata(source_url)
                doc.metadata.update(metadata)
                
        print(f"Successfully loaded and tagged {len(docs_transformed)} documents.")
        return docs_transformed

# Example usage for testing
if __name__ == "__main__":
    scraper = MutualFundScraper(TARGET_URLS)
    docs = scraper.load_documents()
    for d in docs:
        print(f"---")
        print(f"Scheme: {d.metadata.get('scheme_name')}")
        print(f"Source: {d.metadata.get('source_url')}")
        print(f"Metadata: {d.metadata}")
        print(f"Content Length: {len(d.page_content)} characters")
