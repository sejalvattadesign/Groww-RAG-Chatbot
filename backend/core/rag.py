import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from backend.database.vector_store import MutualFundVectorStore

# Load environment variables (like GROQ_API_KEY)
load_dotenv()

class MutualFundRAG:
    """
    Phase 4: Retrieval-Augmented Generation (RAG) Core
    Orchestrates the retrieval and factual response generation using Groq.
    """
    
    def __init__(self):
        # Initialize Groq LLM (Llama 3 8B is ultra-fast and capable for fact extraction)
        self.llm = ChatGroq(
            temperature=0.0, # Strictly factual, 0 hallucination tolerance
            model_name="llama-3.1-8b-instant", 
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Initialize Vector Store
        self.vector_store = MutualFundVectorStore()
        
        # Phase 4.3: Define strict System Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a strictly factual Mutual Fund FAQ Assistant.
Your sole purpose is to answer user queries using ONLY the provided context.

CONSTRAINTS:
1. You must use ONLY the provided context. Do NOT use prior knowledge.
2. If the context does not contain the answer, politely state that you do not have the information. Do not guess.
3. Limit your response to a maximum of 3 sentences.
4. Do not provide any investment advice or recommendations.

CONTEXT:
{context}
"""),
            ("human", "{question}")
        ])
        
        self.output_parser = StrOutputParser()
        
    def _extract_scheme_name(self, query: str) -> str:
        """
        Phase 4.1 Helper: Self-Querying Strategy
        Extracts the mutual fund scheme name from the query to use as a metadata filter.
        (In production, this could be a dedicated LLM call; here we use robust keyword matching for speed)
        """
        query_lower = query.lower()
        
        # Mapping common user phrases to the exact scheme_name metadata tagged in Phase 1
        schemes = {
            "mid cap": "Hdfc Mid Cap Fund Direct Growth",
            "equity": "Hdfc Equity Fund Direct Growth",
            "focused": "Hdfc Focused Fund Direct Growth",
            "elss": "Hdfc Elss Tax Saver Fund Direct Plan Growth",
            "tax saver": "Hdfc Elss Tax Saver Fund Direct Plan Growth",
            "large cap": "Hdfc Large Cap Fund Direct Growth"
        }
        
        for key, exact_name in schemes.items():
            if key in query_lower:
                return exact_name
        return None

    def _format_docs(self, docs):
        """
        Phase 4.2: Context Assembly
        Formats the retrieved documents into a single string for the LLM.
        """
        formatted_context = []
        for d in docs:
            # We inject the content, source, and date directly into the context window
            formatted_context.append(f"Content: {d.page_content}\nSource: {d.metadata.get('source_url', 'Unknown')}\nDate: {d.metadata.get('last_updated_date', 'Unknown')}")
        return "\n\n".join(formatted_context)

    def generate_answer(self, query: str) -> str:
        """
        Main execution pipeline for Phase 4.
        """
        # Step 1: Self-Querying / Metadata Extraction
        scheme_filter = self._extract_scheme_name(query)
        metadata_filter = {"scheme_name": scheme_filter} if scheme_filter else None
        
        # Step 2: Retrieval (using MMR as configured in Phase 2)
        retriever = self.vector_store.get_retriever(metadata_filter=metadata_filter)
        retrieved_docs = retriever.invoke(query)
        
        # Check for empty retrieval
        if not retrieved_docs:
            return "I do not have the information required to answer this question."

        # Step 3: LLM Generation
        chain = (
            {"context": lambda x: self._format_docs(retrieved_docs), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | self.output_parser
        )
        
        llm_response = chain.invoke(query)
        
        # Step 4: Post-Processing (Phase 4.4)
        # Check if the LLM refused to answer due to missing context or is providing general info
        refusal_phrases = ["do not have", "don't have", "cannot answer", "does not contain", "is not mentioned", "no information", "i am a mutual fund faq assistant"]
        is_general_or_unknown = any(phrase in llm_response.lower() for phrase in refusal_phrases)

        
        latest_date = retrieved_docs[0].metadata.get('last_updated_date', 'Unknown Date')
        primary_url = retrieved_docs[0].metadata.get('source_url', 'Unknown URL')
        
        # Return structured data for the UI
        return {
            "answer": llm_response,
            "source_url": primary_url if not is_general_or_unknown else None,
            "last_updated": latest_date if not is_general_or_unknown else None
        }

# Example Usage
if __name__ == "__main__":
    rag = MutualFundRAG()
    
    # This requires a valid GROQ_API_KEY in the .env file and populated ChromaDB to run successfully
    test_q = "What is the exit load for the HDFC Mid Cap fund?"
    print(f"Query: {test_q}")
    try:
        ans = rag.generate_answer(test_q)
        print(f"\nResponse:\n{ans}")
    except Exception as e:
        print(f"\nError (Likely missing API key or empty Vector DB): {e}")
