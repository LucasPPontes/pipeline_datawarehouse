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

def etl_financeiro_analytics():
    ensure_dw_schema()
    engine = get_erp_engine()

    query_fluxo_caixa = """
    CREATE TABLE IF NOT EXISTS dw.fato_fluxo_caixa_mensal (
        ano_mes VARCHAR(7) PRIMARY KEY,
        total_receitas NUMERIC(12, 2),
        total_despesas NUMERIC(12, 2),
        resultado_liquido NUMERIC(12, 2),
        lancamentos_pagos INT,
        lancamentos_pendentes INT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.fato_fluxo_caixa_mensal;

    INSERT INTO dw.fato_fluxo_caixa_mensal (
        ano_mes, total_receitas, total_despesas, resultado_liquido,
        lancamentos_pagos, lancamentos_pendentes
    )
    SELECT
        TO_CHAR(data_vencimento, 'YYYY-MM') AS ano_mes,
        COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0) AS total_receitas,
        COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0) AS total_despesas,
        COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE -valor END), 0) AS resultado_liquido,
        COUNT(CASE WHEN status_pagamento = 'pago' THEN 1 END) AS lancamentos_pagos,
        COUNT(CASE WHEN status_pagamento = 'pendente' THEN 1 END) AS lancamentos_pendentes
    FROM financeiro.lancamentos
    GROUP BY TO_CHAR(data_vencimento, 'YYYY-MM')
    ORDER BY ano_mes;
    """

    query_kpi_saude = """
    CREATE TABLE IF NOT EXISTS dw.kpi_saude_financeira (
        id SERIAL PRIMARY KEY,
        saldo_total_bancos NUMERIC(14, 2),
        total_faturas_pagas NUMERIC(14, 2),
        total_faturas_pendentes NUMERIC(14, 2),
        percentual_adimplencia NUMERIC(5, 2),
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    TRUNCATE TABLE dw.kpi_saude_financeira;

    INSERT INTO dw.kpi_saude_financeira (
        saldo_total_bancos, total_faturas_pagas, total_faturas_pendentes, percentual_adimplencia
    )
    SELECT
        (SELECT COALESCE(SUM(saldo_atual), 0) FROM financeiro.contas_bancarias) AS saldo_total_bancos,
        COALESCE(SUM(CASE WHEN status = 'paga' THEN valor_total ELSE 0 END), 0) AS total_faturas_pagas,
        COALESCE(SUM(CASE WHEN status = 'pendente' THEN valor_total ELSE 0 END), 0) AS total_faturas_pendentes,
        ROUND(
            (COUNT(CASE WHEN status = 'paga' THEN 1 END)::NUMERIC / NULLIF(COUNT(*), 0)::NUMERIC) * 100, 2
        ) AS percentual_adimplencia
    FROM financeiro.faturas;
    """

    with engine.connect() as conn:
        conn.execute(text(query_fluxo_caixa))
        conn.execute(text(query_kpi_saude))
        conn.commit()
    print("✅ ETL Financeiro concluído com sucesso no Data Warehouse (dw)!")

if HAS_AIRFLOW and DAG is not None:
    with DAG(
        'dag_dw_financeiro_analytics',
        default_args=default_args,
        description='Pipeline ETL de análise do setor Financeiro (dw.fato_fluxo_caixa_mensal e dw.kpi_saude_financeira)',
        schedule='@daily',
        catchup=False,
        tags=['analytics', 'financeiro', 'dw'],
    ) as dag:


        task_financeiro_etl = PythonOperator(
            task_id='processar_analytics_financeiro',
            python_callable=etl_financeiro_analytics,
        )
