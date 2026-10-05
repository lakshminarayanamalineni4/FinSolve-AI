## Can you explain what an embedding is, how you generate embeddings in your FinSolve AI project, and what happens when you convert a document chunk or user query into an embedding?

An embedding is a numerical representation of text in the form of a vector. Embeddings capture the semantic meaning of text, allowing us to compare the similarity between different pieces of content.

In FinSolve AI, we use an embedding model such as Qwen/Qwen3-Embedding-0.6B to convert document chunks into vectors. These vectors are stored in a vector database such as Qdrant, along with metadata like document ID and access-control information.

When a user submits a question, we convert the question into an embedding using the same model. We then perform a similarity search against the stored vectors to retrieve semantically relevant chunks. In our application, access-control filters ensure that only authorized documents are retrieved.

Important project-specific point

Your actual FinSolve AI implementation uses Qwen embeddings and Qdrant, so focus on those in the interview rather than listing FAISS, ChromaDB, and other tools unless you are specifically asked about alternatives.