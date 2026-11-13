# app/services/query.py
from typing import Any, Optional

from mysql.connector import Error

from ..security import check_ident


class QueryError(Exception):
    """Erreur renvoyée par MySQL, à transformer en réponse HTTP par le router."""


def _serialize(value: Any) -> Any:
    # JSON ne gère pas les bytes (colonnes BLOB/BINARY) ;
    # datetime, date, Decimal sont déjà gérés par FastAPI
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    return value


def execute_query(
    conn,
    sql: str,
    params: Optional[list[Any]] = None,
    database: Optional[str] = None,
) -> dict[str, Any]:
    cur = conn.cursor(dictionary=True)
    try:
        if database:
            cur.execute(f"USE `{check_ident(database)}`")

        cur.execute(sql, params or ())

        # Requête qui renvoie des lignes : SELECT, SHOW, DESCRIBE, EXPLAIN...
        if cur.with_rows:
            rows = [
                {k: _serialize(v) for k, v in row.items()}
                for row in cur.fetchall()
            ]
            return {"columns": list(cur.column_names), "rows": rows}

        # Requête qui modifie : INSERT, UPDATE, DELETE, CREATE, DROP...
        conn.commit()
        return {
            "affected_rows": cur.rowcount,
            "last_insert_id": cur.lastrowid,
        }
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()