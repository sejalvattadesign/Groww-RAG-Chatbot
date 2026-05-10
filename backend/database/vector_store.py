import os
from typing import List, Any
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# Define the persistent directory for ChromaDB locally
CHROMA_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "chroma_db")

class MutualFundVectorStore:
    """
    Phase 2: Vector Database & Knowledge Base Setup.
    Handles embedding and storage of cleaned document chunks.
    """
    def __init__(self, collection_name: str = "mutual_funds"):
        self.collection_name = collection_name
        
        # Phase 2.1: Initialize the BAAI/bge-small-en-v1.5 embedding model
        model_name = "BAAI/bge-small-en-v1.5"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': True} # True to enable cosine similarity optimization
        
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        
        # Phase 2.2: Initialize ChromaDB
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DB_DIR
        )

    def add_documents(self, chunks: List[Any], clear_existing: bool = True):
        """
        Add document chunks to the Vector Store.
        :param clear_existing: If True, clears the existing database before adding new data.
        """
        if clear_existing:
            print("Refreshing database: Clearing existing chunks...")
            # We delete the collection and re-initialize it to ensure a clean state
            self.vector_store.delete_collection()
            self.vector_store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_DB_DIR
            )
            
        print(f"Adding {len(chunks)} chunks to ChromaDB...")
        self.vector_store.add_documents(documents=chunks)
        print("Successfully added chunks and persisted database.")


    def get_retriever(self, search_type: str = "mmr", k: int = 4, fetch_k: int = 15, metadata_filter: dict = None):
        """
        Phase 4.1 Implementation: Returns a retriever configured with MMR.
        Can accept metadata_filter for Self-Querying retrieval (e.g., {"scheme_name": "Hdfc Mid Cap Fund Direct Growth"}).
        """
        search_kwargs = {"k": k, "fetch_k": fetch_k}
        
        # Apply strict metadata filtering if provided
        if metadata_filter:
            search_kwargs["filter"] = metadata_filter
            
        return self.vector_store.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs
        )

# Example usage for testing
if __name__ == "__main__":
    print("Initializing Vector Store and downloading embedding model (if not cached)...")
    vs = MutualFundVectorStore()
    print(f"Vector Store successfully initialized at: {CHROMA_DB_DIR}")
