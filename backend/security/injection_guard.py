import re
PATTERNS = [
    r'ignore (all|any|the|previous) .*instructions', r'reveal .*system prompt',
    r'exfiltrat', r'dump .*secret', r'bypass .*authorization', r'api[_ -]?key'
]

def inspect_text(text: str) -> tuple[bool, list[str]]:
    hits = [p for p in PATTERNS if re.search(p, text, re.I)]
    return (len(hits) == 0, hits)
