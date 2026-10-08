import os
try:
    from langsmith import traceable
except Exception:
    traceable=None

def traced(name):
    def deco(fn):
        if traceable and os.getenv('LANGSMITH_TRACING','').lower() in {'true','1'}:
            return traceable(name=name, run_type='chain')(fn)
        return fn
    return deco
