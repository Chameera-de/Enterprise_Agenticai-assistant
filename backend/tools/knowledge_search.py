from backend.rag.store import load_docs
from backend.rag.hybrid import hybrid_search
from backend.security.rbac import authorize, metadata_filter
async def knowledge_search(query, role):
    if not authorize(role,'knowledge_search'): raise PermissionError('tool denied')
    return hybrid_search(query,load_docs(),metadata_filter=metadata_filter(role))
