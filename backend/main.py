from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import uuid4
from backend.graph.workflow import run_graph, LANGGRAPH_AVAILABLE
from backend.middleware.rate_limiter import TokenBucket
from backend.memory.session import memory
import os

app=FastAPI(title='Enterprise Agentic AI Assistant',version='2.0.0')
limiter=TokenBucket()
class ChatRequest(BaseModel):
    user_id:str=Field(min_length=1,max_length=64)
    role:str='viewer'
    query:str=Field(min_length=1,max_length=5000)

@app.get('/health')
async def health():
    return {'status':'ok','langgraph':LANGGRAPH_AVAILABLE,'pinecone_configured':bool(os.getenv('PINECONE_API_KEY') and os.getenv('PINECONE_INDEX')),'langsmith_configured':bool(os.getenv('LANGSMITH_API_KEY')),'llm_configured':bool(os.getenv('OPENAI_API_KEY'))}

@app.post('/chat')
async def chat(req:ChatRequest):
    if req.role not in {'viewer','analyst','administrator'}: raise HTTPException(403,'Invalid role')
    if not limiter.allow(req.user_id): raise HTTPException(429,'Rate limit exceeded; retry shortly')
    memory.add(req.user_id,'user',req.query)
    state={'request_id':str(uuid4()),'user_id':req.user_id,'role':req.role,'query':req.query,'events':[],'errors':[],'memory_context':memory.get(req.user_id)}
    try:
        result=await run_graph(state)
        memory.add(req.user_id,'assistant',result.get('answer',''))
        result['memory_turns']=len(memory.get(req.user_id))
        return result
    except Exception as e:
        raise HTTPException(503,f'Graceful degradation: {type(e).__name__}')
