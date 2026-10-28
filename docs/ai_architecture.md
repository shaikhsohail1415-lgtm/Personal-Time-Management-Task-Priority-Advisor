# AI Architecture

The natural-language path uses LangChain's ChatPromptTemplate and LangChain OpenAI integration. The LLM is configured with Pydantic structured output (`with_structured_output`) so the response becomes validated task objects instead of unstructured text.

A separate LangChain explanation chain receives the actual fuzzy results as JSON. It is explicitly instructed not to recalculate or invent the scores.
