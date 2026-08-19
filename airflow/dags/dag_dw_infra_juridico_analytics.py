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

def etl_infra_juridico_analytics():
    ensure_dw_schema()
    engine = get_erp_engine()

    query_infra_juridico = """
    CREATE TABLE IF NOT EXISTS dw.fato_infra_juridico_custos (
        id SERIAL PRIMARY KEY,
        custo_total_manutencoes_ti NUMERIC(12, 2),
        custo_anual_licencas_software NUMERIC(12, 2),
        total_servidores_ativos INT,
        total_equipamentos_em_uso INT,
        valor_total_contratos_vigentes NUMERIC(14, 2),
        total_passivo_processos_judiciais NUMERIC(14, 2),
        processos_em_andamento INT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.fato_infra_juridico_custos;

    INSERT INTO dw.fato_infra_juridico_custos (
        custo_total_manutencoes_ti,
        custo_anual_licencas_software,
        total_servidores_ativos,
        total_equipamentos_em_uso,
        valor_total_contratos_vigentes,
        total_passivo_processos_judiciais,
        processos_em_andamento
    )
    SELECT
        (SELECT COALESCE(SUM(custo), 0) FROM infra.manutencoes) AS custo_total_manutencoes_ti,
        (SELECT COALESCE(SUM(valor_anual), 0) FROM infra.licencas_software) AS custo_anual_licencas_software,
        (SELECT COUNT(*) FROM infra.servidores WHERE status_operacional = 'online') AS total_servidores_ativos,
        (SELECT COUNT(*) FROM infra.equipamentos WHERE status = 'em_uso') AS total_equipamentos_em_uso,
        (SELECT COALESCE(SUM(valor_contrato), 0) FROM juridico.contratos WHERE status = 'vigente') AS valor_total_contratos_vigentes,
        (SELECT COALESCE(SUM(valor_causa), 0) FROM juridico.processos WHERE status_processo = 'em_andamento') AS total_passivo_processos_judiciais,
        (SELECT COUNT(*) FROM juridico.processos WHERE status_processo = 'em_andamento') AS processos_em_andamento;
    """

    with engine.connect() as conn:
        conn.execute(text(query_infra_juridico))
        conn.commit()
    print("✅ ETL de Infraestrutura e Jurídico concluído com sucesso no Data Warehouse (dw)!")

if HAS_AIRFLOW and DAG is not None:
    with DAG(
        'dag_dw_infra_juridico_analytics',
        default_args=default_args,
        description='Pipeline ETL de análise de Custos de Infraestrutura e Riscos Jurídicos (dw.fato_infra_juridico_custos)',
        schedule='@daily',
        catchup=False,
        tags=['analytics', 'infra', 'juridico', 'dw'],
    ) as dag:


        task_infra_juridico_etl = PythonOperator(
            task_id='processar_analytics_infra_juridico',
            python_callable=etl_infra_juridico_analytics,
        )
