import os
from sqlalchemy import create_engine, text, inspect

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "store.db")
engine = create_engine(f"sqlite:///{os.path.abspath(DB_PATH)}")


def get_schema() -> str:
    inspector = inspect(engine)
    tables = []
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        col_defs = ", ".join(
            f"{c['name']} {str(c['type'])}" for c in columns
        )
        fks = inspector.get_foreign_keys(table_name)
        fk_info = ""
        if fks:
            fk_parts = [
                f"{fk['constrained_columns']} -> {fk['referred_table']}({fk['referred_columns']})"
                for fk in fks
            ]
            fk_info = f"\n  Foreign keys: {', '.join(fk_parts)}"
        tables.append(f"Table: {table_name}\n  Columns: {col_defs}{fk_info}")
    return "\n\n".join(tables)


def execute_query(sql: str) -> tuple[str, str]:
    sql_stripped = sql.strip()

    blocked = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "CREATE", "REPLACE"]
    sql_upper = sql_stripped.upper()
    for keyword in blocked:
        if keyword in sql_upper.split():
            return "", f"Blocked keyword detected: {keyword}"

    if not sql_upper.startswith("SELECT"):
        return "", "Only SELECT queries are permitted."

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_stripped))
            cols = list(result.keys())
            rows = result.fetchmany(100)
            if not rows:
                return "Query returned no results.", ""
            formatted_rows = [dict(zip(cols, row)) for row in rows]
            header = " | ".join(cols)
            separator = "-" * len(header)
            lines = [header, separator]
            for row in formatted_rows:
                lines.append(" | ".join(str(v) for v in row.values()))
            return "\n".join(lines), ""
    except Exception as e:
        return "", str(e)
