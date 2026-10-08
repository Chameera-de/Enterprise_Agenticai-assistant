# Final Submission Checklist

## Before demo recording
- [ ] Create public Git repository and push with meaningful commit history.
- [ ] `pytest -q` passes.
- [ ] `docker compose up --build` starts API and Streamlit.
- [ ] `/health` reports LangGraph available.
- [ ] Configure OpenAI (or chosen LLM) credentials.
- [ ] Create/configure Pinecone index and namespace; ingest sample/enterprise documents.
- [ ] Verify metadata filters prevent Viewer access to confidential content.
- [ ] Configure LangSmith and confirm traces contain graph transitions, retrieval and tool calls.
- [ ] Start MCP server and demonstrate at least one authorized MCP call.
- [ ] Run prompt-injection attack and show block/audit event.
- [ ] Run Viewer vs Analyst RBAC demonstration.
- [ ] Run broad payment-outage RLM scenario.
- [ ] Show citation validation and evidence attribution.
- [ ] Demonstrate graceful degradation by disabling one optional dependency/credential.

## Deliverables
- [ ] Public source repository URL.
- [ ] Architecture diagram (README Mermaid + export to PNG/PDF if desired).
- [ ] 45-minute public demo video URL.
- [ ] LangSmith traces visible in demo.
- [ ] Assumptions/trade-offs explained in demo.
- [ ] No secrets committed to Git.
