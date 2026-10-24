# NL to SQL Agent

A multi-agent system built with LangChain + LangGraph + MCP that converts natural language questions into SQL queries and returns plain-English answers. Agents never touch the DB directly — all DB access goes through the MCP server process.

Deployed on Streamlit Community cloud at https://nl-to-sql-agent.streamlit.app


## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI (app.py)                    │
│              User types natural language question               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   LangGraph Pipeline (graph.py)                 │
│                                                                 │
│  ┌─────────────────┐                                            │
│  │ schema_injector │ ── fetches DB schema ──────────────┐       │
│  └────────┬────────┘                                    │       │
│           │                                             │       │
│           ▼                                             │       │
│  ┌─────────────────┐                                    │       │
│  │   sql_writer    │ ── GPT-4o-mini generates SQL       │       │
│  └────────┬────────┘                                    │       │
│           │                                             │       │
│           ▼                                             │       │
│  ┌─────────────────┐                                    │       │
│  │    validator    │ ── blocks DML / non-SELECT         │       │
│  └────────┬────────┘                                    │       │
│     VALID │   INVALID ──────────────────────────────────┘       │
│           │           (retry loop, max 3)                       │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │    executor     │ ── runs SQL ────────────────────────┐      │
│  └────────┬────────┘                                    │      │
│     OK    │   ERROR ───────────────────────────────────┘       │
│           ▼                                                     │
│  ┌─────────────────┐                                            │
│  │    explainer    │ ── GPT-4o-mini writes plain English answer │
│  └────────┬────────┘                                            │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼ final_answer displayed in Streamlit

┌─────────────────────────────────────────────────────────────────┐
│                    MCP Layer (stdio subprocess)                  │
│                                                                  │
│   agents/executor.py  ──┐                                        │
│   graph.py             ─┤─▶ tools/mcp_client.py                 │
│                          │        │                              │
│                          │        │ spawns subprocess            │
│                          │        ▼                              │
│                          │  mcp_server/db_server.py             │
│                          │   ├── tool: get_schema()             │
│                          │   └── tool: execute_query()          │
│                          │        │                              │
│                          │        ▼  tools/db_tools.py          │
└──────────────────────────┼──────────────────────────────────────┘
                           │
              ┌────────────┴──────────────┐
              │                           │
              ▼                           ▼
   PostgreSQL (if DATABASE_URL set)    SQLite store.db (fallback)
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
# Optionally add DATABASE_URL to connect to PostgreSQL instead of SQLite
```

### 3. Set up the database
```bash
python db/setup_db.py
```

### 4a. Run CLI
```bash
python main.py
```

### 4b. Run Streamlit UI
```bash
streamlit run app.py
```

## Project Structure

```
nl_to_sql_agent/
├── agents/
│   ├── sql_writer.py       # Generates SQL using GPT-4o-mini
│   ├── validator.py        # Blocks unsafe queries
│   ├── executor.py         # Runs SQL via MCP client
│   └── explainer.py        # Turns results into plain English
├── mcp_server/
│   └── db_server.py        # MCP server exposing get_schema & execute_query tools
├── tools/
│   ├── db_tools.py         # SQLAlchemy schema reader + query runner
│   └── mcp_client.py       # Sync wrappers that call the MCP server via stdio
├── db/
│   ├── setup_db.py         # Seeds sample e-commerce data
│   └── store.db            # SQLite DB (fallback when DATABASE_URL is not set)
├── state.py                # LangGraph AgentState definition
├── graph.py                # LangGraph graph + routing logic
├── main.py                 # CLI runner
├── app.py                  # Streamlit UI
├── requirements.txt
└── .env.example
```

## Sample Database

The sample DB is a small e-commerce store with:
- `customers` — 10 customers across US cities
- `products` — 10 products across 4 categories
- `categories` — Electronics, Clothing, Books, Home & Kitchen
- `orders` — 15 orders with statuses (delivered, shipped, pending)
- `order_items` — line items linking orders to products

## Sample Questions to Try

- How many customers do we have?
- Which product has the highest revenue?
- Show me the top 3 customers by total spending
- How many orders are pending?
- What is the average order value?
- Which category has the most products?
- List all products with less than 100 units in stock
- How many orders were placed each month?
