import os
from sqlalchemy import create_engine, text

def get_erp_connection_url():
    # Tenta conectar ao host do Docker (172.17.0.1 ou host.docker.internal) ou localhost
    host = os.getenv("ERP_POSTGRES_HOST", "172.17.0.1")
    port = os.getenv("ERP_POSTGRES_PORT", "5432")
    db = os.getenv("ERP_POSTGRES_DB", "dev")
    user = os.getenv("ERP_POSTGRES_USER", "dev")
    password = os.getenv("ERP_POSTGRES_PASSWORD", "dev")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"

def get_erp_engine():
    # Se 172.17.0.1 falhar, tenta host.docker.internal
    url = get_erp_connection_url()
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        return engine
    except Exception:
        fallback_url = url.replace("172.17.0.1", "host.docker.internal")
        try:
            engine = create_engine(fallback_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            return engine
        except Exception:
            localhost_url = url.replace("172.17.0.1", "localhost")
            return create_engine(localhost_url)

def ensure_dw_schema():
    engine = get_erp_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
        conn.commit()
