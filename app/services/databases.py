from mysql.connector import Error, connect
from typing import Any

class QueryError(Exception):
    """Erreur renvoyée par MySQL, à transformer en réponse HTTP par le router."""

def _serialize(value: Any) -> Any:
    # JSON ne gère pas les bytes (colonnes BLOB/BINARY) ;
    # datetime, date, Decimal sont déjà gérés par FastAPI
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    return value

""" Get all databases """
def get_databases_old(conn):
    # construction du CREATE TABLE ...
    sql = "SELECT s.schema_name AS database_name, s.default_character_set_name AS charset, ROUND(COALESCE(SUM(t.data_length + t.index_length) / 1024 / 1024, 0), 2) AS size_mb FROM information_schema.schemata s LEFT JOIN information_schema.tables t ON t.table_schema = s.schema_name GROUP BY s.schema_name, s.default_character_set_name ORDER BY size_mb DESC"
    cur = conn.cursor(dictionary=True)

    try:

        cur.execute(sql)

        # Requête qui renvoie des lignes : SELECT, SHOW, DESCRIBE, EXPLAIN...
        rows = [
            {k: _serialize(v) for k, v in row.items()}
            for row in cur.fetchall()
        ]
        return {"columns": list(cur.column_names), "rows": rows}
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()

def get_databases(conn):
    
    sql1 = "SELECT s.schema_name AS database_name, s.default_character_set_name AS charset, ROUND(COALESCE(SUM(t.data_length + t.index_length) / 1024 / 1024, 0), 2) AS size_mb FROM information_schema.schemata s LEFT JOIN information_schema.tables t ON t.table_schema = s.schema_name GROUP BY s.schema_name, s.default_character_set_name ORDER BY size_mb DESC"

    cur = conn.cursor(dictionary=True)

    res = []

    try:

        cur.execute(sql1)

        # Requête qui renvoie des lignes : SELECT, SHOW, DESCRIBE, EXPLAIN...
        databases = [
            {k: _serialize(v) for k, v in row.items()}
            for row in cur.fetchall()
        ]
        for db in databases:
            res_row = {"name": db["database_name"], "engine": "MySQL 8.0", "host": "localhost", "charset": db["charset"], "size": f"{db["size_mb"]} MB", "created": "00/00/0000", "tables": []}

            cur.execute(f"SELECT t.table_schema AS database_name, t.table_name AS table_name, t.engine AS engine, t.table_rows AS row_count, (SELECT COUNT(*) FROM information_schema.columns c WHERE c.table_schema = t.table_schema AND c.table_name = t.table_name) AS column_count, ROUND((t.data_length + t.index_length) / 1024 / 1024, 2) AS size_mb, t.update_time AS last_update FROM information_schema.tables t WHERE t.table_schema = '{db["database_name"]}' AND t.table_type = 'BASE TABLE' ORDER BY size_mb DESC;")
            # cur.execute(f"USE `{db["database_name"]}`")
            # cur.execute(f"SHOW TABLES")

            tables = [
                {k: _serialize(v) for k, v in row.items()}
                for row in cur.fetchall()
            ]

            for table in tables:
                res_row["tables"].append({"name": table["table_name"], "rows": table["row_count"], "columns": table["column_count"], "size": f"{table["size_mb"]} MB", "updated": table["last_update"]})
                print(res_row)
            
            res.append(res_row)
        return res
        # return {"columns": list(cur.column_names), "rows": rows}
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()



""" Create a new database """
def create_database(conn, db_name):
    cur = conn.cursor(dictionary=True)
    try:
        sql = "CREATE DATABASE IF NOT EXISTS " + db_name

        cur.execute(sql)

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

if __name__ == "__main__":
    pass

def drop_database(conn, db_name):
    cur = conn.cursor(dictionary=True)
    try:
        sql = "DROP DATABASE IF EXISTS " + db_name

        cur.execute(sql)

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

if __name__ == "__main__":
    cnx = connect(user='root', password='root', host='localhost', port="8889")
    res = get_databases(cnx)
    cnx.close()
    # get_databases_v2(conn)