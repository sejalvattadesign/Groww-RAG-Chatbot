import re
from enum import Enum
from typing import Tuple

class QueryIntent(Enum):
    FACTUAL = "Factual"
    ADVISORY = "Advisory/Comparative/Speculative"
    PERFORMANCE = "Performance-based"
    OUT_OF_SCOPE = "Out of Scope"


class GuardrailSystem:
    """
    Phase 3: Query Processing & Guardrails (Refusal System)
    Intercepts user queries to enforce compliance, security, and intent rules.
    """
    
    def __init__(self, llm=None):
        """
        :param llm: An optional LangChain LLM instance to be used for advanced intent classification.
        """
        self.llm = llm
        
        # Phase 3.1: Standard regex patterns for Indian PII detection
        self.pii_patterns = {
            "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
            "Aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
            "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "Phone": r"\b(?:\+?91|0)?[6789]\d{9}\b"
        }

    def check_pii(self, query: str) -> Tuple[bool, str]:
        """
        Phase 3.1: PII & Security Filter.
        Returns (is_blocked, refusal_message).
        """
        for pii_type, pattern in self.pii_patterns.items():
            if re.search(pattern, query, re.IGNORECASE):
                # As per newly added architecture rules: Do not attach any URLs for PII violations.
                msg = (f"Privacy Warning: Your query appears to contain personal information ({pii_type}). "
                       f"For your security, please do not share PAN, Aadhaar, Account Numbers, or contact details. "
                       f"I cannot process this query.")
                return True, msg
        return False, ""

    def detect_intent(self, query: str) -> Tuple[QueryIntent, str]:
        """
        Phase 3.2: Intent Detection.
        Classifies the query. If it's not factual, returns the appropriate refusal.
        """
        # In a production system, this can be offloaded to `self.llm` with a zero-shot classification prompt.
        # Here we simulate the logic with robust rule-based heuristics as a fast fallback.
        query_lower = query.lower()
        
        advisory_keywords = ["should i", "is it good", "better", "recommend", "advice", "buy or sell", "invest in", "worth it", "decide", "choose", "compare", "which one", "pick"]
        performance_keywords = ["returns", "cagr", "how much profit", "yield", "historical return", "performance of"]
        
        # 1. Check Advisory
        if any(kw in query_lower for kw in advisory_keywords):
            msg = ("I can only provide factual information from official documents. "
                   "I cannot provide investment advice, speculative predictions, or comparative recommendations. "
                   "Please consult a registered financial advisor.")
            return QueryIntent.ADVISORY, msg
            
        # 2. Check Performance
        if any(kw in query_lower for kw in performance_keywords):
            msg = ("I cannot state or calculate historical returns or performance data. "
                   "Please refer to the official factsheet of the specific fund for performance figures.")
            return QueryIntent.PERFORMANCE, msg

            
        # 3. Check Scope (Domain Filter)
        # We ensure the query is related to mutual funds or HDFC specifically
        fund_keywords = ["fund", "scheme", "hdfc", "nav", "exit load", "expense", "sip", "investment", "portfolio", "manager", "amc", "mid cap", "large cap", "small cap", "focused", "tax saver", "elss", "folio"]
        if not any(kw in query_lower for kw in fund_keywords):
            msg = ("I am only authorized to answer factual questions about HDFC Mutual Fund schemes. "
                   "I cannot provide information on general market prices, commodities, or non-fund related topics.")
            return QueryIntent.OUT_OF_SCOPE, msg

        # 4. Default to Factual
        return QueryIntent.FACTUAL, ""


    def process_query(self, query: str) -> Tuple[bool, str]:
        """
        Master function to run a query through all guardrails.
        Returns (is_safe_to_proceed, message_or_error)
        """
        # Step 1: PII Check (High Priority)
        is_blocked, pii_msg = self.check_pii(query)
        if is_blocked:
            return False, pii_msg
            
        # Step 2: Intent Check
        intent, intent_msg = self.detect_intent(query)
        if intent != QueryIntent.FACTUAL:
            return False, intent_msg
            
        # Query passed all guardrails
        return True, "Query is safe and factual. Proceeding to RAG retrieval."

# Example Usage
if __name__ == "__main__":
    guardrails = GuardrailSystem()
    
    test_queries = [
        "What is the exit load for HDFC Mid Cap?",
        "My PAN is ABCDE1234F, can you check my portfolio?",
        "Should I invest in HDFC Large Cap right now?",
        "What are the 5 year returns for the ELSS fund?"
    ]
    
    for i, q in enumerate(test_queries, 1):
        print(f"Test {i}: '{q}'")
        is_safe, msg = guardrails.process_query(q)
        print(f" -> Safe to Proceed: {is_safe}")
        print(f" -> Result: {msg}\n")
