import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH", "school.db")).resolve()


def get_schema() -> str:
    """Return table definitions and foreign-key relationships."""

    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. Check DB_PATH in .env."
        )

    with sqlite3.connect(
        f"{DB_PATH.as_uri()}?mode=ro",
        uri=True,
        timeout=10
    ) as connection:

        tables = connection.execute("""
            SELECT name, sql
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

        if not tables:
            return "No user tables found in the database."

        sections = []

        for table_name, create_sql in tables:
            columns = connection.execute(
                f"PRAGMA table_info({quote_identifier(table_name)})"
            ).fetchall()

            foreign_keys = connection.execute(
                f"PRAGMA foreign_key_list({quote_identifier(table_name)})"
            ).fetchall()

            sections.append(
                f"Table: {table_name}\n"
                f"Definition: {create_sql}\n"
                f"Columns: {columns}\n"
                f"Foreign keys: {foreign_keys}"
            )

        return "\n\n".join(sections)


def quote_identifier(name: str) -> str:
    """Safely quote a SQLite identifier."""
    return '"' + name.replace('"', '""') + '"'


def execute_readonly(sql: str, params=None):

    import sqlite3

    connection = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )

    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA query_only = ON")

        cursor = connection.cursor()

        # Execute SQL with parameters
        cursor.execute(sql, params or {})

        rows = cursor.fetchmany(500)

        return [dict(row) for row in rows]

    finally:
        connection.close()