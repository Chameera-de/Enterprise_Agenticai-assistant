import re, math
from collections import Counter

def _tokens(s): return re.findall(r'[a-z0-9]+', s.lower())
def _sparse(q, text):
    q,c=Counter(_tokens(q)),Counter(_tokens(text)); return sum(min(c[t],n) for t,n in q.items())/(sum(q.values()) or 1)
def _dense_proxy(q,text):
    # Offline POC proxy. Production adapter uses Pinecone embeddings.
    a,b=set(_tokens(q)),set(_tokens(text)); return len(a&b)/math.sqrt(max(1,len(a))*max(1,len(b)))

def hybrid_search(query, docs, alpha=.55, top_k=6, metadata_filter=None):
    out=[]
    for d in docs:
        if metadata_filter and '$in' in metadata_filter.get('access_level',{}):
            if d.get('access_level') not in metadata_filter['access_level']['$in']: continue
        dense=_dense_proxy(query,d['text']); sparse=_sparse(query,d['text'])
        out.append({**d,'dense_score':dense,'sparse_score':sparse,'score':alpha*dense+(1-alpha)*sparse})
    return sorted(out,key=lambda x:x['score'],reverse=True)[:top_k]
