"""Ingest sample JSON documents into Pinecone with access metadata.
Run after setting OPENAI_API_KEY, PINECONE_API_KEY and PINECONE_INDEX.
"""
import os, asyncio
from backend.rag.store import load_docs

async def main():
    from pinecone import Pinecone, ServerlessSpec
    from langchain_openai import OpenAIEmbeddings
    pc=Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    name=os.environ.get('PINECONE_INDEX','enterprise-ai-assistant')
    model=os.environ.get('EMBEDDING_MODEL','text-embedding-3-small')
    emb=OpenAIEmbeddings(model=model)
    docs=load_docs(); vectors=await emb.aembed_documents([d['text'] for d in docs])
    existing={x['name'] for x in pc.list_indexes()}
    if name not in existing:
        pc.create_index(name=name,dimension=len(vectors[0]),metric='cosine',spec=ServerlessSpec(cloud='aws',region=os.environ.get('PINECONE_REGION','us-east-1')))
    index=pc.Index(name); ns=os.environ.get('PINECONE_NAMESPACE','enterprise-kb')
    rows=[]
    for i,(d,v) in enumerate(zip(docs,vectors)):
        rows.append({'id':f'doc-{i}','values':v,'metadata':{'text':d['text'],'source':d.get('source',f'doc-{i}'),'access_level':d.get('access_level','internal'),'department':d.get('department','unknown'),'document_type':d.get('document_type','unknown')}})
    index.upsert(vectors=rows,namespace=ns)
    print(f'Ingested {len(rows)} documents into {name}/{ns}')
if __name__=='__main__': asyncio.run(main())
