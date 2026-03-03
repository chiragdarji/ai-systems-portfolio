# Experiment 05 — Token Limit Analysis Results

> **Model**: `gpt-4o-mini` | **Temperature**: `0.3` | **Budgets**: [50, 150, 300, 600]

---

## Domain: `explanation`

**Prompt (truncated):** *Explain how Retrieval-Augmented Generation (RAG) works. Cover: what it is, why it exists, how retrieval and generation i...*

| max_tokens | Used | Utilisation | finish_reason | Truncated | Cost USD |
|------------|------|-------------|---------------|-----------|----------|
| 50 | 50 | 100.0% | `length` | **YES ⚠** | `$0.000039` |
| 150 | 150 | 100.0% | `length` | **YES ⚠** | `$0.000099` |
| 300 | 300 | 100.0% | `length` | **YES ⚠** | `$0.000189` |
| 600 | 600 | 100.0% | `length` | **YES ⚠** | `$0.000369` |

### `max_tokens=50` — ⚠ TRUNCATED

```
Retrieval-Augmented Generation (RAG) is a hybrid approach that combines the strengths of retrieval-based methods and generative models to enhance the performance of natural language processing tasks, particularly in generating responses or answers based on external knowledge sources.

### What It
```

### `max_tokens=150` — ⚠ TRUNCATED

```
Retrieval-Augmented Generation (RAG) is a hybrid approach that combines the strengths of information retrieval and natural language generation to enhance the capabilities of language models. Here’s a detailed breakdown of RAG, including its purpose, interaction between retrieval and generation, and scenarios for its use compared to fine-tuning.

### What is RAG?

RAG is a framework that integrates a retrieval mechanism with a generative model. It typically consists of two main components:

1. **Retriever**: This component searches a large corpus of documents or knowledge bases to find relevant information based on a given query. The retriever can use various techniques, such as traditional keyword search or more advanced methods like dense vector similarity.

2. **Generator**: Once the retr
```

### `max_tokens=300` — ⚠ TRUNCATED

```
Retrieval-Augmented Generation (RAG) is a hybrid approach that combines the strengths of information retrieval and natural language generation to enhance the performance of language models, particularly in tasks that require generating contextually relevant and accurate responses based on external knowledge.

### What it is

RAG integrates two main components: a retriever and a generator. The retriever is responsible for fetching relevant documents or pieces of information from a large corpus based on a given query. The generator then uses this retrieved information to produce coherent and contextually appropriate text. This approach allows the model to leverage external knowledge, making it more effective in generating responses that are informed by up-to-date or specific information that may not be present in the model's training data.

### Why it exists

RAG exists to address limitations in traditional language models, which often rely solely on the data they were trained on. These models can struggle with:

1. **Outdated Information**: They may not have access to the latest facts or developments.
2. **Specificity**: They can lack detailed knowledge on niche topics that were not well-represented in the training dataset.
3. **Scalability**: Fine-tuning a model on every possible topic or domain is impractical.

By combining retrieval and generation, RAG allows models to dynamically access a broader range of information, improving their ability to generate accurate and relevant responses.

### How retrieval and generation interact

1. **Retrieval Phase**: When a user inputs a query
```

### `max_tokens=600` — ⚠ TRUNCATED

```
Retrieval-Augmented Generation (RAG) is a hybrid approach that combines the strengths of information retrieval and natural language generation to enhance the capabilities of language models. Here’s a detailed breakdown of what RAG is, why it exists, how retrieval and generation interact, and when to use it over fine-tuning.

### What is RAG?

RAG is a framework that integrates a retrieval mechanism with a generative model. It typically consists of two main components:

1. **Retriever**: This component searches a large corpus of documents or knowledge base to find relevant pieces of information based on a given query or prompt. The retriever can use various techniques, such as TF-IDF, BM25, or more advanced neural retrieval methods.

2. **Generator**: After the retriever identifies relevant documents, the generator (often a transformer-based model) uses this information to produce coherent and contextually relevant text. The generator can be fine-tuned on specific tasks to improve its performance.

### Why Does RAG Exist?

RAG exists to address several limitations of traditional generative models:

1. **Knowledge Limitations**: Generative models, especially those trained on static datasets, may not have up-to-date information or may lack specific knowledge about niche topics. RAG allows the model to access a dynamic and extensive knowledge base.

2. **Contextual Relevance**: By retrieving relevant documents, RAG can provide contextually rich information that enhances the quality and accuracy of the generated text.

3. **Efficiency**: Instead of fine-tuning a model on every possible topic, RAG can leverage existing knowledge bases, making it more efficient to handle a wider range of queries without extensive retraining.

### How Retrieval and Generation Interact

The interaction between retrieval and generation in RAG occurs in a two-step process:

1. **Retrieval Phase**: When a user inputs a query, the retriever searches the knowledge base and retrieves a set of relevant documents or passages. This process is crucial because the quality and relevance of the retrieved information directly influence the output of the generator.

2. **Generation Phase**: The retrieved documents are then fed into the generative model, which synthesizes the information to produce a coherent response. The generator can use the context from the retrieved documents to enhance its output, ensuring that the generated text is not only relevant but also informative.

### When to Use RAG Over Fine-Tuning

Choosing RAG over fine-tuning depends on several factors:

1. **Dynamic Knowledge Requirements**: If the application requires up-to-date information or knowledge that changes frequently (e.g., current events, technical documentation), RAG is preferable because it can access real-time data.

2. **Diversity of Topics**: When dealing with a wide range of topics or domains, RAG can efficiently handle queries without the need for extensive fine-tuning on each specific area.

3. **Resource Constraints**: Fine-tuning a model can be resource-intensive, requiring
```

---

## Domain: `summarisation`

**Prompt (truncated):** *Summarise the following in your own words:

Large Language Models (LLMs) are deep learning systems trained on massive co...*

| max_tokens | Used | Utilisation | finish_reason | Truncated | Cost USD |
|------------|------|-------------|---------------|-----------|----------|
| 50 | 50 | 100.0% | `length` | **YES ⚠** | `$0.000049` |
| 150 | 85 | 56.7% | `stop` | no | `$0.000070` |
| 300 | 89 | 29.7% | `stop` | no | `$0.000072` |
| 600 | 100 | 16.7% | `stop` | no | `$0.000079` |

### `max_tokens=50` — ⚠ TRUNCATED

```
Large Language Models (LLMs) are advanced deep learning systems that analyze extensive text data to identify statistical patterns and produce coherent text. While they excel in generating fluent and contextually appropriate content, they often produce inaccurate information, known as hallucination, as
```

### `max_tokens=150` — ✓ Complete

```
Large Language Models (LLMs) are advanced deep learning systems that analyze vast amounts of text to learn patterns and produce coherent, contextually appropriate text. However, they can produce misleading information, known as hallucination, as they prioritize fluency over factual correctness. While they are useful for drafting and exploring ideas, they are not dependable for accurate factual information in critical situations unless supported by grounding methods like RAG or external tools.
```

### `max_tokens=300` — ✓ Complete

```
Large Language Models (LLMs) are advanced deep learning systems that analyze vast amounts of text to identify statistical patterns, enabling them to produce coherent and contextually appropriate text. However, they can create misleading information, known as hallucination, as they prioritize fluency over factual correctness. While they are useful for drafting and exploratory tasks, they are not dependable for accurate information retrieval in critical situations unless supported by grounding methods like RAG or tool integration.
```

### `max_tokens=600` — ✓ Complete

```
Large Language Models (LLMs) are advanced deep learning systems that analyze extensive text data to identify statistical patterns in language, enabling them to produce coherent and contextually appropriate text. However, they can sometimes create convincing yet inaccurate information, a phenomenon known as hallucination, as they prioritize fluency over factual correctness. While LLMs are useful for drafting and exploring ideas, they are not dependable for critical factual information unless supported by grounding methods like Retrieval-Augmented Generation (RAG) or other tools.
```

---

## Domain: `code`

**Prompt (truncated):** *Write a Python class called VectorStore that supports: add(id, embedding, metadata), search(query_embedding, top_k) usin...*

| max_tokens | Used | Utilisation | finish_reason | Truncated | Cost USD |
|------------|------|-------------|---------------|-----------|----------|
| 50 | 50 | 100.0% | `length` | **YES ⚠** | `$0.000040` |
| 150 | 150 | 100.0% | `length` | **YES ⚠** | `$0.000100` |
| 300 | 300 | 100.0% | `length` | **YES ⚠** | `$0.000190` |
| 600 | 600 | 100.0% | `length` | **YES ⚠** | `$0.000370` |

### `max_tokens=50` — ⚠ TRUNCATED

```
```python
import math
from typing import List, Dict, Any

class VectorStore:
    """
    A simple vector store class that allows adding, searching, and deleting
    vector embeddings along with associated metadata. The search is performed
```

### `max_tokens=150` — ⚠ TRUNCATED

```
```python
import math
from typing import List, Dict, Any

class VectorStore:
    """
    A simple vector store that allows adding, searching, and deleting vectors 
    with associated metadata. It uses cosine similarity for searching.
    """

    def __init__(self):
        self.vectors: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Any] = {}

    def add(self, id: str, embedding: List[float], metadata: Any = None) -> None:
        """
        Adds a vector with its associated metadata to the store.

        :param id: Unique identifier for the vector.
        :param embedding: List of floats representing the vector.
        :param metadata: Optional metadata
```

### `max_tokens=300` — ⚠ TRUNCATED

```
```python
import math
from typing import List, Dict, Tuple

class VectorStore:
    """
    A simple in-memory vector store that supports adding, searching, and deleting vectors.
    
    Attributes:
        vectors (Dict[str, Tuple[List[float], Dict]]): A dictionary mapping IDs to tuples of (embedding, metadata).
    """

    def __init__(self):
        self.vectors: Dict[str, Tuple[List[float], Dict]] = {}

    def add(self, id: str, embedding: List[float], metadata: Dict) -> None:
        """
        Add a vector to the store with the given ID, embedding, and metadata.

        Args:
            id (str): The unique identifier for the vector.
            embedding (List[float]): The vector to be stored.
            metadata (Dict): Additional information associated with the vector.
        """
        self.vectors[id] = (embedding, metadata)

    def search(self, query_embedding: List[float], top_k: int) -> List[Tuple[str, float, Dict]]:
        """
        Search for the top_k most similar vectors to the query embedding using cosine similarity.

        Args:
            query_embedding (List[float]): The embedding to search against.
            top_k (int): The number of top similar vectors to return.

        Returns:
            List[Tuple[str, float, Dict]]: A list of tuples containing the ID, similarity score, and metadata of the top_k vectors.
```

### `max_tokens=600` — ⚠ TRUNCATED

```
```python
import math
from typing import List, Dict, Optional

class VectorStore:
    """
    A simple vector store that supports adding, searching, and deleting vectors
    with associated metadata. The search is performed using cosine similarity.

    Attributes:
        vectors (Dict[str, List[float]]): A dictionary to store vectors by their IDs.
        metadata (Dict[str, Dict]): A dictionary to store metadata by their IDs.
    """

    def __init__(self):
        self.vectors: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Dict] = {}

    def add(self, id: str, embedding: List[float], metadata: Optional[Dict] = None) -> None:
        """
        Add a vector and its associated metadata to the store.

        Args:
            id (str): The unique identifier for the vector.
            embedding (List[float]): The vector to be added.
            metadata (Optional[Dict]): The associated metadata for the vector.
        """
        self.vectors[id] = embedding
        self.metadata[id] = metadata if metadata is not None else {}

    def search(self, query_embedding: List[float], top_k: int) -> List[Dict]:
        """
        Search for the top_k most similar vectors to the query_embedding using cosine similarity.

        Args:
            query_embedding (List[float]): The vector to search for.
            top_k (int): The number of top similar vectors to return.

        Returns:
            List[Dict]: A list of dictionaries containing the ID, similarity score, and metadata of the top_k vectors.
        """
        similarities = []
        for id, embedding in self.vectors.items():
            similarity = self.cosine_similarity(query_embedding, embedding)
            similarities.append((id, similarity, self.metadata[id]))

        # Sort by similarity score in descending order and get the top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [{"id": id, "similarity": similarity, "metadata": meta} for id, similarity, meta in similarities[:top_k]]

    def delete(self, id: str) -> None:
        """
        Delete a vector and its associated metadata from the store.

        Args:
            id (str): The unique identifier for the vector to be deleted.
        """
        if id in self.vectors:
            del self.vectors[id]
            del self.metadata[id]

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate the cosine similarity between two vectors.

        Args:
            vec_a (List[float]): The first vector.
            vec_b (List[float]): The second vector.

        Returns:
            float: The cosine similarity score between the two vectors.
        """
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm
```

---

## Domain: `rag_chunk`

**Prompt (truncated):** *Context: LlamaIndex is a data framework for LLM applications. It provides tools for ingesting, indexing, and querying da...*

| max_tokens | Used | Utilisation | finish_reason | Truncated | Cost USD |
|------------|------|-------------|---------------|-----------|----------|
| 50 | 50 | 100.0% | `length` | **YES ⚠** | `$0.000051` |
| 150 | 51 | 34.0% | `stop` | no | `$0.000052` |
| 300 | 51 | 17.0% | `stop` | no | `$0.000052` |
| 600 | 51 | 8.5% | `stop` | no | `$0.000052` |

### `max_tokens=50` — ⚠ TRUNCATED

```
The core components of LlamaIndex include data connectors (called Readers), indexes (VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex), query engines, and agent tools. It supports vector databases such as Pinecone, Weaviate, and Chroma
```

### `max_tokens=150` — ✓ Complete

```
The core components of LlamaIndex include data connectors (called Readers), indexes (VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex), query engines, and agent tools. It supports vector databases such as Pinecone, Weaviate, and Chroma.
```

### `max_tokens=300` — ✓ Complete

```
The core components of LlamaIndex include data connectors (called Readers), indexes (VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex), query engines, and agent tools. It supports vector databases such as Pinecone, Weaviate, and Chroma.
```

### `max_tokens=600` — ✓ Complete

```
The core components of LlamaIndex include data connectors (called Readers), indexes (VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex), query engines, and agent tools. It supports vector databases such as Pinecone, Weaviate, and Chroma.
```

---

## Global Summary

| Domain | Budget | Used | finish_reason | Truncated | Cost |
|--------|--------|------|---------------|-----------|------|
| explanation | 50 | 50 | `length` | YES ⚠ | `$0.000039` |
| explanation | 150 | 150 | `length` | YES ⚠ | `$0.000099` |
| explanation | 300 | 300 | `length` | YES ⚠ | `$0.000189` |
| explanation | 600 | 600 | `length` | YES ⚠ | `$0.000369` |
| summarisation | 50 | 50 | `length` | YES ⚠ | `$0.000049` |
| summarisation | 150 | 85 | `stop` | no | `$0.000070` |
| summarisation | 300 | 89 | `stop` | no | `$0.000072` |
| summarisation | 600 | 100 | `stop` | no | `$0.000079` |
| code | 50 | 50 | `length` | YES ⚠ | `$0.000040` |
| code | 150 | 150 | `length` | YES ⚠ | `$0.000100` |
| code | 300 | 300 | `length` | YES ⚠ | `$0.000190` |
| code | 600 | 600 | `length` | YES ⚠ | `$0.000370` |
| rag_chunk | 50 | 50 | `length` | YES ⚠ | `$0.000051` |
| rag_chunk | 150 | 51 | `stop` | no | `$0.000052` |
| rag_chunk | 300 | 51 | `stop` | no | `$0.000052` |
| rag_chunk | 600 | 51 | `stop` | no | `$0.000052` |

**Total estimated cost:** `$0.00187`  
**Truncated responses:** `10/16`
