## What is chunking in RAG? Why do we split documents into chunks instead of embedding the entire document as one vector?

Chunking is the process of splitting a large document into smaller, meaningful pieces before generating embeddings. We do this because a document may contain information about multiple topics, while a user's question may relate to only one specific part.

If we embed the entire document as one vector, the embedding represents the document at a broad level, which can reduce retrieval precision. With chunking, each chunk gets its own embedding, allowing the vector database to retrieve the specific sections that are semantically relevant to the user's question.

It also helps control the amount of context sent to the LLM, reducing unnecessary token usage, latency, and cost.

Think of the RAG flow like this

Large document

→ Split into meaningful chunks

→ Generate one embedding per chunk

→ Store chunks + embeddings + metadata

→ User asks question

→ Generate query embedding

→ Similarity search

→ Retrieve relevant Top-K chunks

→ Send those chunks to LLM

This is an important distinction to remember:

Chunking improves the granularity of retrieval. Top-K controls how much retrieved context we pass forward.