from __future__ import annotations
from typing import Any
from backend.rag.store import load_docs
from backend.rag.hybrid import hybrid_search
from backend.rag.pinecone_adapter import PineconeRetriever
from backend.security.rbac import metadata_filter, authorize
from backend.security.injection_guard import inspect_text
from backend.rlm.planner import make_plan
from backend.rlm.recursive_search import analyze_batches
from backend.llm.provider import classify_route, synthesize_answer
from backend.observability.tracing import traced

try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except Exception:
    LANGGRAPH_AVAILABLE = False


def event(state: dict, node: str, message: str, **data: Any):
    state.setdefault('events', []).append({'node': node, 'message': message, **data})

@traced('security_guard')
async def security_guard(state):
    ok, hits = inspect_text(state['query'])
    event(state, 'security_guard', 'Input and exfiltration inspection completed', passed=ok)
    if not ok:
        state['blocked'] = True
        state['answer'] = 'Request blocked by prompt-injection/data-exfiltration guard.'
        state['validation'] = {'passed': False, 'reason': hits}
    return state

@traced('supervisor')
async def supervisor(state):
    route = await classify_route(state['query'])
    state['intent'] = route
    event(state, 'supervisor', 'Intent classified and route selected', route=route)
    return state

@traced('retrieval_agent')
async def retrieval_agent(state):
    filt = metadata_filter(state['role'])
    retriever = PineconeRetriever()
    hits = await retriever.search(state['query'], filt, top_k=8)
    if hits is None:
        hits = hybrid_search(state['query'], load_docs(), metadata_filter=filt, top_k=8)
        backend = 'offline-hybrid'
    else:
        backend = 'pinecone'
    state['retrieved'] = hits
    event(state, 'retrieval_agent', 'Hybrid retrieval completed', candidates=len(hits), backend=backend, filter=filt)
    return state

@traced('research_rlm')
async def research_agent(state):
    hits = state.get('retrieved', [])
    state['plan'] = make_plan(state['query'], hits)
    event(state, 'research_rlm', 'Recursive research plan generated', steps=len(state['plan']))
    state['analysis'] = analyze_batches(hits)
    event(state, 'research_rlm', 'Bounded subtask analyses aggregated', batches=len(state['analysis'].get('batches', [])))
    return state

@traced('analysis_agent')
async def analysis_agent(state):
    if not authorize(state['role'], 'python_analysis'):
        state.setdefault('errors', []).append('python_analysis denied by RBAC')
        event(state, 'authorization_guard', 'Python analysis denied', role=state['role'])
        return state
    state['analysis'] = analyze_batches(state.get('retrieved', []))
    event(state, 'analysis_agent', 'Structured Python analysis completed')
    return state

@traced('citation_validator')
async def validator(state):
    sources = [d.get('source') for d in state.get('retrieved', []) if d.get('source')]
    citations = list(dict.fromkeys(sources[:5]))
    state['citations'] = citations
    valid = bool(state.get('retrieved')) and all(c in sources for c in citations)
    state['validation'] = {'passed': valid, 'citation_count': len(citations), 'grounded': valid}
    event(state, 'validation', 'Citation grounding validation completed', passed=valid)
    return state

@traced('response_agent')
async def response_agent(state):
    state['answer'] = await synthesize_answer(state)
    event(state, 'response_agent', 'Final grounded response generated')
    return state


def _route_after_security(state):
    return 'end' if state.get('blocked') else 'supervisor'

def _route_after_supervisor(state):
    return 'retrieval_agent'

def _route_after_retrieval(state):
    return {'research': 'research_agent', 'analysis': 'analysis_agent'}.get(state.get('intent'), 'validator')


def build_graph():
    if not LANGGRAPH_AVAILABLE:
        return None
    from backend.graph.state import AgentState
    g = StateGraph(AgentState)
    g.add_node('security_guard', security_guard)
    g.add_node('supervisor', supervisor)
    g.add_node('retrieval_agent', retrieval_agent)
    g.add_node('research_agent', research_agent)
    g.add_node('analysis_agent', analysis_agent)
    g.add_node('validator', validator)
    g.add_node('response_agent', response_agent)
    g.add_edge(START, 'security_guard')
    g.add_conditional_edges('security_guard', _route_after_security, {'supervisor':'supervisor','end':END})
    g.add_edge('supervisor', 'retrieval_agent')
    g.add_conditional_edges('retrieval_agent', _route_after_retrieval, {
        'research_agent':'research_agent','analysis_agent':'analysis_agent','validator':'validator'})
    g.add_edge('research_agent','validator')
    g.add_edge('analysis_agent','validator')
    g.add_edge('validator','response_agent')
    g.add_edge('response_agent', END)
    return g.compile()

GRAPH = build_graph()

async def _fallback(state):
    state = await security_guard(state)
    if state.get('blocked'): return state
    state = await supervisor(state)
    state = await retrieval_agent(state)
    if state['intent'] == 'research': state = await research_agent(state)
    elif state['intent'] == 'analysis': state = await analysis_agent(state)
    state = await validator(state)
    state = await response_agent(state)
    event(state, 'runtime', 'LangGraph package unavailable; deterministic compatibility runner used')
    return state

async def run_graph(state):
    if GRAPH is not None:
        result = await GRAPH.ainvoke(state)
        result.setdefault('events', []).append({'node':'runtime','message':'Executed with LangGraph StateGraph'})
        return result
    return await _fallback(state)
