## How would you decide the chunk size and chunk overlap for a RAG system? What problems can occur if chunks are too small or too large?

I would initially determine chunk size based on the document structure and content, such as headings, sections, paragraphs, and logical boundaries. I would also use chunk overlap so that important information near chunk boundaries is not lost.

There isn't one universally correct chunk size. I would evaluate retrieval quality using representative queries and adjust it accordingly.

If chunks are too small, we may lose the context required to answer a question. If they are too large, each chunk may contain too much unrelated information, which can reduce retrieval precision and increase token usage, latency, and cost.

So I would tune both chunk size and overlap based on retrieval evaluation rather than choosing a value purely as a rule of thumb.



If you're missing relevant information, the cause could instead be:

Poor chunking → adjust chunk size/overlap

Relevant chunk exists but ranks too low → adjust K/retrieval

Semantic mismatch → improve embedding/query processing

Exact keyword problem → hybrid search

RBAC metadata filter excludes it → fix authorization/filtering