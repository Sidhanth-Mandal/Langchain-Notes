In the context of building LLM applications (like RAG - Retrieval Augmented Generation), text splitters are critical components. Large Language Models have context windows (token limits), so you cannot feed an entire book or massive document into them at once. You must break the text into smaller, semantically meaningful chunks.

LangChain provides a variety of text splitters to handle this. Below is a detailed explanation of the most important ones with examples.

---

### Key Concepts Before We Begin

Before looking at the specific splitters, there are two parameters you will see in almost every example:

1. **`chunk_size`**: The maximum size of your chunks (measured in characters or tokens).
2. **`chunk_overlap`**: The amount of overlap between two consecutive chunks. This is crucial to ensure that context isn't lost at the cut points.

---

### 1. RecursiveCharacterTextSplitter (Recommended Default)

This is the most versatile and commonly used splitter. It doesn't just split by a single character; it tries to split by a list of separators in order (e.g., `\n\n`, then `\n`, then `     `, then `""`).

**Why it's good:** It attempts to keep paragraphs, sentences, and words together for as long as possible, preserving the semantic structure of the text.

**Example:**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """
LangChain is a framework for developing applications powered by language models.
It enables applications that:
1. Are context-aware: connect a language model to sources of context.
2. Reason: rely on a language model to reason (how to answer based on provided context).
"""

# Initialize the splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

docs = text_splitter.create_documents([text])

for i, doc in enumerate(docs):
    print(f"Chunk {i+1}: {doc.page_content!r}")

```

---

### 2. CharacterTextSplitter

This is the simplest method. It splits based on a single specific character (default is `"\n\n"`).

**Why use it:** It is faster and useful if you have very consistently formatted text where you know exactly where the breaks should be. However, it is less flexible than the Recursive splitter.

**Example:**

```python
from langchain.text_splitter import CharacterTextSplitter

text = "This is the first paragraph.\n\nThis is the second paragraph.\n\nThis is the third."

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=50,
    chunk_overlap=10
)

docs = text_splitter.create_documents([text])
# Result will be exactly the paragraphs split by the double newline

```

---

### 3. TokenTextSplitter

LLMs (like GPT-4) operate on tokens, not characters. A character limit of 1000 might be 200 tokens or 500 tokens depending on the language. To maximize the usage of the context window without breaking limits, use a Token Splitter.

**Why use it:** When you need strict adherence to the model's context window limits (e.g., ensuring a chunk is exactly 500 tokens).

**Example:**

```python
from langchain.text_splitter import TokenTextSplitter

text = "LangChain is awesome!" * 50  # A long string

text_splitter = TokenTextSplitter(
    chunk_size=10,
    chunk_overlap=0
)

docs = text_splitter.split_text(text)
print(docs[0]) 

```

---

### 4. MarkdownHeaderTextSplitter

This is highly effective for technical documentation or structured content. It splits text based on Markdown headers (`#`, `##`, `###`).

**Why use it:** It attaches the header information to the metadata of the chunk. This provides excellent context for the LLM. If a chunk says "Return True," knowing it came from the "Authentication > Login" header makes it much more valuable.

**Example:**

```python
from langchain.text_splitter import MarkdownHeaderTextSplitter

markdown_document = """
# Introduction
This is the intro.

## Installation
Run `pip install langchain`.

## Usage
Import the module.
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
docs = markdown_splitter.split_text(markdown_document)

for doc in docs:
    print(f"Content: {doc.page_content}")
    print(f"Metadata: {doc.metadata}")
    print("---")

```

**Output Insight:**
The metadata for the "Installation" chunk will look like: `{'Header 1': 'Introduction', 'Header 2': 'Installation'}` (depending on hierarchy settings), allowing you to filter by section later.

---

### 5. Code Splitters (Language Specific)

LangChain has a `RecursiveCharacterTextSplitter.from_language` method which comes pre-configured with separators for specific programming languages (Python, JS, Go, etc.).

**Why use it:** It ensures that classes and functions aren't split in the middle of a syntax block, which would confuse the LLM.

**Example (Python):**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

python_code = """
def hello_world():
    print("Hello, World!")

class Greeter:
    def greet(self):
        return "Hi there"
"""

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, 
    chunk_size=50, 
    chunk_overlap=0
)

docs = python_splitter.create_documents([python_code])

```

---

### Summary of When to Use What

| Splitter | Use Case |
| --- | --- |
| **RecursiveCharacter** | **General purpose.** The best starting point for PDF text, articles, and generic documents. |
| **Character** | Simple, raw text files where paragraphs are clearly separated by double newlines. |
| **Token** | When hitting exact API token limits is your priority. |
| **MarkdownHeader** | Documentation, READMEs, or Notion exports. Essential for preserving structure. |
| **Language (Code)** | Indexing codebases for code analysis or Q&A. |

