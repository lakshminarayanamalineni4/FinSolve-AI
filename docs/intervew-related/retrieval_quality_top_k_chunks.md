## Why do we retrieve Top-K chunks instead of sending all the documents from the vector database to the LLM?

We retrieve only the Top-K most relevant chunks instead of sending all documents because an enterprise knowledge base can contain a large amount of information, and most of it will not be relevant to a particular question.

By retrieving Top-K chunks, we provide the LLM with focused and relevant context. This reduces the amount of unnecessary information, helps the model stay within its context window, reduces token usage and cost, and can improve response quality and latency.

The value of K is also important. If K is too small, we may miss useful information; if it is too large, we may introduce unnecessary context. So K should be evaluated based on the application's retrieval requirements.


## Suppose the user asks: What is our company's leave policy for employees? Your vector search returns 5 chunks, but none of those chunks actually contain the leave policy. What should your RAG system do? Would you still ask the LLM to answer the question?

If the required information exists in the knowledge base but isn't being retrieved, I would first investigate the retrieval pipeline rather than immediately increasing K.

I would check whether the chunking strategy is appropriate, whether the query embedding is retrieving the expected semantic matches, and whether metadata or RBAC filters are excluding the relevant document.

If the relevant chunk is ranking just below the retrieval threshold, increasing Top-K could help. If the problem is caused by poor chunking, I would adjust the chunk size or overlap and re-index the documents. For exact terms or policy names, I could also consider hybrid retrieval or query rewriting.

Finally, I would evaluate these changes using a retrieval test set rather than assuming that a larger K or larger chunk size is always better.