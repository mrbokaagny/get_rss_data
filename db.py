import os
from sqlalchemy import create_engine

def get_db_conn():
    host = os.getenv("DB_HOST", "db_postgres")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "flux_rss")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASS", "postgres")
    
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    
    engine = create_engine(url)
    return engine
