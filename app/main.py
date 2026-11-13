from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import databases, tables, query

app = FastAPI(title="SGBD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite
        "http://localhost:3000",   # Create React App / Next
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(databases.router)
app.include_router(tables.router)
app.include_router(query.router)