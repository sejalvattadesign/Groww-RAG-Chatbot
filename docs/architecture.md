# Phase-Wise Architecture: Mutual Fund FAQ Assistant

This document outlines the detailed, phase-wise architectural design for the Mutual Fund FAQ Assistant based on the provided problem statement. It utilizes a Retrieval-Augmented Generation (RAG) approach to ensure fact-based, accurate, and compliant responses.

## Phase 1: Data Acquisition & Processing Pipeline
**Objective:** Identify, extract, and clean official source documents.

*   **1.1 Data Source Definition:**
    *   **Scope:** Select 1 AMC and 3-5 diverse schemes (e.g., Large-cap, Flexi-cap, ELSS).
    *   **URLs:** Target 15-25 official public URLs (Factsheets, KIM, SID, AMFI/SEBI guidance). Use the following URLs for this project:
        *   https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth 
        *   https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth 
        *   https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth 
        *   https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth 
        *   https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth
*   **1.2 Ingestion Engine:**
    *   **Web Scraper/Loader:** Implemented using LangChain's `PlaywrightURLLoader` to execute JavaScript and extract raw text from Groww's dynamic Single Page Applications (SPAs). Extraneous selectors (`nav`, `footer`, `script`, `style`, `noscript`, `iframe`, `svg`) are removed during extraction.
    *   **Metadata Tagging:** Each document is tagged with essential metadata: `source_url`, `doc_type` (`scheme_web_page`), `scheme_name` (extracted from URL slug), `last_updated_date`, and `amc`.
*   **1.3 Data Cleaning & Chunking:**
    *   **Cleaning:** Raw text is cleaned using Regex to remove excessive newlines/spaces and filter out standard mutual fund disclaimers.
    *   **Chunking Strategy:** Implemented `RecursiveCharacterTextSplitter` with a chunk size of 800 characters and a chunk overlap of 150 characters to preserve the semantic meaning of the financial data while optimizing for vector storage.
*   **1.4 Automated Data Refresh (Scheduling):**
    *   **Scheduler:** Utilize **GitHub Actions** (via cron triggers) to automatically run the scraping, cleaning, and embedding pipeline on a predefined schedule (e.g., daily or weekly).
    *   **Sync:** This ensures the Vector DB is continuously kept up-to-date with the latest NAV, AUM, and fee structures without requiring manual intervention.

## Phase 2: Vector Database & Knowledge Base Setup
**Objective:** Convert text chunks into searchable vector representations.

*   **2.1 Embedding Model:**
    *   Utilize `BAAI/bge-small-en-v1.5` (or similar) as the open-source embedding model. It is highly efficient (384 dimensions) and perfectly capable of handling the semantic retrieval of financial terms for a small-to-medium sized dataset.
*   **2.2 Vector Store:**
    *   Deploy a lightweight Vector Database in ChromaDB
    *   Store the generated embeddings alongside the metadata (URL, dates) for citation retrieval.

## Phase 3: Query Processing & Guardrails (Refusal System)
**Objective:** Intercept user queries to enforce compliance and security before hitting the core RAG pipeline.

*   **3.1 PII & Security Filter:**
    *   Scan incoming queries using regex or a lightweight NER model (e.g., Presidio) to block PAN, Aadhaar, account numbers, OTPs, emails, and phone numbers.
    *   **Action on PII:** If personal information is detected, immediately refuse the query *without attaching any URLs*.
*   **3.2 Intent Detection & Guardrails (The Refusal Layer):**
    *   **Classifier:** Implement an LLM-based or rule-based classifier to categorize queries into:
        1.  *Factual* (Proceed to RAG).
        2.  *Advisory/Comparative/Speculative* (e.g., "Should I invest?", "Which is better?").
        3.  *Performance-based* (e.g., "What are the returns?").
    *   **Handling Non-Factual:** Immediately return a canned, polite refusal response reinforcing the "facts-only" rule, accompanied by an educational AMFI/SEBI link.
    *   **Handling Performance:** Return a direct link to the official factsheet without calculating or stating returns.

## Phase 4: Retrieval-Augmented Generation (RAG) Core
**Objective:** Fetch relevant facts and generate a strictly formatted answer.

*   **4.1 Semantic Retrieval:**
    *   **Self-Querying Retriever:** First, extract the specific `scheme_name` from the user's query to apply a strict metadata pre-filter on the Vector Database. This prevents cross-fund data contamination.
    *   **Maximal Marginal Relevance (MMR):** Perform the similarity search using MMR (e.g., fetch top 10 chunks, return the 3-4 most diverse) to ensure broad context and prevent repetitive boilerplate text from dominating the results.
*   **4.2 Context Assembly:**
    *   Retrieve the most relevant text chunks and their associated metadata (`source_url`, `last_updated_date`).
*   **4.3 LLM Generation Prompt:**
    *   **System Prompt:** Instruct the LLM (hosted via **Groq** for ultra-fast inference, e.g., Llama 3) to act as a strict factual assistant.
    *   **Constraints Enforced in Prompt:**
        *   Use *only* the provided context. Do not use prior knowledge.
        *   Limit the response to a maximum of 3 sentences.
        *   Do not provide any investment advice.
*   **4.4 Post-Processing (Formatting):**
    *   Append exactly one primary citation link derived from the retrieved metadata *only if* the LLM successfully answers the question.
    *   **Unknown Answers:** If the LLM does not know the answer or the context is insufficient, politely state so and *do not attach any URLs*.
    *   Append the footer: `"Last updated from sources: <date>"`.

## Phase 5: Application Layer & User Interface
**Objective:** Build a minimal, compliant user interface and backend API.

*   **5.1 Backend API:**
    *   Framework: FastAPI or Flask (Python) or Express (Node.js).
    *   Endpoints: `/api/query` (handles RAG and guardrails), `/api/health`.
*   **5.2 Frontend UI:**
    *   Framework: **Next.js** (React) utilizing a premium, responsive, and dynamic UI design.
    *   **UI Components:**
        *   Welcome message.
        *   Three clickable example questions (e.g., "What is the exit load for [Scheme]?", "What is the minimum SIP amount?").
        *   Chat interface.
        *   Persistent Disclaimer Snippet prominently displayed: `"Facts-only. No investment advice."`

## Phase 6: Testing & Deployment
**Objective:** Validate against success criteria and deploy the solution.

*   **6.1 Quality Assurance (Evaluation):**
    *   Test standard factual queries for accuracy and 3-sentence limits.
    *   Test edge cases (advisory queries, PII inclusion) to ensure the guardrails correctly refuse and sanitize inputs.
    *   Verify citation formatting and valid URLs.
*   **6.2 Deployment:**
    *   Host the backend and vector store on a cloud provider (e.g., AWS, Render, Vercel, or Heroku).
    *   Ensure secure environment variables for API keys and database connections.
    *   No persistent storage of user chat logs containing personal data.

---
### System Architecture Diagram Summary
`User -> Frontend UI -> Guardrails (PII/Intent) -> [If Advisory: Return Refusal] -> [If Factual: Proceed] -> Vector Search -> LLM Generation (with Constraints) -> Post-Processor (Add Links/Footer) -> Frontend UI`
