from sqlalchemy import text
from app.database import engine

def verificar_schemas():
    query = text("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema IN ('vendas', 'financeiro', 'juridico', 'rh', 'atendimento', 'infra', 'seguranca')
        ORDER BY table_schema, table_name;
    """)

    with engine.connect() as conn:
        result = conn.execute(query).fetchall()

    print("\n--- SCHEMAS E TABELAS NO BANCO POSTGRESQL ('dev') ---")
    current_schema = None
    for schema, table in result:
        if schema != current_schema:
            current_schema = schema
            print(f"\n📁 SCHEMA: {current_schema.upper()}")
        print(f"   └── {current_schema}.{table}")

if __name__ == "__main__":
    verificar_schemas()
