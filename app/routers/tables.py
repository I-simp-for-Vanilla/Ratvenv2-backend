from fastapi import APIRouter, Depends
from ..database import get_connection
from ..schemas import TableCreate, TableRename # Importe le modèle de body de la route post
from ..services import tables

router = APIRouter(prefix="/databases/{db_name}/tables", tags=["tables"])

@router.get("")
def get_tables(db_name: str, conn=Depends(get_connection)):
    result = tables.get_tables(conn, db_name)
    return {"result": result}


@router.get("/{table_name}")
def select_table(db_name: str, table_name: str, columns = "", filter = "", order_by = "", limit = "", conn=Depends(get_connection)):
    result = tables.select_table(conn, db_name, table_name, columns, filter, order_by, limit)
    return {"result": result}


@router.get("/{table_name}/infos")
def get_table_infos(db_name: str, table_name: str, conn=Depends(get_connection)):
    result = tables.get_infos_table(conn, db_name, table_name)
    return {"result": result}


@router.put("/{table_name}", status_code=201)
def rename_table(db_name: str, table_name: str, table: TableRename, conn=Depends(get_connection)):
    result = tables.rename_table(conn, db_name, table_name, table)
    return result


@router.post("", status_code=201)
def create_table(db_name: str, table: TableCreate, conn=Depends(get_connection)):
    tables.create_table(conn, db_name, table)
    return {"created": f"{db_name}.{table.name}"}


@router.delete("/{table_name}")
def drop_table(db_name: str, table_name: str, conn=Depends(get_connection)):
    tables.drop_table(conn, db_name, table_name)
    return {"droped": f"{db_name}.{table_name}"}