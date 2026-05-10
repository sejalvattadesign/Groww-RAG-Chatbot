import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional


# Ensure the root of the project is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.guardrails.guardrails import GuardrailSystem
from backend.core.rag import MutualFundRAG

app = FastAPI(
    title="Mutual Fund FAQ Assistant API",
    description="Backend API for querying mutual fund data with strict factual guardrails.",
    version="1.0.0"
)

# Enable CORS for the Next.js frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow local frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons for the Guardrails and RAG Core
guardrails = GuardrailSystem()
rag_core = MutualFundRAG()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    is_safe: bool
    source_url: Optional[str] = None
    last_updated: Optional[str] = None


@app.get("/api/health")
def health_check():
    """
    Phase 5.1 Endpoint: Health check for infrastructure/deployment.
    """
    return {"status": "healthy", "service": "Mutual Fund FAQ API"}

@app.post("/api/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    """
    Phase 5.1 Endpoint: Main pipeline entry point.
    Runs guardrails -> if safe -> runs RAG core.
    """
    query = request.query
    
    # 1. Run through Phase 3 Guardrails (PII & Intent)
    is_safe, guardrail_message = guardrails.process_query(query)
    
    if not is_safe:
        # Return the polite refusal message (No URLs for PII/unknown as per architecture)
        return QueryResponse(answer=guardrail_message, is_safe=False)
        
    # 2. Run through Phase 4 RAG Core
    try:
        rag_data = rag_core.generate_answer(query)
        return QueryResponse(
            answer=rag_data["answer"], 
            is_safe=True,
            source_url=rag_data.get("source_url"),
            last_updated=rag_data.get("last_updated")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server locally on port 8000
    print("Starting FastAPI Backend on http://localhost:8000 ...")
    uvicorn.run("backend.api:app", host="0.0.0.0", port=8000, reload=True)
