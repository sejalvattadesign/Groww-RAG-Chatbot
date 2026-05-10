# Phase 2 Edge Cases: Vector Database & Knowledge Base Setup

This document outlines potential edge cases during the embedding and vector storage phase and proposes mitigation strategies.

## 1. Embedding API Rate Limits
*   **Edge Case:** Processing a large volume of chunks simultaneously hits the rate limits of the embedding provider (e.g., OpenAI).
*   **Mitigation:** Implement robust retry logic with exponential backoff. Batch embedding requests according to the provider's limits.

## 2. Context Loss in Chunking
*   **Edge Case:** A critical piece of information (e.g., "The exit load for Scheme A is 1%") is split across two chunks, leading to poor embedding representation.
*   **Mitigation:** Carefully tune the chunk size and overlap parameters in the `RecursiveCharacterTextSplitter`. Ensure semantic boundaries (like paragraphs or sentences) are respected during splitting.

## 3. Vector Database Connectivity Issues
*   **Edge Case:** The application fails to connect to the hosted Vector Database (e.g., Pinecone or a remote ChromaDB instance) due to network issues.
*   **Mitigation:** Implement connection pooling, health checks, and automatic retries. Ensure the backend degrades gracefully if the vector store is temporarily unavailable.

## 4. Dimensionality Mismatch
*   **Edge Case:** Upgrading to a newer embedding model (e.g., from `text-embedding-ada-002` to `text-embedding-3-small`) results in vectors with different dimensions, breaking the search.
*   **Mitigation:** Plan for model versioning. If upgrading, re-embed the entire corpus into a new index or namespace rather than mixing dimensions in the same index.

## 5. Metadata Filtering Failures
*   **Edge Case:** Searching by metadata (e.g., `scheme_name`) fails due to inconsistent tagging during the ingestion phase.
*   **Mitigation:** Enforce strict schemas for metadata during Phase 1. Use enums or standardized lists for AMC and Scheme names to ensure exact matches during retrieval.
