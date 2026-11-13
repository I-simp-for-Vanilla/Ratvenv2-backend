from mysql.connector import pooling
from .config import settings

pool = pooling.MySQLConnectionPool(
    pool_name="sgbd_pool",
    pool_size=settings.pool_size,
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
)

def get_connection():
    conn = pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()