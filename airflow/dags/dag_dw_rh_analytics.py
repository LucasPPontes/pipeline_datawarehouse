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

def etl_rh_analytics():
    ensure_dw_schema()
    engine = get_erp_engine()

    query_rh_metricas = """
    CREATE TABLE IF NOT EXISTS dw.fato_rh_metricas_departamento (
        departamento_id INT PRIMARY KEY,
        nome_departamento VARCHAR(150),
        sigla VARCHAR(20),
        headcount INT,
        custo_mensal_folha NUMERIC(12, 2),
        salario_medio NUMERIC(10, 2),
        orcamento_anual NUMERIC(12, 2),
        percentual_orcamento_usado NUMERIC(5, 2),
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.fato_rh_metricas_departamento;

    INSERT INTO dw.fato_rh_metricas_departamento (
        departamento_id, nome_departamento, sigla, headcount,
        custo_mensal_folha, salario_medio, orcamento_anual, percentual_orcamento_usado
    )
    SELECT
        d.id AS departamento_id,
        d.nome AS nome_departamento,
        d.sigla,
        COUNT(f.id) AS headcount,
        COALESCE(SUM(f.salario), 0) AS custo_mensal_folha,
        ROUND(COALESCE(AVG(f.salario), 0), 2) AS salario_medio,
        d.orcamento_anual,
        ROUND(
            (COALESCE(SUM(f.salario), 0) * 12 / NULLIF(d.orcamento_anual, 0)) * 100, 2
        ) AS percentual_orcamento_usado
    FROM rh.departamentos d
    LEFT JOIN rh.funcionarios f ON d.id = f.departamento_id AND f.status = 'ativo'
    GROUP BY d.id, d.nome, d.sigla, d.orcamento_anual
    ORDER BY custo_mensal_folha DESC;
    """

    with engine.connect() as conn:
        conn.execute(text(query_rh_metricas))
        conn.commit()
    print("✅ ETL de RH concluído com sucesso no Data Warehouse (dw)!")

if HAS_AIRFLOW and DAG is not None:
    with DAG(
        'dag_dw_rh_analytics',
        default_args=default_args,
        description='Pipeline ETL de análise do setor de RH (dw.fato_rh_metricas_departamento)',
        schedule='@daily',
        catchup=False,
        tags=['analytics', 'rh', 'dw'],
    ) as dag:


        task_rh_etl = PythonOperator(
            task_id='processar_analytics_rh',
            python_callable=etl_rh_analytics,
        )
