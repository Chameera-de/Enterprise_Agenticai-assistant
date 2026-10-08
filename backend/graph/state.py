from typing import TypedDict, Literal, Any
class AgentState(TypedDict, total=False):
    request_id: str
    user_id: str
    role: Literal['viewer','analyst','administrator']
    query: str
    intent: Literal['retrieval','research','analysis']
    plan: list[str]
    retrieved: list[dict[str, Any]]
    analysis: dict[str, Any]
    answer: str
    citations: list[str]
    events: list[dict[str, Any]]
    errors: list[str]
    validation: dict[str, Any]
    blocked: bool
