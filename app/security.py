import re
from fastapi import HTTPException

IDENT = re.compile(r"^[A-Za-z0-9_]{1,64}$")
COL_TYPE = re.compile(r"^[A-Za-z]+(\(\d+(,\d+)?\))?( UNSIGNED)?$", re.IGNORECASE)


def check_ident(name: str) -> str:
    """Les identifiants (bases, tables, colonnes) ne peuvent pas être paramétrés : on les valide."""
    if not IDENT.match(name):
        raise HTTPException(400, f"Identifiant invalide : {name!r}")
    return name