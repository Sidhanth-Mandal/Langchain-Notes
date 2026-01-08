In **LangChain**, a **MultiQuery Retriever** is a retriever that improves recall by asking the LLM to generate **multiple alternative versions of the user’s query**, then retrieving documents for **each** version and merging the results.

It’s designed to solve the problem that **one query often isn’t enough** to find all relevant documents.

---

## The problem it solves

Vector search depends heavily on **how the query is phrased**.

Example user question:

> *“How do I speed up my LangChain RAG pipeline?”*

A single embedding query might miss documents that talk about:

* “performance optimization”
* “latency reduction”
* “retriever tuning”
* “MMR vs similarity search”

---

## What MultiQuery Retriever does

1. Takes the **original user question**
2. Uses an **LLM** to generate **N paraphrased / expanded queries**
3. Runs retrieval for **each query**
4. **Deduplicates and merges** the results
5. Returns a richer, more complete document set

---

## Simple mental model

> **MultiQuery = “Ask the same question multiple smart ways.”**

---

## How it works internally

### Step-by-step

1. LLM generates alternative queries:

   ```
   1. How can retrieval latency be reduced in LangChain?
   2. What techniques improve RAG pipeline performance?
   3. How to optimize vector search in LangChain?
   ```

2. Retriever runs similarity search for each query

3. Results are:

   * Combined
   * Deduplicated (usually by document ID or content hash)

---

## Example in LangChain (Python)

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm,
    include_original=True
)

docs = retriever.get_relevant_documents(
    "How do I speed up my LangChain RAG pipeline?"
)
```

---

## Key configuration options

| Option             | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `llm`              | LLM used to generate query variants                   |
| `retriever`        | Base retriever (vector, hybrid, etc.)                 |
| `include_original` | Keep the original query in addition to generated ones |
| `prompt`           | Custom prompt for query generation                    |

---

## When MultiQuery Retriever is useful

✅ Use it when:

* Queries are **ambiguous or high-level**
* You have **heterogeneous documents**
* Recall matters more than speed
* You’re missing answers with single-query search

❌ Avoid it when:

* Low-latency is critical (it runs multiple searches)
* Your documents are already well-structured
* Queries are very precise

---

## MultiQuery vs MMR (important distinction)

| MultiQuery                  | MMR                          |
| --------------------------- | ---------------------------- |
| Expands the **query space** | Diversifies the **results**  |
| Improves recall             | Reduces redundancy           |
| Uses an LLM                 | Pure retrieval algorithm     |
| Multiple searches           | Single search with reranking |

💡 **They are often used together**:

* MultiQuery to find *more candidates*
* MMR to select *diverse, relevant* documents

---

## One-sentence summary

> **MultiQuery Retriever increases recall by using an LLM to rephrase the user’s question into multiple semantically different queries.**
