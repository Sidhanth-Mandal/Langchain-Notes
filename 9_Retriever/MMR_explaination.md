In **LangChain retrievers**, **MMR** stands for **Maximal Marginal Relevance**.

It’s a retrieval strategy that balances **relevance** *and* **diversity** when selecting documents for a query.

---

## What problem MMR solves

Standard similarity search:

* Retrieves the *most similar* documents to the query
* Often returns **near-duplicates** or very similar chunks

MMR:

* Retrieves documents that are **relevant to the query**
* While also being **different from each other**

This is especially useful for **RAG (Retrieval-Augmented Generation)** so the LLM sees a broader set of information instead of repetitive context.

---

## How MMR works (conceptually)

MMR selects documents iteratively:

1. Pick the most relevant document to the query
2. For each next document, score it as:

[
\text{MMR} = \lambda \cdot \text{similarity(query, doc)}
;;-;;
(1 - \lambda) \cdot \text{similarity(doc, selected_docs)}
]

Where:

* **λ (lambda)** controls the tradeoff

  * `λ → 1`: favor relevance (like normal similarity search)
  * `λ → 0`: favor diversity

---

## MMR in LangChain retrievers

LangChain exposes MMR through retrievers like **VectorStoreRetriever**.

### Example

```python
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,          # final number of documents returned
        "fetch_k": 20,   # number of candidates to consider
        "lambda_mult": 0.5
    }
)
```

### Key parameters

| Parameter     | Meaning                                               |
| ------------- | ----------------------------------------------------- |
| `k`           | Number of documents returned                          |
| `fetch_k`     | Number of top candidates fetched before MMR selection |
| `lambda_mult` | Relevance vs diversity tradeoff (0–1)                 |

---

## When to use MMR

✅ Use MMR when:

* You want **less redundancy** in retrieved chunks
* Documents overlap heavily (chunked PDFs, docs, webpages)
* You’re doing **question answering or summarization**

❌ Skip MMR when:

* You need the **top-N most similar** passages
* Precision is more important than coverage

---

## Intuition in one sentence

> **MMR = “Give me relevant results, but don’t keep saying the same thing.”**