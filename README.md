⚖️ ClauseGuardian: Intelligent Legal Risk Review Agent






ClauseGuardian is an autonomous legal analysis assistant built to modernize contract risk assessment. Rather than relying on surface-level keyword matching or basic retrieval-augmented chat systems, it applies structured agent reasoning combined with high-recall semantic search to detect, evaluate, and contextualize contractual risk.

🚀 The Core Problem

Legal professionals invest enormous time reviewing contracts such as NDAs, MSAs, and vendor agreements. Overlooking a single asymmetric indemnity clause or an unlimited liability provision can expose organizations to significant financial and operational risk.

Why Traditional Tools Fall Short

Keyword search fails when clauses are written using alternative phrasing.

Basic RAG systems may retrieve loosely related sections or fabricate context.

Approximate search engines can sacrifice retrieval accuracy for speed.

In legal review, precision and recall are non-negotiable.

The Approach

ClauseGuardian combines:

High-Recall Semantic Retrieval
A vector database optimized for recall ensures critical clauses are retrieved even when phrased differently. This prevents important provisions from being overlooked due to wording variations.

Agent-Based Reasoning Engine
Instead of answering in one step, the system follows a structured reasoning path:

Identify relevant clause categories

Retrieve supporting contract sections

Evaluate clause language against predefined risk criteria

Generate a contextual risk explanation

Rule-Driven Risk Benchmarking
Extracted clauses are compared against internal legal playbooks or policy thresholds (e.g., liability caps, indemnification symmetry, termination rights).

This layered workflow mimics how experienced legal professionals review contracts — systematically and contextually.

🏗️ System Architecture

User uploads contract (PDF)
↓
Frontend Interface (Streamlit)
↓
FastAPI Backend
↓
Agentic Core

Reasoning Agent

Tool Set (Vector Search + Risk Rule Engine)
↓
High-Recall Vector Database
↓
Contextual Risk Analysis Returned to User

Data Pipeline:

Document ingestion

Recursive semantic chunking

Embedding generation (BGE-M3)

Vector storage in database

🔧 Technology Stack

Vector Database: Endee

Agent Framework: Custom ReAct-style state machine (Python)

Backend: FastAPI with Pydantic

Frontend: Streamlit

Embeddings: BAAI/bge-m3 via SentenceTransformers

LLM Compatibility: Llama 3 (Ollama) or GPT-4

🏃 How to Run

Prerequisites:

Docker and Docker Compose

Python 3.10+ (if running without Docker)

Setup Steps:

Clone the repository
git clone https://github.com/yourusername/ContractSentinel.git

cd ContractSentinel
cp .env.example .env

Start services with Docker
docker-compose up --build

Services will launch at:

Vector Database: localhost:8080

Backend API: localhost:8000

Frontend UI: localhost:8501

Usage:

Open http://localhost:8501

Upload a contract PDF

Click “Ingest Document”

Ask questions such as:

Does this agreement include mutual indemnification?

What is the liability cap?

Can either party terminate for convenience?

🧠 Why This Vector Database Choice Matters

In legal AI, retrieval accuracy is more important than raw speed.

Many vector systems rely heavily on approximate nearest neighbor search, which may skip relevant clauses to optimize performance.

The selected vector engine focuses on:

High recall for sensitive legal text

Lower memory consumption

Suitability for on-premise deployment

Strong performance for compliance-sensitive environments

When reviewing contracts, missing a clause is not acceptable.

🔮 Future Roadmap

Graph-Enhanced Retrieval (GraphRAG) to track entity relationships

Multi-modal support for scanned PDFs and tables

Automated risk checks integrated into CI/CD pipelines

Version comparison for contract redlines

Risk scoring dashboard with historical analytics
