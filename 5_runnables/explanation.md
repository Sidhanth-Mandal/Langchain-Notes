# LangChain Runnables – Detailed Guide

LangChain **Runnables** are the core abstraction used to build flexible, composable, and reusable AI workflows. They allow you to chain prompts, models, tools, and logic together in a clean and predictable way.

This README explains the main **Runnable types**:

* Branch
* Lambda
* Parallel
* Passthrough
* Sequence

---

## What Are Runnables?

A **Runnable** is any object that:

* Takes an input
* Performs an operation
* Returns an output

Runnables can be:

* Chained together
* Executed synchronously or asynchronously
* Combined into complex workflows

They replace older patterns like `LLMChain` and provide more flexibility and control.

---

## 1. RunnableSequence

### Purpose

Executes multiple runnables **one after another**, where the output of one becomes the input of the next.

### How It Works

```
Input → Step 1 → Step 2 → Step 3 → Output
```

### When to Use

* Linear workflows
* Prompt → LLM → Parser
* Step-by-step transformations

### Example

```python
from langchain.schema.runnable import RunnableSequence

chain = RunnableSequence([prompt, llm, output_parser])
result = chain.invoke("Explain gravity")
```

### Key Points

* Order matters
* Most common runnable type
* Simple and predictable

---

## 2. RunnableParallel

### Purpose

Runs multiple runnables **at the same time** using the same input.

### How It Works

```
        ┌─ Runnable A ─┐
Input ──┼─ Runnable B ─┼─> Combined Output
        └─ Runnable C ─┘
```

### When to Use

* Run multiple prompts at once
* Compare different models
* Extract different types of information in parallel

### Example

```python
from langchain.schema.runnable import RunnableParallel

parallel = RunnableParallel({
    "summary": summary_chain,
    "keywords": keyword_chain
})

result = parallel.invoke("LangChain is a framework for LLM apps")
```

### Output

```json
{
  "summary": "...",
  "keywords": "..."
}
```

### Key Points

* Faster execution
* Same input → multiple outputs
* Output is a dictionary

---

## 3. RunnableBranch

### Purpose

Chooses **one runnable to execute** based on a condition.

### How It Works

```
          ┌─ If condition A → Runnable A
Input ────┼─ If condition B → Runnable B
          └─ Else → Default Runnable
```

### When to Use

* Conditional logic
* Routing queries
* Decision-based workflows

### Example

```python
from langchain.schema.runnable import RunnableBranch

branch = RunnableBranch(
    (lambda x: "math" in x, math_chain),
    (lambda x: "code" in x, code_chain),
    general_chain
)

result = branch.invoke("Solve this math problem")
```

### Key Points

* First matching condition is used
* Last runnable acts as default
* Similar to `if / elif / else`

---

## 4. RunnableLambda

### Purpose

Wraps a **custom Python function** into a runnable.

### How It Works

```
Input → Python Function → Output
```

### When to Use

* Custom logic
* Data transformation
* Validation or formatting

### Example

```python
from langchain.schema.runnable import RunnableLambda

uppercase = RunnableLambda(lambda x: x.upper())
result = uppercase.invoke("hello")
```

### Output

```
HELLO
```

### Key Points

* Lightweight
* No LLM required
* Great for glue logic

---

## 5. RunnablePassthrough

### Purpose

Passes input through **unchanged** (or slightly modified).

### How It Works

```
Input → Output (same value)
```

### When to Use

* Preserve original input
* Combine raw input with processed output
* Debugging pipelines

### Example

```python
from langchain.schema.runnable import RunnablePassthrough

passthrough = RunnablePassthrough()
result = passthrough.invoke("Keep this text")
```

### Example with Assignment

```python
passthrough = RunnablePassthrough.assign(
    length=lambda x: len(x)
)

result = passthrough.invoke("Hello")
```

### Output

```json
{
  "input": "Hello",
  "length": 5
}
```

### Key Points

* Does not alter original input
* Useful in complex pipelines
* Often combined with Parallel

---

## Summary Table

| Runnable Type | Purpose                    | Execution Style |
| ------------- | -------------------------- | --------------- |
| Sequence      | Step-by-step execution     | Linear          |
| Parallel      | Run multiple tasks at once | Concurrent      |
| Branch        | Conditional execution      | Decision-based  |
| Lambda        | Custom Python logic        | Functional      |
| Passthrough   | Preserve input             | Utility         |

---

## Final Notes

* Runnables are **composable**
* They replace older LangChain abstractions
* They support sync, async, and streaming
* They make AI workflows cleaner and more maintainable

---
