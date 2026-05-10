# Phase 4 Edge Cases: Retrieval-Augmented Generation (RAG) Core

This document outlines potential edge cases during the RAG retrieval and generation phase and proposes mitigation strategies.

## 1. Empty or Irrelevant Retrieval
*   **Edge Case:** The vector search returns chunks that are completely irrelevant to the user's query, or returns no chunks above the similarity threshold.
*   **Mitigation:** Instruct the generation LLM via the system prompt: "If the provided context does not contain the answer, politely state that you do not have the information." Do not allow the LLM to guess.

## 2. Conflicting Context Information
*   **Edge Case:** The retrieval fetches chunks from different dates that have conflicting information (e.g., an old factsheet and a new one showing different expense ratios).
*   **Mitigation:** Ensure strict metadata filtering to prioritize the most recently updated documents. Pass the `last_updated_date` to the LLM and instruct it to use the most recent information.

## 3. LLM Hallucinations
*   **Edge Case:** Despite instructions, the LLM incorporates its pre-training knowledge to answer a question that is not present in the retrieved context.
*   **Mitigation:** Use a lower temperature setting (e.g., `temperature=0.0`) for generation. Emphasize in the prompt: "STRICTLY use ONLY the provided context. Do NOT use outside knowledge."

## 4. 3-Sentence Limit Violation
*   **Edge Case:** The LLM struggles to compress a complex factual answer (e.g., multi-tiered exit load structures) into the strict 3-sentence limit.
*   **Mitigation:** Provide few-shot examples in the system prompt demonstrating how to summarize complex fee structures concisely. If necessary, allow bullet points within the 3-sentence constraint.

## 5. Missing Citations
*   **Edge Case:** The post-processing step fails to append the correct source URL because the metadata was lost during chunking or retrieval.
*   **Mitigation:** Ensure metadata is tightly coupled with the `Document` object throughout the LangChain/LlamaIndex pipeline. Implement a fallback link to the general AMC mutual fund page if the specific chunk URL is missing.
