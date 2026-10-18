# research-agent

Multi-analyst research pipeline built with [LangGraph](https://langchain-ai.github.io/langgraph/). Inspired by STORM-style workflows: generate analyst personas, run simulated expert interviews with web search, then synthesize a structured report.

## Features

- **Analyst generation** — LLM creates multiple analyst personas for a topic, with optional human-in-the-loop feedback (`interrupt`).
- **Interviews** — Each analyst asks questions; Tavily retrieves context; an “expert” answers from that context.
- **Report assembly** — Sections per analyst are merged into insights, introduction, conclusion, and a final markdown report.

## Requirements

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) (recommended)
- API keys: **OpenAI** (chat model), **Tavily** (web search)

## Setup

```bash
git clone https://github.com/Eddie4k-code/Research-Agent-.git
cd research-agent   # or your local folder name
uv sync
```

Create a `.env` file in the project root (see `langgraph.json` → `"env": ".env"`):

```env
OPENAI_API_KEY=your-openai-key
TAVILY_API_KEY=your-tavily-key

# Optional — tracing in LangSmith (disable locally if offline)
# LANGSMITH_TRACING_V2=false
# LANGSMITH_API_KEY=...
```

## Run locally (LangGraph Studio)

The CLI is installed in the project venv; use `uv run`:

```bash
uv run langgraph dev
```

Open the URL printed in the terminal (typically `http://127.0.0.1:2024`) to use LangGraph Studio.

Validate graphs without starting the server:

```bash
uv run langgraph validate
```

> **Note:** In zsh, install extras with quotes: `uv add 'langgraph-cli[inmem]'`

## Graphs

Registered in `langgraph.json`:

| Graph ID | Module | Purpose |
|----------|--------|---------|
| `create_analysts` | `research_agent.creating_analysts` | Topic → analysts → human feedback loop |
| `questions` | `research_agent.questions` | Single interview subgraph (ask → search → answer → section) |
| `research_agent` | `research_agent.agent` | End-to-end pipeline (analysts → interviews → report) |

### Example input: `create_analysts`

```json
{
  "topic": "The impact of LLMs on software engineering",
  "max_analysts": 3
}
```

At **human feedback**, approve with an empty response, `okay`, `continue`, or `perfect`, or send text to regenerate analysts.

### Example input: `questions`

```json
{
  "analyst": {
    "name": "Alex Chen",
    "role": "Industry analyst",
    "affilitation": "Tech Research Group",
    "description": "Focus on developer productivity and tooling"
  },
  "max_num_turns": 2,
  "messages": [],
  "context": [],
  "interview": "",
  "sections": []
}
```

### Example input: `research_agent`

```json
{
  "topic": "The impact of LLMs on software engineering",
  "max_analysts": 3,
  "analysts": [],
  "sections": [],
  "introduction": "",
  "content": "",
  "conclusion": "",
  "final_report": ""
}
```

Complete the human feedback step in Studio before interviews are dispatched in parallel.

## Project layout

```text
src/research_agent/
  agent.py              # Full research graph
  creating_analysts.py  # Analyst + feedback graph
  questions.py          # Interview subgraph
  utils/
    nodes.py            # Node implementations
    edges.py            # Routing (including Send for parallel interviews)
    state.py            # TypedDict state definitions
    prompts.py          # System prompts
    objects.py          # Pydantic models (Analyst, etc.)
    models.py           # ChatOpenAI client
langgraph.json          # LangGraph dev / deploy config
pyproject.toml
```

## CLI entry point

```bash
uv run research-agent
```

(Placeholder script defined in `pyproject.toml`; primary development path is `langgraph dev`.)

## License

See repository settings on GitHub for license information.
