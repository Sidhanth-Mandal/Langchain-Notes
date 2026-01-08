In **LangChain**, a **ContextualCompressionRetriever** is a retriever that **reduces and refines retrieved documents *after* retrieval**, keeping only the parts that are **relevant to the user’s query**.

Think of it as a **post-retrieval “compression” step**.

---

## The problem it solves

Standard retrievers return full chunks or documents:

* Many sentences are **irrelevant**
* Context window gets **wasted**
* LLM sees **noise**, hurting answer quality

Even good retrieval ≠ good context.

---

## What ContextualCompressionRetriever does

1. **Retrieves documents** using a base retriever (vector, BM25, MMR, MultiQuery, etc.)
2. **Compresses each document** using a *document compressor*
3. Returns **shorter, query-focused content**

---

## Mental model

> **Retriever finds documents → Compressor trims them to what matters**

---

## Architecture

```
User Query
   ↓
Base Retriever (vector / MMR / multi-query)
   ↓
ContextualCompressionRetriever
   ↓
Compressed documents
   ↓
LLM
```

---

## Key components

### 1️⃣ Base Retriever

Any retriever that returns documents:

```python
base_retriever = vectorstore.as_retriever()
```

---

### 2️⃣ Document Compressor

Responsible for shrinking content.

Common compressors:

| Compressor                   | What it does                           |
| ---------------------------- | -------------------------------------- |
| `LLMChainExtractor`          | Extracts only relevant sentences       |
| `LLMChainFilter`             | Drops irrelevant documents             |
| `EmbeddingsFilter`           | Keeps only semantically relevant parts |
| `DocumentCompressorPipeline` | Chain multiple compressors             |

---

## Example: LLM-based compression (most common)

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0)

compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_retriever=vectorstore.as_retriever(),
    document_compressor=compressor
)

docs = compression_retriever.get_relevant_documents(
    "How does MMR improve RAG retrieval?"
)
```

Result:

* Short, focused snippets
* Less hallucination
* Better signal-to-noise ratio

---

## Example: Embedding-based compression (cheaper, faster)

```python
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

compressor = EmbeddingsFilter(
    embeddings=embeddings,
    similarity_threshold=0.76
)
```

No LLM calls → lower cost, lower precision.

---

## When to use ContextualCompressionRetriever

✅ Use it when:

* Documents are **long**
* Chunks still contain irrelevant info
* You hit **context window limits**
* You want higher answer quality in RAG

❌ Avoid it when:

* Documents are already small and clean
* Latency is critical (LLM compression adds time)
* You need verbatim full documents

---

## How it compares to other retrievers

| Technique                      | Purpose                     |
| ------------------------------ | --------------------------- |
| MultiQueryRetriever            | Expands *queries*           |
| MMR                            | Diversifies *results*       |
| ContextualCompressionRetriever | Shrinks *content*           |
| Parent / Child Retriever       | Reconstructs larger context |

💡 Best practice:

> **MultiQuery → MMR → Contextual Compression**

---

## One-sentence summary

> **ContextualCompressionRetriever retrieves documents normally, then compresses them to keep only query-relevant information before sending to the LLM.**