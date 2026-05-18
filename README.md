# NL to SQL Agent

A multi-agent system built with LangChain + LangGraph that converts natural language questions into SQL queries and returns plain-English answers.

## Architecture

```
User Question
     │
     ▼
Schema Injector   ← loads DB schema into state
     │
     ▼
SQL Writer        ← generates SELECT query (Claude Haiku)
     │
     ▼
Validator         ← checks safety & syntax (no DML allowed)
     │
   valid? ──No──► SQL Writer (loop)
     │
    Yes
     ▼
Executor          ← runs query against SQLite DB
     │
  error? ──Yes──► SQL Writer (retry with error context, max 3x)
     │
    No
     ▼
Explainer         ← converts raw results to natural language
     │
     ▼
  Answer
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your API key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
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
│   ├── sql_writer.py     # Generates SQL using Claude
│   ├── validator.py      # Blocks unsafe queries
│   ├── executor.py       # Runs SQL against DB
│   └── explainer.py      # Turns results into plain English
├── tools/
│   └── db_tools.py       # Schema reader + query runner
├── db/
│   ├── setup_db.py       # Seeds sample e-commerce data
│   └── store.db          # SQLite DB (auto-created)
├── state.py              # LangGraph AgentState definition
├── graph.py              # LangGraph graph + routing logic
├── main.py               # CLI runner
├── app.py                # Streamlit UI
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
