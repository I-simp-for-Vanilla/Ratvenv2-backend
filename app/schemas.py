# app/schemas.py
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

IDENT_PATTERN = r"^[A-Za-z0-9_]{1,64}$"
TYPE_PATTERN = r"^[A-Za-z]+(\(\d+(,\d+)?\))?( UNSIGNED)?$"


class Column(BaseModel):
    name: str = Field(pattern=IDENT_PATTERN)
    type: str = Field(pattern=TYPE_PATTERN, examples=["INT", "VARCHAR(255)"])
    primary_key: bool = False
    auto_increment: bool = False
    nullable: bool = True
    unique: bool = False


class TableCreate(BaseModel):
    name: str = Field(pattern=IDENT_PATTERN)
    comment: str
    engine: str
    columns: list[Column] = Field(min_length=1)

    @field_validator("columns")
    @classmethod
    def no_duplicate_names(cls, cols: list[Column]):
        names = [c.name.lower() for c in cols]
        if len(names) != len(set(names)):
            raise ValueError("Noms de colonnes en double")
        return cols
    

class TableRename(BaseModel):
    new_table_name: str = Field(pattern=IDENT_PATTERN)


class Query(BaseModel):
    sql: str = Field(min_length=1)
    params: Optional[list[Any]] = None
    database: Optional[str] = Field(default=None, pattern=IDENT_PATTERN)


# ---------- Réponses (optionnel, mais documente l'API dans /docs) ----------
class QueryRows(BaseModel):
    rows: list[dict[str, Any]]


class QueryResult(BaseModel):
    affected_rows: int
    last_insert_id: Optional[int] = None