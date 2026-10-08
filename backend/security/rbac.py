ROLE_TOOLS = {
    'viewer': {'knowledge_search'},
    'analyst': {'knowledge_search', 'python_analysis', 'mcp_lookup'},
    'administrator': {'knowledge_search', 'python_analysis', 'mcp_lookup', 'admin_tool'},
}

def authorize(role: str, tool: str) -> bool:
    return tool in ROLE_TOOLS.get(role, set())

def metadata_filter(role: str) -> dict:
    # Enforced before retrieval, not delegated to the LLM.
    if role == 'viewer':
        return {'access_level': {'$in': ['public', 'internal']}}
    if role == 'analyst':
        return {'access_level': {'$in': ['public', 'internal', 'confidential']}}
    return {}
