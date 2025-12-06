from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus, urlparse

import os


def get_engine():
    load_dotenv()
    db_url = urlparse(
        "mssql+pyodbc://sa:$MSSQL_SA_PASSWORD@localhost:1433/AgroFreight?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    db_url = db_url._replace(
        netloc=db_url.netloc.replace(
            "$MSSQL_SA_PASSWORD", quote_plus(os.getenv("MSSQL_SA_PASSWORD", ""))
        )
    )

    return create_engine(db_url.geturl())
