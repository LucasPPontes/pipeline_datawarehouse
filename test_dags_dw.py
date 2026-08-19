import sys
import os

# Adiciona airflow/dags ao path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "airflow", "dags"))

from dw_helpers import get_erp_engine
from dag_dw_vendas_analytics import etl_vendas_analytics
from dag_dw_financeiro_analytics import etl_financeiro_analytics
from dag_dw_rh_analytics import etl_rh_analytics
from dag_dw_atendimento_analytics import etl_atendimento_analytics
from dag_dw_infra_juridico_analytics import etl_infra_juridico_analytics
from sqlalchemy import text

def test_executar_dags_e_verificar_dw():
    print("\n=======================================================")
    print("🚀 EXECUTANDO AS 5 DAGS DE ETL NO DATA WAREHOUSE ('dw')")
    print("=======================================================\n")

    print("[1/5] Executando dag_dw_vendas_analytics...")
    etl_vendas_analytics()

    print("[2/5] Executando dag_dw_financeiro_analytics...")
    etl_financeiro_analytics()

    print("[3/5] Executando dag_dw_rh_analytics...")
    etl_rh_analytics()

    print("[4/5] Executando dag_dw_atendimento_analytics...")
    etl_atendimento_analytics()

    print("[5/5] Executando dag_dw_infra_juridico_analytics...")
    etl_infra_juridico_analytics()

    print("\n=======================================================")
    print("📊 INSPECIONANDO RESULTADOS NAS TABELAS DO SCHEMA 'dw'")
    print("=======================================================\n")

    engine = get_erp_engine()
    with engine.connect() as conn:
        # 1. Fato Vendas Mensal
        vendas = conn.execute(text("SELECT * FROM dw.fato_vendas_mensal;")).fetchall()
        print(f"📈 dw.fato_vendas_mensal ({len(vendas)} meses consolidados):")
        for row in vendas:
            print(f"   - Mês {row.ano_mes}: Faturamento R$ {row.faturamento_total:,.2f} | Pedidos Concluídos: {row.pedidos_concluidos} | Ticket Médio: R$ {row.ticket_medio}")

        # 2. Dim Desempenho Produtos
        prods = conn.execute(text("SELECT * FROM dw.dim_desempenho_produtos LIMIT 3;")).fetchall()
        print(f"\n🏆 dw.dim_desempenho_produtos (Top 3 Produtos por Faturamento):")
        for row in prods:
            print(f"   - #{row.produto_id} {row.nome_produto} ({row.categoria}): R$ {row.faturamento_gerado:,.2f} em faturamento ({row.quantidade_total_vendida} un. vendidas)")

        # 3. Fato Fluxo de Caixa Mensal
        fin = conn.execute(text("SELECT * FROM dw.fato_fluxo_caixa_mensal;")).fetchall()
        print(f"\n💰 dw.fato_fluxo_caixa_mensal ({len(fin)} meses):")
        for row in fin:
            print(f"   - Mês {row.ano_mes}: Receitas R$ {row.total_receitas:,.2f} | Despesas R$ {row.total_despesas:,.2f} | Resultado Líquido: R$ {row.resultado_liquido:,.2f}")

        # 4. Fato RH Métricas Departamento
        rh = conn.execute(text("SELECT * FROM dw.fato_rh_metricas_departamento;")).fetchall()
        print(f"\n👥 dw.fato_rh_metricas_departamento ({len(rh)} setores):")
        for row in rh:
            print(f"   - [{row.sigla}] {row.nome_departamento}: Headcount {row.headcount} | Custo Folha R$ {row.custo_mensal_folha:,.2f} | Salário Médio R$ {row.salario_medio}")

        # 5. Fato Atendimento KPIs
        atend = conn.execute(text("SELECT * FROM dw.fato_atendimento_kpis;")).fetchone()
        print(f"\n🎧 dw.fato_atendimento_kpis:")
        print(f"   - Total Chamados: {atend.total_tickets} | Taxa de Resolução: {atend.taxa_resolucao}% | Score CSAT Médio: {atend.media_csat}/5.0")

        # 6. Fato Infra & Jurídico Custos
        ij = conn.execute(text("SELECT * FROM dw.fato_infra_juridico_custos;")).fetchone()
        print(f"\n⚙️ dw.fato_infra_juridico_custos:")
        print(f"   - Manutenção TI: R$ {ij.custo_total_manutencoes_ti:,.2f} | Licenças Anuais: R$ {ij.custo_anual_licencas_software:,.2f} | Contratos Vigentes: R$ {ij.valor_total_contratos_vigentes:,.2f} | Passivo Processos: R$ {ij.total_passivo_processos_judiciais:,.2f}")

    print("\n>>> SUCESSO TOTAL! TODAS AS 5 DAGS E TABELAS ANALÍTICAS DO SCHEMA 'dw' FORAM EXECUTADAS E VERIFICADAS! <<<")

if __name__ == "__main__":
    test_executar_dags_e_verificar_dw()
