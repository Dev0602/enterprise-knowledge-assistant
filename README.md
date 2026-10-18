cat > README.md <<'EOF'
# 📚 Enterprise Knowledge Assistant

A production-style Retrieval-Augmented Generation (RAG) system for answering questions from company policies and internal documents.

The system combines semantic search, keyword search, Reciprocal Rank Fusion (RRF), cross-encoder reranking, confidence-based abstention, local LLM generation, and grounding evaluation to produce reliable answers from enterprise knowledge.

---

## 🚀 Features

- 📄 PDF document ingestion
- ✂️ Document chunking
- 🧠 Sentence Transformer embeddings
- 🗄️ ChromaDB vector database
- 🔎 Semantic vector search
- 🔤 BM25 keyword search
- 🔀 Reciprocal Rank Fusion (RRF)
- 🎯 Cross-encoder reranking
- 🛡️ Confidence-based abstention
- 🤖 Qwen 2.5 local LLM via Ollama
- ✅ Answer grounding evaluation
- 📚 Source document display
- 💬 Streamlit chat interface
- 📊 Retrieval and RAG evaluation metrics

---

# 🏗️ Architecture

The system follows a multi-stage RAG pipeline:

```text
                    COMPANY DOCUMENTS
                           │
                           ▼
                  ┌─────────────────┐
                  │ PDF Ingestion   │
                  │ & Text Parsing  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    Chunking     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Embeddings    │
                  │ Sentence        │
                  │ Transformers    │
                  └────────┬────────┘
                           │
                           ▼
                     ┌───────────┐
                     │ ChromaDB  │
                     └─────┬─────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
       Vector Search               BM25 Search
       Semantic Search             Keyword Search
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │       RRF       │
                  │ Rank Fusion     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Cross-Encoder   │
                  │   Reranker      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Confidence Gate │
                  └────────┬────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
          Low Confidence        High Confidence
                 │                   │
                 ▼                   ▼
          Abstain / Fallback      Qwen 2.5
                                      │
                                      ▼
                              Grounding Evaluation
                                      │
                                      ▼
                              Final Answer + Sources
                                      │
                                      ▼
                                Streamlit UI


                            