# Phase 3 Edge Cases: Query Processing & Guardrails

This document outlines potential edge cases during the intent detection and security filtering phase and proposes mitigation strategies.

## 1. PII Obfuscation
*   **Edge Case:** A user intentionally obfuscates Personally Identifiable Information (PII) to bypass the regex filters (e.g., typing "P.A.N. is A B C D E 1 2 3 4 F").
*   **Mitigation:** Use a combination of regex patterns and a dedicated Named Entity Recognition (NER) model (like Microsoft Presidio) that is trained to detect variations and obfuscations of sensitive data.

## 2. Disguised Advisory Queries
*   **Edge Case:** A user phrases an advisory question as a factual one to bypass the intent classifier (e.g., "Given the current high exit load of 1%, is it still a good idea to invest in the HDFC Mid-Cap fund?").
*   **Mitigation:** Prompt the LLM intent classifier to be overly cautious with queries containing subjective or future-oriented keywords ("good idea", "should I", "better"). Default to refusal if the intent is ambiguous.

## 3. Ambiguous or Incomplete Queries
*   **Edge Case:** A user asks a vague question without specifying the scheme (e.g., "What is the exit load?").
*   **Mitigation:** The intent classifier should identify missing required entities. The system can return a clarification prompt asking the user to specify the mutual fund scheme they are inquiring about.

## 4. Multi-Intent Queries
*   **Edge Case:** A user asks a combination of factual and advisory questions in a single prompt (e.g., "What is the expense ratio, and based on that, should I buy it?").
*   **Mitigation:** The system should strictly evaluate the entire prompt. If any part of the prompt is advisory, the entire query should be intercepted by the guardrail and met with a refusal response.

## 5. Non-English Queries
*   **Edge Case:** A user inputs a query in Hindi or another regional language.
*   **Mitigation:** If multilingual support is not scoped, the intent classifier should detect the language and return a polite refusal stating that the assistant only supports English queries at this time.
