# Security model

1. Authentication establishes user identity and role (POC uses explicit demo users/roles).
2. FastAPI validates request shape and applies per-user token-bucket rate limiting.
3. Injection guard rejects common instruction-override, secret-exfiltration and authorization-bypass attempts.
4. RBAC is deterministic application code. The LLM never grants itself tool access.
5. Retrieval applies access metadata before evidence enters model context.
6. Retrieved content is treated as untrusted data, not instructions.
7. Tool arguments require schema validation and authorization at execution time.
8. Final citations must resolve to retrieved authorized evidence; otherwise validation fails.
9. Secrets are environment variables and never stored in prompts or repository files.

For production, add SSO/OIDC (e.g. Keycloak), secret manager, network egress policy, audit retention, PII/DLP controls, signed tool identities and policy-as-code.
