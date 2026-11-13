# app/routers/query.py
from fastapi import APIRouter, Depends, HTTPException

from ..database import get_connection
from ..schemas import Query
from ..services.query import QueryError, execute_query

router = APIRouter(prefix="/query", tags=["query"])


@router.post("")
def run_query(q: Query, conn=Depends(get_connection)):
    try:
        return execute_query(conn, q.sql, q.params, q.database)
    except QueryError as e:
        raise HTTPException(status_code=400, detail=str(e))