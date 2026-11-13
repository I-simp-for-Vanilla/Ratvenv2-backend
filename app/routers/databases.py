from fastapi import APIRouter, Depends, HTTPException

from ..database import get_connection
from ..services import databases

router = APIRouter(prefix="/databases", tags=["database"])

@router.get("")
def get_databases(conn=Depends(get_connection)):
    result = databases.get_databases(conn)
    return {"result": result}

@router.post("/{db_name}")
def create_database(db_name : str, conn=Depends(get_connection)):
    result = databases.create_database(conn, db_name)
    return {"result": result}

@router.delete("/{db_name}")
def drop_database(db_name : str, conn=Depends(get_connection)):
    result = databases.drop_database(conn, db_name)
    return {"result": result}