from datetime import datetime, timedelta
from sqlalchemy import text
from dw_helpers import get_erp_engine, ensure_dw_schema

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    HAS_AIRFLOW = True
except ImportError:
    HAS_AIRFLOW = False
    DAG = None
    PythonOperator = None

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def etl_vendas_analytics():
    ensure_dw_schema()
    engine = get_erp_engine()

    query_fato_vendas = """
    CREATE TABLE IF NOT EXISTS dw.fato_vendas_mensal (
        ano_mes VARCHAR(7) PRIMARY KEY,
        faturamento_total NUMERIC(12, 2),
        total_pedidos INT,
        pedidos_concluidos INT,
        pedidos_pendentes INT,
        pedidos_cancelados INT,
        ticket_medio NUMERIC(10, 2),
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.fato_vendas_mensal;

    INSERT INTO dw.fato_vendas_mensal (
        ano_mes, faturamento_total, total_pedidos,
        pedidos_concluidos, pedidos_pendentes, pedidos_cancelados, ticket_medio
    )
    SELECT
        TO_CHAR(data_venda::DATE, 'YYYY-MM') AS ano_mes,
        COALESCE(SUM(valor_total), 0) AS faturamento_total,
        COUNT(id) AS total_pedidos,
        COUNT(CASE WHEN status = 'concluido' THEN 1 END) AS pedidos_concluidos,
        COUNT(CASE WHEN status = 'pendente' THEN 1 END) AS pedidos_pendentes,
        COUNT(CASE WHEN status = 'cancelado' THEN 1 END) AS pedidos_cancelados,
        ROUND(COALESCE(AVG(valor_total), 0), 2) AS ticket_medio
    FROM vendas.pedidos
    GROUP BY TO_CHAR(data_venda::DATE, 'YYYY-MM')
    ORDER BY ano_mes;

    """

    query_dim_produtos = """
    CREATE TABLE IF NOT EXISTS dw.dim_desempenho_produtos (
        produto_id INT PRIMARY KEY,
        nome_produto VARCHAR(150),
        categoria VARCHAR(100),
        quantidade_total_vendida INT,
        faturamento_gerado NUMERIC(12, 2),
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.dim_desempenho_produtos;

    INSERT INTO dw.dim_desempenho_produtos (
        produto_id, nome_produto, categoria, quantidade_total_vendida, faturamento_gerado
    )
    SELECT
        p.id AS produto_id,
        p.nome AS nome_produto,
        p.categoria,
        COALESCE(SUM(i.quantidade), 0) AS quantidade_total_vendida,
        COALESCE(SUM(i.subtotal), 0) AS faturamento_gerado
    FROM vendas.produtos p
    LEFT JOIN vendas.itens_pedido i ON p.id = i.produto_id
    GROUP BY p.id, p.nome, p.categoria
    ORDER BY faturamento_gerado DESC;
    """

    with engine.connect() as conn:
        conn.execute(text(query_fato_vendas))
        conn.execute(text(query_dim_produtos))
        conn.commit()
    print("✅ ETL de Vendas concluído com sucesso no Data Warehouse (dw)!")

if HAS_AIRFLOW and DAG is not None:
    with DAG(
        'dag_dw_vendas_analytics',
        default_args=default_args,
        description='Pipeline ETL de análise do setor de Vendas (Consolidação em dw.fato_vendas_mensal)',
        schedule='@daily',
        catchup=False,
        tags=['analytics', 'vendas', 'dw'],
    ) as dag:


        task_vendas_etl = PythonOperator(
            task_id='processar_analytics_vendas',
            python_callable=etl_vendas_analytics,
        )
