Chunk overlap means repeating a portion of one chunk at the boundary of the next chunk. It helps preserve context when a sentence, paragraph, or piece of information spans across two chunks. Without overlap, important context at the boundary could be split between chunks, and retrieving only one of them might not provide enough information to answer the question.

Simple example

Suppose we have:

Chunk 1:
Employees can apply for annual leave after completing

Chunk 2:
three months of continuous service.

Without overlap, retrieving only Chunk 2 gives:

"three months of continuous service."

The meaning is incomplete.

With overlap:

Chunk 1:
Employees can apply for annual leave after completing

Chunk 2:
after completing three months of continuous service.

Now the second chunk retains enough context to be meaningful on its own.

One interview point to remember

Chunk size controls how much content is in each chunk.

Chunk overlap preserves context between neighboring chunks.