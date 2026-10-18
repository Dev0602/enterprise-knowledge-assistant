# RAG System Evaluation

## Overview

The Enterprise Knowledge Assistant was evaluated across
answerable and unanswerable questions to measure retrieval
quality, answer grounding, source retrieval, and abstention
behavior.

The evaluation dataset contains:

- 7 answerable questions
- 2 unanswerable questions
- 9 total test cases

---

## Final Results

| Metric | Result |
|---|---:|
| Answerable Question Accuracy | 100% |
| Abstention Accuracy | 100% |
| Grounded Answer Rate | 100% |
| Expected Source Retrieval | 100% |
| Recall@3 | 100% |
| Vector Search MRR | 1.0000 |
| Hybrid Search MRR | 0.7381 |
| Hybrid + Reranker MRR | 0.9286 |

---

## Retrieval Evaluation

### Recall@3

Recall@3 measures whether the expected relevant
document appears within the top 3 retrieved results.

**Result: 100%**

This means the expected source document was retrieved
for all evaluated answerable questions.

---

## Mean Reciprocal Rank

MRR measures how highly the relevant document appears
in the ranked retrieval results.

### Vector Search

**MRR: 1.0000**

Vector search retrieved the relevant document at the
top rank for the evaluated dataset.

### Hybrid Search

Hybrid retrieval combines:

- Vector similarity search
- BM25 keyword search
- Reciprocal Rank Fusion (RRF)

**MRR: 0.7381**

### Hybrid + Cross-Encoder Reranking

The hybrid candidates were further ranked using a
cross-encoder reranker.

**MRR: 0.9286**

The reranker substantially improved ranking quality
compared with the hybrid retrieval stage.

---

## Grounding Evaluation

The system uses a grounding evaluator to determine
whether generated answers are supported by the
retrieved company information.

### Result

**Grounded Answer Rate: 100%**

All answerable questions in the evaluation dataset
produced answers classified as `SUPPORTED`.

---

## Abstention Evaluation

The system also evaluates questions for which the
knowledge base does not contain the requested
information.

Unanswerable test cases included:

- Maternity leave policy
- Employee stock option policy

For these questions, the system correctly returned:

> I couldn't find that information in the company knowledge base.

### Result

**Abstention Accuracy: 100%**

This demonstrates that the system can avoid generating
unsupported answers when relevant information is not
available in the knowledge base.

---

## Example: Answerable Question

### Question

> Can I work remotely?

### Answer

> Employees may work remotely when their role, manager
> approval, and business needs allow it.

### Result

- Relevant source retrieved: `02_remote_work_policy.pdf`
- Grounding verdict: `SUPPORTED`

---

## Example: Unanswerable Question

### Question

> What is the employee stock option policy?

### Result

- Relevant information found: No
- Answer: Knowledge-base fallback
- Grounding verdict: `ABSTENTION`

---

## RAG Architecture

```text
Company PDFs
     |
     v
Document Ingestion
     |
     v
Chunking
     |
     v
Sentence Transformer Embeddings
     |
     v
ChromaDB
     |
     +------------------+
     |                  |
     v                  v
Vector Search        BM25 Search
     |                  |
     +--------+---------+
              |
              v
      Reciprocal Rank Fusion
              |
              v
     Cross-Encoder Reranker
              |
              v
       Confidence Gate
              |
              v
          Qwen 2.5
              |
              v
      Grounding Evaluation
              |
              v
       Final Answer + Sources
              |
              v
         Streamlit UI