from typing import Any, Optional

from mysql.connector import Error, connect

from ..security import check_ident

class QueryError(Exception):
    """Erreur renvoyée par MySQL, à transformer en réponse HTTP par le router."""

def _serialize(value: Any) -> Any:
    # JSON ne gère pas les bytes (colonnes BLOB/BINARY) ;
    # datetime, date, Decimal sont déjà gérés par FastAPI
    if isinstance(value, (bytes, bytearray)):
        return value.hex()
    return value


def get_tables(conn, db_name):
    check_ident(db_name)
    cur = conn.cursor(dictionary=True)

    sql = "SHOW TABLES"

    try:
        cur.execute(f"USE `{db_name}`")
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


def compute_width(rows, columns):
    for key in columns:
        max_width = 140
        if "varchar" in key["type"] or key["type"] == "text":
            max_width = 200
            for row in rows:
                current_width = len(row[key["name"]]) * 4
                if max_width < current_width and current_width < 500:
                    max_width = current_width
                elif current_width > 500:
                    max_width = 500

        key["width"] = max_width
    


def select_table(conn, db_name, table_name, columns, filter, order_by, limit):
    check_ident(db_name)
    cur = conn.cursor(dictionary=True)

    sql = f"SELECT {columns if columns !="" else "*"} FROM {table_name}"

    if filter != "" :
        sql += f" WHERE {filter}"

    if order_by != "" :
        sql += f" ORDER BY {order_by}"

    if limit != "" :
        sql += f" LIMIT {limit}"

    print(sql)

    try:
        cur.execute(f"USE `{db_name}`")
        cur.execute(sql)

        # Requête qui renvoie des lignes : SELECT, SHOW, DESCRIBE, EXPLAIN...
        rows = [
            {k: _serialize(v) for k, v in row.items()}
            for row in cur.fetchall()
        ]

        table_infos = get_infos_table(conn, db_name, table_name)

        compute_width(rows, table_infos["columns"])

        return {"columns": table_infos["columns"], "rows": rows}
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()

def get_infos_table(conn, db_name, table):
    sql = f"SELECT t.table_schema AS database_name, t.table_name AS table_name, t.engine AS engine, t.table_rows AS row_count, (SELECT COUNT(*) FROM information_schema.columns c WHERE c.table_schema = t.table_schema AND c.table_name = t.table_name) AS column_count, ROUND((t.data_length + t.index_length) / 1024 / 1024, 2) AS size_mb, t.update_time AS last_update FROM information_schema.tables t WHERE t.table_schema = '{db_name}' AND t.table_type = 'BASE TABLE' AND t.table_name   = '{table}';"
    sql2 = f"SELECT column_name As name, column_type As type FROM information_schema.columns WHERE table_schema = '{db_name}' AND table_name = '{table}' ORDER BY ordinal_position;"

    cur = conn.cursor(dictionary=True)

    try:

        cur.execute(sql)

        # Requête qui renvoie des lignes : SELECT, SHOW, DESCRIBE, EXPLAIN...
        databases = [
            {k: _serialize(v) for k, v in row.items()}
            for row in cur.fetchall()
        ]

        res = databases[0]

        cur.execute(sql2)

        columns = [
            {k: _serialize(v) for k, v in row.items()}
            for row in cur.fetchall()
        ]

        for column in columns:
            column["label"] = column["name"]
            column["key"] = column["name"]
            column["width"] = 140

        res["columns"] = columns

        return res
        # return {"columns": list(cur.column_names), "rows": rows}
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()


def create_table(conn, db_name, table):
    check_ident(db_name)
    check_ident(table.name)

    cur = conn.cursor(dictionary=True)

    try:
        sql = "CREATE TABLE IF NOT EXISTS " + table.name + "("
        for col in table.columns:
            sql += f" {col.name} {col.type}{" PRIMARY KEY" if col.primary_key else "" }{" AUTO_INCREMENT" if col.auto_increment else "" }{" UNIQUE" if not col.unique else "" }{" NOT NULL" if not col.nullable else "" },"
        sql = sql[:-1] + ")"

        if table.engine and table.engine != "" : sql += f" ENGINE = {table.engine}"

        sql += f" COMMENT = '{table.comment}'"

        print(sql)

        cur.execute(f"USE `{db_name}`")
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


def rename_table(conn, db_name, table_name, body):
    check_ident(db_name)
    check_ident(table_name)

    cur = conn.cursor(dictionary=True)

    try:

        sql = "RENAME TABLE " + table_name + " TO " + body.new_table_name

        cur.execute(f"USE `{db_name}`")
        cur.execute(sql)

        # Requête qui modifie : INSERT, UPDATE, DELETE, CREATE, DROP...
        conn.commit()
        return {
            "new_table_name": body.new_table_name,
        }
    except Error as e:
        conn.rollback()
        raise QueryError(str(e)) from e
    finally:
        cur.close()


def drop_table(conn, db_name, table_name):
    check_ident(db_name)
    check_ident(table_name)

    cur = conn.cursor(dictionary=True)

    try:

        cur.execute(f"USE `{db_name}`")
        cur.execute(f"DROP TABLE {table_name}")

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
    res = get_infos_table(cnx, "BoomDB", "Actions")
    cnx.close()
    # get_databases_v2(conn)