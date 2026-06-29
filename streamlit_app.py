"""
Deep Agents Chatbot — Streamlit App
Showcases all features from the deepagentsdemo notebooks:
  1. Basic Deep Agent (with Tavily web search)
  2. Context Engineering (system prompts + AGENTS.md memory)
  3. Backends (State / Filesystem / Store)
  4. Subagents (specialized research sub-agents)
"""

import os
import uuid
import html as html_module
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Agent Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
  --bg:#0d0f1a; --card:#13172b; --border:#1e2240;
  --a1:#6c63ff; --a2:#3ecfcf; --a3:#ff6584; --a4:#f9c74f;
  --txt:#e8eaf6; --muted:#7986cb; --ok:#4ade80; --err:#f87171;
}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;font-family:'Inter',sans-serif;color:var(--txt);}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d0f1a,#111628)!important;border-right:1px solid var(--border)!important;}
.main .block-container{padding-top:1.5rem;max-width:1100px;}
.hero{background:linear-gradient(135deg,#1a1040,#0d2340,#0d1a2e);border:1px solid var(--border);border-radius:20px;padding:2rem 2.5rem;margin-bottom:1.5rem;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at 30% 40%,rgba(108,99,255,.12),transparent 55%),radial-gradient(ellipse at 70% 60%,rgba(62,207,207,.09),transparent 55%);pointer-events:none;}
.hero-title{font-size:2.4rem;font-weight:700;background:linear-gradient(135deg,#a78bfa,#38bdf8,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:.4rem;}
.hero-sub{color:var(--muted);font-size:1rem;}
.badge-row{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;}
.badge{padding:.3rem .75rem;border-radius:20px;font-size:.75rem;font-weight:600;}
.bp{background:rgba(108,99,255,.2);color:#a78bfa;border:1px solid rgba(108,99,255,.35);}
.bt{background:rgba(62,207,207,.2);color:#2dd4bf;border:1px solid rgba(62,207,207,.35);}
.br{background:rgba(255,101,132,.2);color:#fb7185;border:1px solid rgba(255,101,132,.35);}
.ba{background:rgba(249,199,79,.2);color:#fbbf24;border:1px solid rgba(249,199,79,.35);}
.bg{background:rgba(74,222,128,.2);color:#4ade80;border:1px solid rgba(74,222,128,.35);}
.chat-wrap{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:1.2rem;min-height:400px;max-height:560px;overflow-y:auto;margin-bottom:1rem;}
.msg-user{background:linear-gradient(135deg,rgba(108,99,255,.25),rgba(108,99,255,.1));border:1px solid rgba(108,99,255,.35);border-radius:14px 14px 4px 14px;padding:.85rem 1.1rem;margin:.55rem 0 .55rem 15%;color:var(--txt);font-size:.95rem;line-height:1.6;}
.msg-bot{background:linear-gradient(135deg,rgba(62,207,207,.12),rgba(62,207,207,.05));border:1px solid rgba(62,207,207,.25);border-radius:14px 14px 14px 4px;padding:.85rem 1.1rem;margin:.55rem 15% .55rem 0;color:var(--txt);font-size:.95rem;line-height:1.6;}
.lbl{font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;margin-bottom:.35rem;}
.lu{color:#a78bfa;}.la{color:#2dd4bf;}
.tool-chip{display:inline-block;background:rgba(249,199,79,.15);border:1px solid rgba(249,199,79,.3);color:#fbbf24;border-radius:20px;padding:.2rem .65rem;font-size:.72rem;font-weight:600;margin-bottom:.5rem;}
.pill-ok{display:inline-block;padding:.2rem .6rem;border-radius:20px;font-size:.72rem;font-weight:600;background:rgba(74,222,128,.15);color:#4ade80;border:1px solid rgba(74,222,128,.3);}
.pill-err{display:inline-block;padding:.2rem .6rem;border-radius:20px;font-size:.72rem;font-weight:600;background:rgba(248,113,113,.15);color:#f87171;border:1px solid rgba(248,113,113,.3);}
.sec{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:1rem 0 .4rem;display:flex;align-items:center;gap:.5rem;}
.sec::after{content:'';flex:1;height:1px;background:var(--border);}
.info-box{background:rgba(62,207,207,.07);border:1px solid rgba(62,207,207,.2);border-radius:10px;padding:.75rem 1rem;font-size:.82rem;color:#94e4e4;line-height:1.5;margin:.5rem 0;}
.warn-box{background:rgba(249,199,79,.07);border:1px solid rgba(249,199,79,.2);border-radius:10px;padding:.75rem 1rem;font-size:.82rem;color:#fbbf24;line-height:1.5;margin:.5rem 0;}
.file-viewer{background:#080a12;border:1px solid var(--border);border-radius:10px;padding:.75rem 1rem;font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#a5b4fc;line-height:1.6;overflow-x:auto;white-space:pre-wrap;word-break:break-all;}
.stButton>button{background:linear-gradient(135deg,#6c63ff,#38bdf8)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-weight:600!important;padding:.55rem 1.2rem!important;font-size:.9rem!important;width:100%;}
.stButton>button:hover{opacity:.9!important;transform:translateY(-1px)!important;}
.stSelectbox [data-baseweb="select"]>div,.stTextInput input,.stTextArea textarea{background:#0d0f1a!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--txt)!important;}
::-webkit-scrollbar{width:5px;height:5px;}::-webkit-scrollbar-track{background:transparent;}::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px;}
#MainMenu,footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────
_DEFAULTS = dict(
    messages=[], agent=None, virtual_files={},
    thread_id=str(uuid.uuid4()), store=None,
    selected_backend="State (in-memory)",
    selected_model="groq:meta-llama/llama-4-scout-17b-16e-instruct",
    use_web_search=True, use_subagents=True, use_memory=False,
    system_prompt=(
        "You are a highly capable Deep Agent research assistant. "
        "Plan tasks carefully, delegate to subagents when helpful, "
        "and provide thorough, well-structured answers."
    ),
    agents_md="", error=None, fs_root="./agent_workspace",
)
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────
# Agent factory
# ──────────────────────────────────────────────
def build_agent():
    from deepagents import create_deep_agent
    from langgraph.checkpoint.memory import MemorySaver

    tools = []
    if st.session_state.use_web_search:
        try:
            from tavily import TavilyClient
            from typing import Literal
            key = os.getenv("TAVILY_API_KEY", "")
            if key:
                _tv = TavilyClient(api_key=key)
                def internet_search(
                    query: str,
                    max_results: int = 5,
                    topic: Literal["general","news","finance"] = "general",
                    include_raw_content: bool = False,
                ):
                    """Run a web search."""
                    return _tv.search(query, max_results=max_results,
                                      include_raw_content=include_raw_content, topic=topic)
                tools.append(internet_search)
        except Exception:
            pass

    subagents = []
    if st.session_state.use_subagents:
        subagents = [
            {
                "name": "research-agent",
                "description": "Deep-dive research assistant. Use for thorough, multi-source research on any topic.",
                "system_prompt": "You are an expert research analyst. Gather comprehensive information and return a detailed, structured report.",
                "tools": tools,
                "model": st.session_state.selected_model,
            },
            {
                "name": "writer-agent",
                "description": "Professional writer. Delegate when the user needs polished documents, summaries, or reports.",
                "system_prompt": "You are a professional technical writer. Produce clear, polished prose with headings and structure.",
                "tools": [],
                "model": st.session_state.selected_model,
            },
        ]

    sys_prompt = st.session_state.system_prompt
    if st.session_state.agents_md.strip():
        sys_prompt += "\n\n---\n## Project Context (AGENTS.md)\n\n" + st.session_state.agents_md

    checkpointer = MemorySaver() if st.session_state.use_memory else None

    try:
        backend_name = st.session_state.selected_backend
        if backend_name == "State (in-memory)":
            from deepagents.backends import StateBackend
            backend = StateBackend()
        elif backend_name == "Filesystem (disk)":
            from deepagents.backends import FilesystemBackend
            root = st.session_state.fs_root
            os.makedirs(root, exist_ok=True)
            backend = FilesystemBackend(root_dir=root, virtual_mode=True)
        else:
            from langgraph.store.memory import InMemoryStore
            from deepagents.backends import StoreBackend
            if st.session_state.store is None:
                st.session_state.store = InMemoryStore()
            backend = StoreBackend(namespace=lambda rt: ("deep-agent-studio",))

        kwargs = dict(
            model=st.session_state.selected_model,
            tools=tools,
            subagents=subagents or None,
            system_prompt=sys_prompt,
            backend=backend,
        )
        if checkpointer:
            kwargs["checkpointer"] = checkpointer
        if backend_name == "Store (cross-thread)" and st.session_state.store:
            kwargs["store"] = st.session_state.store

        agent = create_deep_agent(**kwargs)
        st.session_state.agent = agent
        st.session_state.error = None
        return agent
    except Exception as exc:
        st.session_state.error = str(exc)
        return None


def get_agent():
    if st.session_state.agent is None:
        return build_agent()
    return st.session_state.agent

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:.5rem 0 1rem">
      <div style="font-size:2.2rem">🤖</div>
      <div style="font-size:1.1rem;font-weight:700;color:#a78bfa">Deep Agent Studio</div>
      <div style="font-size:.72rem;color:#7986cb;margin-top:.2rem">Full-featured chatbot demo</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec">🧠 Model</div>', unsafe_allow_html=True)
    MODEL_OPTS = [
        "groq:meta-llama/llama-4-scout-17b-16e-instruct",
        "groq:qwen/qwen3-32b",
        "groq:qwen/qwen3.6-27b",
        "openai:gpt-4o",
        "openai:gpt-4o-mini",
    ]
    sel_model = st.selectbox("Model", MODEL_OPTS,
        index=MODEL_OPTS.index(st.session_state.selected_model)
              if st.session_state.selected_model in MODEL_OPTS else 0,
        label_visibility="collapsed")
    if sel_model != st.session_state.selected_model:
        st.session_state.selected_model = sel_model; st.session_state.agent = None

    st.markdown('<div class="sec">💾 Backend</div>', unsafe_allow_html=True)
    BACKEND_OPTS = ["State (in-memory)", "Filesystem (disk)", "Store (cross-thread)"]
    BACKEND_DESC = {
        "State (in-memory)": "Files live in LangGraph state. Ephemeral — reset each conversation.",
        "Filesystem (disk)": "Files written to real disk. Persists across restarts.",
        "Store (cross-thread)": "Files in a shared store, accessible from any thread.",
    }
    sel_backend = st.selectbox("Backend", BACKEND_OPTS,
        index=BACKEND_OPTS.index(st.session_state.selected_backend)
              if st.session_state.selected_backend in BACKEND_OPTS else 0,
        label_visibility="collapsed")
    if sel_backend != st.session_state.selected_backend:
        st.session_state.selected_backend = sel_backend
        st.session_state.virtual_files = {}; st.session_state.agent = None

    st.markdown(f'<div class="info-box">ℹ️ {BACKEND_DESC[sel_backend]}</div>', unsafe_allow_html=True)

    if sel_backend == "Filesystem (disk)":
        fs_root = st.text_input("Root dir", value=st.session_state.fs_root, label_visibility="collapsed")
        if fs_root != st.session_state.fs_root:
            st.session_state.fs_root = fs_root; st.session_state.agent = None

    st.markdown('<div class="sec">⚡ Features</div>', unsafe_allow_html=True)
    ws = st.toggle("🌐 Web Search (Tavily)", value=st.session_state.use_web_search)
    if ws != st.session_state.use_web_search:
        st.session_state.use_web_search = ws; st.session_state.agent = None
    sa = st.toggle("🤝 Sub-Agents", value=st.session_state.use_subagents)
    if sa != st.session_state.use_subagents:
        st.session_state.use_subagents = sa; st.session_state.agent = None
    mem = st.toggle("🧠 Persistent Memory", value=st.session_state.use_memory)
    if mem != st.session_state.use_memory:
        st.session_state.use_memory = mem; st.session_state.agent = None

    st.markdown('<div class="sec">📝 Context Engineering</div>', unsafe_allow_html=True)
    sys_p = st.text_area("System Prompt", value=st.session_state.system_prompt,
                          height=100, label_visibility="collapsed",
                          placeholder="Describe how the agent should behave…")
    if sys_p != st.session_state.system_prompt:
        st.session_state.system_prompt = sys_p; st.session_state.agent = None
    ag_md = st.text_area("AGENTS.md (optional)", value=st.session_state.agents_md,
                          height=90, label_visibility="collapsed",
                          placeholder="Paste AGENTS.md context file here…")
    if ag_md != st.session_state.agents_md:
        st.session_state.agents_md = ag_md; st.session_state.agent = None

    st.markdown('<div class="sec">🛠 Actions</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 Rebuild"):
            st.session_state.agent = None
            st.session_state.messages = []
            st.session_state.virtual_files = {}
            st.session_state.thread_id = str(uuid.uuid4())
            build_agent(); st.rerun()
    with c2:
        if st.button("🗑 Clear"):
            st.session_state.messages = []
            st.session_state.virtual_files = {}
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

    st.markdown('<div class="sec">📊 Status</div>', unsafe_allow_html=True)
    if st.session_state.agent:
        st.markdown('<span class="pill-ok">✅ Agent ready</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill-err">⚠ Not built</span>', unsafe_allow_html=True)
    if st.session_state.error:
        st.markdown(f'<div class="warn-box">⚠️ {html_module.escape(st.session_state.error)}</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Hero
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">🤖 Deep Agent Studio</div>
  <div class="hero-sub">Interactive chatbot demonstrating every feature from the Deep Agents notebooks.</div>
  <div class="badge-row">
    <span class="badge bp">📋 Planning (write_todos)</span>
    <span class="badge bt">🌐 Web Search</span>
    <span class="badge br">🤝 Subagents</span>
    <span class="badge ba">🧠 Context Engineering</span>
    <span class="badge bg">💾 Pluggable Backends</span>
    <span class="badge bp">📂 Virtual File System</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────
tab_chat, tab_files, tab_guide = st.tabs(["💬 Chat", "📂 File Explorer", "📖 Feature Guide"])

# ════════════════ CHAT ════════════════
with tab_chat:
    # Config bar
    cfg_cols = st.columns(5)
    cfg_items = [
        ("Model", st.session_state.selected_model.split(":")[-1], "#a78bfa"),
        ("Backend", st.session_state.selected_backend.split(" ")[0], "#2dd4bf"),
        ("Search", "ON" if st.session_state.use_web_search else "OFF",
         "#4ade80" if st.session_state.use_web_search else "#f87171"),
        ("SubAgents", "ON" if st.session_state.use_subagents else "OFF",
         "#4ade80" if st.session_state.use_subagents else "#f87171"),
        ("Memory", "ON" if st.session_state.use_memory else "OFF",
         "#4ade80" if st.session_state.use_memory else "#f87171"),
    ]
    for col, (label, val, color) in zip(cfg_cols, cfg_items):
        col.markdown(
            f"<div style='background:#0d0f1a;border:1px solid #1e2240;border-radius:10px;"
            f"padding:.5rem .75rem;text-align:center;'>"
            f"<div style='font-size:.65rem;color:#7986cb;font-weight:600;text-transform:uppercase'>{label}</div>"
            f"<div style='font-size:.85rem;color:{color};font-weight:700'>{val}</div></div>",
            unsafe_allow_html=True)

    st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)

    # Chat history
    chat_html = '<div class="chat-wrap" id="cw">'
    if not st.session_state.messages:
        chat_html += """
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    height:300px;color:#7986cb;gap:.75rem;text-align:center;">
          <div style="font-size:3rem">🤖</div>
          <div style="font-size:1rem;font-weight:600">Deep Agent is ready</div>
          <div style="font-size:.82rem">Try: <em>"Research the latest AI frameworks"</em> or
               <em>"Create a plan for learning Python"</em></div>
        </div>"""
    else:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = html_module.escape(msg["content"]).replace("\n", "<br>")
            is_user = (role == "user")
            css = "msg-user" if is_user else "msg-bot"
            lcss = "lu" if is_user else "la"
            lbl = "You" if is_user else "🤖 Deep Agent"
            tool_html = ""
            if not is_user and msg.get("used_tools"):
                tool_html = f'<div class="tool-chip">⚙️ {", ".join(msg["used_tools"])}</div><br>'
            chat_html += f'<div class="{css}"><div class="lbl {lcss}">{lbl}</div>{tool_html}<div>{content}</div></div>'
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)

    # Scroll
    st.markdown('<script>var cw=document.getElementById("cw");if(cw)cw.scrollTop=cw.scrollHeight;</script>',
                unsafe_allow_html=True)

    # Input
    inp_c, btn_c = st.columns([9, 1])
    with inp_c:
        user_input = st.text_input("Message", key="user_input",
                                   placeholder="Ask the Deep Agent anything…",
                                   label_visibility="collapsed")
    with btn_c:
        send = st.button("Send ➤", key="send_btn")

    # Quick prompts
    qps = [
        ("🔍", "Research LLM Gateways and summarise"),
        ("📋", "Create a 5-step learning plan for machine learning"),
        ("🌐", "What are the latest AI news today?"),
        ("📝", "Write a todo list and save it to /notes/demo.txt"),
    ]
    qcols = st.columns(4)
    clicked = None
    for col, (icon, text) in zip(qcols, qps):
        if col.button(f"{icon} {text[:28]}…" if len(text) > 28 else f"{icon} {text}", key=f"qp_{text[:15]}"):
            clicked = text

    # Process
    final = None
    if send and user_input.strip():
        final = user_input.strip()
    elif clicked:
        final = clicked

    if final:
        st.session_state.messages.append({"role": "user", "content": final})

        with st.spinner("🤖 Deep Agent is thinking…"):
            agent = get_agent()
            if agent is None:
                err = st.session_state.error or "Failed to build agent. Check the sidebar."
                st.session_state.messages.append({"role": "assistant", "content": f"⚠️ {err}", "used_tools": []})
            else:
                try:
                    payload = {"messages": [{"role": "user", "content": final}]}
                    if st.session_state.virtual_files:
                        payload["files"] = st.session_state.virtual_files

                    kwargs = {}
                    if st.session_state.use_memory:
                        kwargs["config"] = {"configurable": {"thread_id": st.session_state.thread_id}}

                    result = agent.invoke(payload, **kwargs)

                    reply = ""
                    used_tools = []
                    if "messages" in result:
                        for m in reversed(result["messages"]):
                            if hasattr(m, "content") and m.content and getattr(m, "type", "") != "tool":
                                reply = m.content if isinstance(m.content, str) else str(m.content)
                                break
                        for m in result["messages"]:
                            if hasattr(m, "tool_calls") and m.tool_calls:
                                for tc in m.tool_calls:
                                    n = tc.get("name","") if isinstance(tc, dict) else getattr(tc,"name","")
                                    if n and n not in used_tools:
                                        used_tools.append(n)
                    if not reply:
                        reply = str(result)

                    if "files" in result and result["files"]:
                        st.session_state.virtual_files.update(result["files"])

                    st.session_state.messages.append({"role": "assistant", "content": reply, "used_tools": used_tools})
                    st.session_state.error = None
                except Exception as exc:
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ Error: {exc}", "used_tools": []})
                    st.session_state.error = str(exc)

        st.rerun()

# ════════════════ FILE EXPLORER ════════════════
with tab_files:
    st.markdown("""
    <div style="margin-bottom:1rem">
      <div style="font-size:1.1rem;font-weight:700;color:#e8eaf6">📂 Virtual File System</div>
      <div style="font-size:.82rem;color:#7986cb;margin-top:.2rem">
        Files created by the agent. Ask the agent to <em>"create a file at /notes/todo.txt"</em> to see them here.
      </div>
    </div>""", unsafe_allow_html=True)

    if st.session_state.selected_backend == "Filesystem (disk)":
        root = Path(st.session_state.fs_root)
        if root.exists():
            disk_files = [f for f in root.rglob("*") if f.is_file()]
            if disk_files:
                st.markdown(f'<div class="info-box">Found {len(disk_files)} file(s) on disk at {root.resolve()}</div>', unsafe_allow_html=True)
                for fp in disk_files:
                    with st.expander(f"📄 {fp.relative_to(root)}"):
                        try:
                            st.markdown(f'<div class="file-viewer">{html_module.escape(fp.read_text())}</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(str(e))
            else:
                st.markdown('<div class="warn-box">No files on disk yet.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="warn-box">Root directory does not exist yet.</div>', unsafe_allow_html=True)
    elif st.session_state.virtual_files:
        for path, file_data in st.session_state.virtual_files.items():
            with st.expander(f"📄 {path}"):
                if isinstance(file_data, dict):
                    content = file_data.get("content", str(file_data))
                    meta = {k:v for k,v in file_data.items() if k != "content"}
                    if meta:
                        st.markdown(f'<div style="font-size:.72rem;color:#7986cb;margin-bottom:.4rem">{" · ".join(f"{k}: {v}" for k,v in meta.items())}</div>', unsafe_allow_html=True)
                else:
                    content = str(file_data)
                st.markdown(f'<div class="file-viewer">{html_module.escape(content)}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                    padding:3rem;color:#7986cb;gap:.75rem;text-align:center">
          <div style="font-size:3rem">📂</div>
          <div style="font-size:1rem;font-weight:600">No files yet</div>
          <div style="font-size:.82rem">
            Ask the agent to <em>"create a file at /notes/todo.txt"</em> or
            <em>"write a research report to /reports/ai.md"</em>.
          </div>
        </div>""", unsafe_allow_html=True)

    if st.session_state.virtual_files:
        if st.button("🗑 Clear virtual files"):
            st.session_state.virtual_files = {}; st.rerun()

# ════════════════ FEATURE GUIDE ════════════════
with tab_guide:
    st.markdown("<div style='font-size:1.2rem;font-weight:700;color:#e8eaf6;margin-bottom:1rem'>📖 Deep Agents Feature Guide</div>", unsafe_allow_html=True)

    features = [
        ("🤖","Basic Deep Agent — Notebook 1","#a78bfa","""
**Foundation:** `create_deep_agent()` combines an LLM with tools into a LangGraph agent loop.

**Built-in tools every deep agent gets:**
- `write_todos` — structured task planning with status tracking
- `ls`, `read_file`, `write_file`, `edit_file`, `glob`, `grep` — virtual filesystem
- `task` — delegate to a specialised subagent

**Demo:** *"What is Deep Agents?"* or *"Create a plan for a YouTube channel launch"*
        """),
        ("🧠","Context Engineering — Notebook 2","#2dd4bf","""
**Giving the agent the right information at the right time.**

1. **System Prompt** — persona, behaviour constraints baked in at startup
2. **AGENTS.md** — versioned markdown loaded into context (see sidebar)
3. **In-context seeding** — inject large context blobs as the first user message
4. **MemorySaver + thread_id** — persist conversation state across turns

**Demo:** Fill the *AGENTS.md* field in the sidebar, then ask *"Who are you and what should you follow?"*
        """),
        ("💾","Backends — Notebook 3","#fbbf24","""
**The storage layer behind the agent's file tools.**

| Backend | Lives in | Cross-thread | Disk |
|---|---|---|---|
| StateBackend | LangGraph state | ❌ | ❌ |
| FilesystemBackend | Your disk | ✅ | ✅ |
| StoreBackend | LangGraph Store | ✅ | ❌ |

**Demo:** Switch backends in the sidebar, ask the agent to *"Create a file at /notes/demo.txt with 'Hello Deep Agents'"*, then check the File Explorer tab.
        """),
        ("🤝","Subagents — Notebook 4","#4ade80","""
**Main agent delegates self-contained tasks to specialised child agents.**

**Subagents in this app:**
- `research-agent` — deep researcher with Tavily web search
- `writer-agent` — professional technical writer

**How it works:** Parent agent calls `task` tool → subagent runs in isolated context → only final answer returns to parent (keeping parent context clean).

**Demo:** *"Research LLM Gateways and write a detailed summary"* — watch `write_todos` plan, delegate to research-agent, then synthesise.
        """),
        ("📋","Planning — write_todos","#fb7185","""
**The agent uses `write_todos` to break complex tasks into a checklist.**

Statuses: `pending` → `in_progress` → `completed`

The agent updates the list as steps finish, keeping itself on track over long tasks.

**Demo:** *"Research AI agent frameworks, compare them, and write a recommendation report"* — planning tool is called first.
        """),
        ("🌐","Web Search — Tavily","#38bdf8","""
**Custom tool wrapping the Tavily Search API for live internet access.**

```python
def internet_search(query, max_results=5, topic="general"):
    return tavily_client.search(query, ...)
```

Topics supported: `general`, `news`, `finance`

**Demo:** *"What are the latest developments in AI agents this week?"*
        """),
    ]

    for icon, title, color, content in features:
        with st.expander(f"{icon} {title}"):
            st.markdown(f"<div style='border-left:3px solid {color};padding-left:1rem'>", unsafe_allow_html=True)
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
**Quick Reference**
```python
from deepagents import create_deep_agent
from deepagents.backends import StateBackend, FilesystemBackend, StoreBackend
from langgraph.checkpoint.memory import MemorySaver

agent = create_deep_agent(
    model="groq:meta-llama/llama-4-scout-17b-16e-instruct",
    tools=[internet_search],          # Custom tools (e.g. Tavily)
    system_prompt="You are…",         # Context Engineering
    subagents=[research_subagent],    # Specialised sub-agents
    backend=StateBackend(),           # or FilesystemBackend / StoreBackend
    checkpointer=MemorySaver(),       # Persistent memory across turns
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Research AI frameworks"}]},
    config={"configurable": {"thread_id": "my-session"}},
)
```
    """)
