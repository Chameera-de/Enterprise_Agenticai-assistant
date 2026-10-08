# Assumptions and trade-offs

- POC optimizes evaluator-visible architecture and correctness over UI styling.
- Pinecone is the required production vector database. Offline fallback exists only to make the demo reproducible without cloud credentials.
- Session memory stores conversation state; durable long-term memory is a bonus extension and should use an explicit consent/retention policy.
- RLM recursion is bounded by batch size/depth to control cost and butterfly-effect error propagation.
- Model-generated reasoning is not exposed verbatim. The UI exposes auditable agent states, plans, tools, retrieval counts and validation outcomes instead.
- External/MCP data is illustrative and should be replaced with enterprise services protected by independent authorization.
