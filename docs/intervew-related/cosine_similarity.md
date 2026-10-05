## What is cosine similarity, and how does it help Qdrant determine which document chunks are relevant to a user's query?

Cosine similarity measures how similar two embedding vectors are based on the angle between them. In FinSolve AI, we first convert the user's question into an embedding and compare that query vector with the stored document-chunk embeddings in Qdrant. Qdrant calculates the similarity between them and ranks the chunks based on their similarity to the query. The highest-ranked chunks are then selected as the top-K relevant context for the RAG pipeline.

