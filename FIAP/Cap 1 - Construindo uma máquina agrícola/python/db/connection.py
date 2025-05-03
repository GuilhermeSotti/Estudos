import pyodbc
from config import SQL_SERVER, SQL_DATABASE, SQL_USERNAME, SQL_PASSWORD

def get_connection():
    """
    Retorna uma conexão pyodbc ao SQL Server.
    """
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};"
        f"UID={SQL_USERNAME};PWD={SQL_PASSWORD};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)
