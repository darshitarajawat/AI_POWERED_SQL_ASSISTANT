
import sqlglot
from sqlglot import exp


def validate_sql(sql: str) -> tuple[bool, str | None]:

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    try:
        statements = sqlglot.parse(sql, read="sqlite")

    except sqlglot.errors.ParseError as exc:
        return False, f"Invalid SQL syntax: {exc}"

    # Allow only one SQL statement
    if len(statements) != 1 or statements[0] is None:
        return False, "Only one SQL statement is permitted."

    tree = statements[0]

    # Allow SELECT queries and WITH ... SELECT queries
    if not isinstance(tree, (exp.Select, exp.Union)):
        return False, "Only SELECT queries are permitted."

    # Reject database modification operations
    forbidden = (
        exp.Insert,
        exp.Update,
        exp.Delete,
        exp.Drop,
        exp.Create,
        exp.Alter,
        exp.Command,
        exp.Merge,
    )

    for operation in forbidden:
        if any(tree.find_all(operation)):
            return False, "The query contains a prohibited operation."

    # Reject SELECT INTO and locking clauses
    if tree.args.get("into") or tree.args.get("locks"):
        return False, "SELECT INTO and locking clauses are not permitted."

    return True, None
