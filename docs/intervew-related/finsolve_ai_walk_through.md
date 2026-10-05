## Can you explain your FinSolve AI project and walk me through what happens when a user asks a question?

"FinSolve AI is an enterprise RAG assistant that combines secure access control with retrieval-augmented generation.

When a user asks a question, the request first goes through authentication using JWT, and we determine the user's permissions through our RBAC system. These permissions are used to restrict which resources the user can retrieve.

We then process the query and generate an embedding for it. We perform semantic similarity search against the vector database, applying metadata-based filters so that only documents the user is authorized to access are considered. We retrieve the top-K relevant chunks along with their metadata.

Next, we build the LLM prompt using the user's original question, the retrieved context, and instructions that control how the model should generate the response. The prompt is then sent through our LLM abstraction layer to the configured LLM.

Finally, the model generates a grounded response based on the retrieved enterprise context, and we can provide source attribution for the information used."**


## Why do you need embeddings and a vector database? Why can't you just search the documents using SQL or normal keyword search

"Traditional SQL or keyword-based search primarily relies on matching terms between the query and the documents. It can struggle when the user expresses a concept using different words from those in the document.

Semantic search addresses this by using an embedding model to convert the query and document chunks into numerical vectors. We can then compare the vectors using a similarity metric, such as cosine similarity, to retrieve content that is semantically related to the user's question.

In FinSolve AI, we use embeddings and a vector database to retrieve relevant enterprise knowledge, which we then provide as context to the LLM for generating a grounded response.

However, keyword search still has value, so a hybrid retrieval approach can combine both methods when necessary."