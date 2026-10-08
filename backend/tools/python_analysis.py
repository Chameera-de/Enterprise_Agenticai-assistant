from collections import Counter
from backend.security.rbac import authorize
async def analyze_root_causes(records, role):
    if not authorize(role,'python_analysis'): raise PermissionError('tool denied')
    return Counter(c for r in records for c in r.get('root_causes',[])).most_common()
