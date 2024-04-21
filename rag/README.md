# RAG stuff

#### Resources
- [Building Production-Ready RAG Applications: Jerry Liu](https://youtu.be/TRjq7t2Ms5I?feature=shared)


## Evaluation

- need to know the task well enough to be able to specify performance-measuring criteria
- components: retrieval, synthesis, e2e

### Retrieval

- evaluation dataset
- input: user query
- output: ground truth - documents relevant to the query
- run retriever on the evaluation dataset
- measure ranking metrics:
    - hit rate
    - success rate
    - MRR (MMR?)

### E2E

- LLM evaluation methods & criteria (TODO: get to know about it more)


## Optimization

### Data quality

- better parsing
    - how about asking an LLM about splitting the text into chunks each having a coherent content?
- chunk sizes
    - tuning
- metadata filters
    - summary of adjacent chunks
    - questions that are answerable (at least partially) by the chunk
    - related: for example, filtering by text content
- hybrid search

### Retrieval

- small-to-big technique
- embed sentences and then expand the context window after retrieval
- embed chunk summary, but pass the raw chunk to the synthesis phase

### Multi-document agents (advanced)

- chain-of-thought
- modeling each document as a separate agent with query-answering capability

### Fine-tuning (advanced)

- embeddings for the specific dataset
    - generate synthetic query dataset using LLMs
    - use that dataset to fine-tune the embedding model
- LLM for the specific dataset/use case
    - use a powerful LLM to generate syntethic dataset from raw chunks
    - fine-tune a "weaker" LLM
