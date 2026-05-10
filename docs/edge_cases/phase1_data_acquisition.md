# Phase 1 Edge Cases: Data Acquisition & Processing Pipeline

This document outlines potential edge cases during the data acquisition and processing phase and proposes mitigation strategies.

## 1. Web Scraping Failures
*   **Edge Case:** Source URLs (e.g., Groww) update their HTML structure, breaking the web scraper's CSS selectors.
*   **Mitigation:** Implement robust error handling and fallback mechanisms. Use resilient selection strategies (e.g., relying on semantic tags or broader content areas) and monitor for sudden drops in extracted text volume.

## 2. Anti-Bot Protection & Rate Limiting
*   **Edge Case:** The source website blocks the scraper with 403 Forbidden errors or CAPTCHAs due to frequent requests.
*   **Mitigation:** Implement exponential backoff, rate limiting on the scraper side, and rotate user agents. Respect the site's `robots.txt` and consider using proxy rotation if necessary.

## 3. PDF Parsing Challenges
*   **Edge Case:** Factsheets or Scheme Information Documents (SIDs) are provided as scanned images rather than text-based PDFs.
*   **Mitigation:** Integrate Optical Character Recognition (OCR) fallback (e.g., Tesseract or AWS Textract) for image-based PDFs.

## 4. Complex Document Structures (Tables & Charts)
*   **Edge Case:** Financial documents heavily rely on tables for performance data and fees, which may be scrambled during text extraction and chunking.
*   **Mitigation:** Use specialized document parsing tools (like Unstructured.io or LLM-based vision models) that can intelligently extract and format table data into Markdown or JSON before chunking.

## 5. Stale or Duplicate Data
*   **Edge Case:** Scraping the same URL multiple times creates duplicate chunks, or an updated document is published but the old one remains in the system.
*   **Mitigation:** Implement a hashing mechanism for document contents to detect changes. Store a "last updated" timestamp and upsert (update/insert) documents based on their unique URL or ID rather than purely appending.
