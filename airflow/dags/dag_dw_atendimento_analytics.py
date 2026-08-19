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

def etl_atendimento_analytics():
    ensure_dw_schema()
    engine = get_erp_engine()

    query_atendimento_kpis = """
    CREATE TABLE IF NOT EXISTS dw.fato_atendimento_kpis (
        id SERIAL PRIMARY KEY,
        total_tickets INT,
        tickets_resolvidos INT,
        tickets_em_andamento INT,
        tickets_abertos INT,
        taxa_resolucao NUMERIC(5, 2),
        media_csat NUMERIC(3, 2),
        tickets_prioridade_critica INT,
        tickets_prioridade_alta INT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.fato_atendimento_kpis;

    INSERT INTO dw.fato_atendimento_kpis (
        total_tickets, tickets_resolvidos, tickets_em_andamento, tickets_abertos,
        taxa_resolucao, media_csat, tickets_prioridade_critica, tickets_prioridade_alta
    )
    SELECT
        COUNT(t.id) AS total_tickets,
        COUNT(CASE WHEN t.status = 'resolvido' THEN 1 END) AS tickets_resolvidos,
        COUNT(CASE WHEN t.status = 'em_andamento' THEN 1 END) AS tickets_em_andamento,
        COUNT(CASE WHEN t.status = 'aberto' THEN 1 END) AS tickets_abertos,
        ROUND(
            (COUNT(CASE WHEN t.status = 'resolvido' THEN 1 END)::NUMERIC / NULLIF(COUNT(t.id), 0)::NUMERIC) * 100, 2
        ) AS taxa_resolucao,
        ROUND((SELECT COALESCE(AVG(nota_satisfacao), 0) FROM atendimento.pesquisas_satisfacao), 2) AS media_csat,
        COUNT(CASE WHEN t.prioridade = 'critica' THEN 1 END) AS tickets_prioridade_critica,
        COUNT(CASE WHEN t.prioridade = 'alta' THEN 1 END) AS tickets_prioridade_alta
    FROM atendimento.tickets t;
    """

    with engine.connect() as conn:
        conn.execute(text(query_atendimento_kpis))
        conn.commit()
    print("✅ ETL de Atendimento ao Cliente concluído com sucesso no Data Warehouse (dw)!")

if HAS_AIRFLOW and DAG is not None:
    with DAG(
        'dag_dw_atendimento_analytics',
        default_args=default_args,
        description='Pipeline ETL de análise de Suporte e Atendimento (dw.fato_atendimento_kpis)',
        schedule='@daily',
        catchup=False,
        tags=['analytics', 'atendimento', 'dw'],
    ) as dag:


        task_atendimento_etl = PythonOperator(
            task_id='processar_analytics_atendimento',
            python_callable=etl_atendimento_analytics,
        )
