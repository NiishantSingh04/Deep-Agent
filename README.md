# Deep Agent Studio & Demo Suite

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58.0-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Supported-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An advanced pair-programming assistant, researcher, and document writer suite built on top of the **DeepAgents** library and **LangGraph**. This repository contains a collection of interactive notebooks demonstrating the core architectural pillars of Deep Agents and a fully featured, premium Streamlit dashboard to test and visualize the agent's capabilities in real time.

---

## 🌟 Key Pillars & Features

Deep Agents are designed to handle complex, long-horizon, multi-step tasks by utilizing specialized abstractions. This project demonstrates all of them:

```
                    ┌─────────────────────────────┐
                    │        Deep Agent           │
                    │  (create_deep_agent, on     │
                    │   top of LangGraph)         │
                    └──────────┬──────────────────┘
                               │
        ┌──────────────┬───────┴───────┬──────────────────┐
        ▼              ▼               ▼                  ▼
  ┌───────────┐  ┌───────────┐  ┌─────────────┐   ┌─────────────┐
  │ Planning  │  │ File      │  │ Subagents   │   │ Custom      │
  │ tool      │  │ system    │  │ (task tool) │   │ e.g. web    │
  │ write_    │  │ ls, read_ │  │ isolated    │   │ search      │
  │ todos     │  │ file,     │  │ context per │   │ (Tavily)    │
  │           │  │ edit_file │  │ subagent    │   │             │
  │           │  │           │  │             │   │             │
  └───────────┘  └───────────┘  └─────────────┘   └─────────────┘
```

1. **Structured Planning (`write_todos`)**
   - The agent breaks complex tasks down into a structured todo list (`pending` ➔ `in_progress` ➔ `completed`) before executing, adjusting the plan dynamically as it progresses.
2. **Context Offloading (Virtual File System)**
   - To prevent context window pollution, the agent writes raw reports, notes, or web search results to a virtual filesystem (using `write_file`, `read_file`, `edit_file`, etc.) and only passes summarized responses back to the user.
3. **Pluggable Backends**
   - **StateBackend**: Virtual files are held in RAM inside the LangGraph state.
   - **FilesystemBackend**: Virtual files are mapped directly to a root directory on the local disk.
   - **StoreBackend**: Files are stored in a shared cross-thread memory store (perfect for long-term user memories).
4. **Specialized Subagents**
   - Spawns specialized child agents (`research-agent`, `writer-agent`) for specific subtasks. Each subagent gets a clean, isolated context window, with only the final output returned to the supervisor.
5. **Interactive Web UI Studio**
   - A beautiful Streamlit-based web dashboard offering chat capability, a live configuration sidebar, and an interactive virtual file explorer.

---

## 📂 Repository Structure

```
├── deepagentsdemo/
│   ├── 1-BasicDeepAgent.ipynb      # Core agent loop, Tavily search, and planning
│   ├── 2-ContextEngineering.ipynb   # Prompts, AGENTS.md, and state memory seeding
│   ├── 3-Backends.ipynb             # Pluggable backend storage (State, File, Store)
│   ├── 4-subagents.ipynb            # Subagent configuration and synchronous delegation
│   ├── projects/
│   │   └── AGENTS.md                # Durable system context loaded by the agent
│   └── notes/
│       └── todo.txt                 # Demo file output
├── streamlit_app.py                 # Premium Web UI Dashboard
├── main.py                          # Basic Entry point
├── pyproject.toml                   # Project metadata and dependencies
└── requirements.txt                 # dependencies list
```

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.12+** installed. We recommend using `uv` for fast package management, but `pip` works perfectly as well.

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/deep-agent-studio.git
cd deep-agent-studio
```

### 2. Set Up Virtual Environment & Dependencies
**Using `uv`:**
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Using standard `pip`:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root of the project and populate it with your API keys:
```env
GROQ_API_KEY="your-groq-api-key"
OPENAI_API_KEY="your-openai-api-key"
TAVILY_API_KEY="your-tavily-api-key"
```

---

## 🚀 Usage

### Option A: Launching the Streamlit Web Studio (Recommended)

Run the following command to start the unified interactive interface:
```bash
streamlit run streamlit_app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to access the dashboard.

#### Web Studio Features:
* **Interactive Chat**: Chat with a deep agent using color-coded messages, tool-running indicators, and predefined quick-start prompt buttons.
* **Live Configuration Sidebar**: Switch LLM models (llama-4, Qwen, GPT), select storage backends (State, File, Store), and toggle features (Tavily search, Subagents, or Memory) on the fly.
* **Virtual File Explorer**: Open and view code, reports, or lists that the agent writes during conversation.

---

### Option B: Running the Jupyter Notebooks

Launch Jupyter to explore the notebook guides page-by-page:
```bash
jupyter notebook
```
Explore the notebooks inside the `deepagentsdemo` directory in chronological order to learn how the agent uses planning, writes files, persists state, and delegates tasks to subagents.

---

## ⚙️ Pluggable Backends Comparison

| Backend | Storage Location | Cross-Thread Persistence | Local Disk Access | Use Case |
| :--- | :--- | :---: | :---: | :--- |
| **`StateBackend`** | LangGraph State (RAM) | ❌ | ❌ | Short-lived scratch space |
| **`FilesystemBackend`** | Local Directory | ✅ | ✅ | Code edits and workspace file generation |
| **`StoreBackend`** | Shared Store DB | ✅ | ❌ | Multi-session user memory |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have suggestions, features, or bug fixes.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
