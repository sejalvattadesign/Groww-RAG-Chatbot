# Mutual Fund FAQ Assistant (Groww-Inspired)

A production-ready, facts-only RAG (Retrieval-Augmented Generation) assistant for HDFC Mutual Fund schemes. Built with a premium Groww-inspired UI, robust financial guardrails, and automated daily data ingestion.

---

## 🚀 Setup Instructions

### 1. Backend Setup (Python)
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/sejalvattadesign/Groww-RAG-Chatbot.git
    cd Groww-RAG-Chatbot
    ```
2.  **Create a Virtual Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Environment Variables**:
    Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=your_gsk_key_here
    ```
5.  **Initialize Database**:
    Run the ingestion script to scrape official data and populate the Vector DB:
    ```bash
    python scripts/ingest_data.py
    ```
6.  **Run Backend Server**:
    ```bash
    python -m backend.api
    ```

### 2. Frontend Setup (Next.js)
1.  **Navigate to frontend**:
    ```bash
    cd frontend
    ```
2.  **Install Packages**:
    ```bash
    npm install
    ```
3.  **Run Dev Server**:
    ```bash
    npm run dev
    ```
4.  **Access the App**: Open [http://localhost:3000](http://localhost:3000)

---

## 🎯 Scope of Knowledge

The assistant is strictly limited to factual data from **HDFC Mutual Fund** and **AMFI India**.

### Supported Schemes:
*   HDFC Mid Cap Fund
*   HDFC Focused Fund
*   HDFC ELSS Tax Saver Fund
*   HDFC Large Cap Fund
*   HDFC Small Cap Fund
*   HDFC Liquid Fund
*   HDFC Multi Cap Fund

### Included Resources:
*   Official HDFC AMC Service FAQs (KYC, FATCA, Nomination)
*   Smart Account Statement download guides
*   AMFI Regulatory Guidance (NAV, Exit Load, SIP basics)

---

## ⚠️ Known Limits & Guardrails

To ensure compliance and user safety, the following strict limits are enforced:

1.  **Facts-Only**: The assistant will only answer based on retrieved official documents. It will refuse to guess or use general knowledge.
2.  **No Investment Advice**: Queries like "Should I invest?" or "Which is better?" are automatically blocked.
3.  **No Performance Data**: The system does not provide CAGR, historical returns, or performance rankings to avoid misleading users.
4.  **No External Links**: For security, the assistant does not provide links to third-party organizations (except official source references).
5.  **PII Filter**: Any query containing PAN, Aadhaar, or contact details is immediately blocked.

---

## 🛠️ Tech Stack
*   **LLM**: Groq (Llama-3.1-8b-instant)
*   **Vector DB**: ChromaDB
*   **Frameworks**: FastAPI (Backend) & Next.js (Frontend)
*   **Automation**: GitHub Actions (Daily Ingestion Scheduler)
