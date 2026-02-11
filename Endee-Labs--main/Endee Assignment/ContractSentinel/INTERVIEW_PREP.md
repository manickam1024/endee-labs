# 🎤 Interview Prep Guide: ContractSentinel

## Key Project Talking Points

1.  **"Not Just a Wrapper":** Emphasize that you built a custom **Agentic Loop** (ReAct pattern), not just a basic LangChain `retrieve_and_generate` function. You understand how the "brain" works.
2.  **Recall Matters:** Explain why you chose **Endee**. In legal/medical fields, missing a document (false negative) is worse than being slow. Endee's architecture focuses on high recall and efficiency.
3.  **Data Privacy:** This entire stack is containerized and can run **Air-Gapped** (offline). This is a huge selling point for Enterprise AI handling sensitive contracts.
4.  **Semantic Chunking:** Mention that you used recursive token splitting to preserve context, which is critical for parsing legalese that often spans multiple paragraphs.

---

## ❓ Likely Interview Questions & Answers

### Q1: Why did you choose Endee over Pinecone or Chroma?
**Answer:** "For this use case—Legal Risk Analysis—recall and data privacy were the top priorities. Cloud-only solutions like Pinecone raise data sovereignty issues for contracts. Endee offered a high-performance, container-ready solution that I could deploy locally. Its Vector Graph Engine (VGE) also promises better memory efficiency, allowing us to scale to millions of clauses without massive infrastructure costs."

### Q2: How does your Agent decide when to search?
**Answer:** "I implemented a ReAct (Reason-Act) loop. The Agent receives the query and first generates a 'Thought'. If the thought identifies missing information (e.g., 'I need to check the liability clause'), it triggers the 'Search' tool. This prevents the system from hallucinating answers or searching unnecessarily for simple pleasantries."

### Q3: How do you handle documents that exceed the context window?
**Answer:** "That's why the **Chunking Strategy** is foundational. I split the document into manageable chunks (e.g., 512 tokens) with overlap to preserve continuity. The retrieval step only pulls the top-k most relevant chunks. If a clause is split across chunks, the overlap ensures the semantic meaning is captured in at least one vector."

### Q4: How would you scale this to 10,000 contracts?
**Answer:**
1.  **Ingestion:** Move the ingestion pipeline to a message queue (RabbitMQ/Celery) for async processing.
2.  **Storage:** Endee is designed for scale, but we would implement Sharding based on `client_id` or `contract_type`.
3.  **Hybrid Search:** Implement BM25 (keyword) + Vector search to catch exact matches (like names/dates) better than vectors alone.

### Q5: What was the hardest part of this project?
**Answer:** "Getting the Agent to reliably follow the 'Playbook'. Large Language Models can be unpredictable. I had to refine the system prompts and tool descriptions to ensure the Agent strictly compared clauses against the risk rules rather than just summarizing the text."
