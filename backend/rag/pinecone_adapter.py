from __future__ import annotations
import os

class PineconeRetriever:
    """Real Pinecone adapter. Returns None when credentials/index are not configured, enabling an offline demo."""
    def __init__(self):
        self.api_key=os.getenv('PINECONE_API_KEY'); self.index_name=os.getenv('PINECONE_INDEX')

    async def search(self, query: str, metadata_filter: dict, top_k: int=8):
        if not (self.api_key and self.index_name and os.getenv('OPENAI_API_KEY')): return None
        try:
            from pinecone import Pinecone
            from langchain_openai import OpenAIEmbeddings
            emb=OpenAIEmbeddings(model=os.getenv('EMBEDDING_MODEL','text-embedding-3-small'))
            vector=await emb.aembed_query(query)
            index=Pinecone(api_key=self.api_key).Index(self.index_name)
            ns=os.getenv('PINECONE_NAMESPACE','enterprise-kb')
            res=index.query(namespace=ns, vector=vector, top_k=top_k, include_metadata=True, filter=metadata_filter)
            out=[]
            for m in res.matches:
                md=m.metadata or {}
                out.append({'text':md.get('text',''),'source':md.get('source',m.id),'access_level':md.get('access_level','internal'),'score':float(m.score),'dense_score':float(m.score),'sparse_score':md.get('sparse_score',0.0)})
            return out
        except Exception:
            return None
