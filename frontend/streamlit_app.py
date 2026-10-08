import streamlit as st, httpx
st.set_page_config(page_title='Enterprise AI Assistant',layout='wide')
st.title('Enterprise AI Assistant')
st.caption('Agentic enterprise RAG • LangGraph • RBAC • RLM • grounded citations')
if 'messages' not in st.session_state: st.session_state.messages=[]
role=st.sidebar.selectbox('Demo role',['viewer','analyst','administrator'])
api=st.sidebar.text_input('FastAPI URL','http://localhost:8000')
try:
    health=httpx.get(api+'/health',timeout=2).json()
    st.sidebar.success('Backend online')
    st.sidebar.json(health)
except Exception: st.sidebar.warning('Backend not reachable yet')
for m in st.session_state.messages:
    with st.chat_message(m['role']): st.write(m['content'])
q=st.chat_input('Ask the organizational knowledge base…')
if q:
    st.session_state.messages.append({'role':'user','content':q})
    with st.chat_message('user'): st.write(q)
    try:
        with st.status('Agent workflow running…',expanded=True) as status:
            r=httpx.post(api+'/chat',json={'user_id':'demo-user','role':role,'query':q},timeout=60); r.raise_for_status(); data=r.json()
            for e in data.get('events',[]):
                st.write(f"**{e['node']}** — {e['message']}")
            status.update(label='Workflow complete',state='complete')
        with st.chat_message('assistant'): st.write(data['answer'])
        st.session_state.messages.append({'role':'assistant','content':data['answer']})
        c1,c2=st.columns(2)
        with c1:
            st.subheader('Evidence')
            for c in data.get('citations',[]): st.code(c)
        with c2:
            st.subheader('Validation')
            st.json(data.get('validation',{}))
            st.caption(f"Session memory turns: {data.get('memory_turns',0)}")
        with st.expander('Research plan / analysis'):
            st.write(data.get('plan',[])); st.json(data.get('analysis',{}))
    except Exception as e: st.error(str(e))
