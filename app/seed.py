import os
import json
from datetime import datetime, date
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.auth import hash_password
from app.models import (
    Usuario, AuditLog,
    # Vendas
    ClienteVenda, ProdutoVenda, PedidoVenda, ItemPedidoVenda,
    # Financeiro
    ContaBancaria, CategoriaFinanceira, LancamentoFinanceiro, FaturaFinanceira,
    # Jurídico
    Contrato, AditivoContrato, ProcessoJudicial, DocumentoJuridico,
    # RH
    Departamento, Funcionario, FolhaPagamento, Treinamento,
    # Atendimento
    ClienteAtendimento, TicketAtendimento, InteracaoTicket, PesquisaSatisfacao,
    # Infraestrutura
    EquipamentoInfra, ServidorInfra, LicencaSoftware, ManutencaoInfra,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def criar_schemas():
    schemas = ["seguranca", "vendas", "financeiro", "juridico", "rh", "atendimento", "infra"]
    with engine.connect() as conn:
        for schema in schemas:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
        conn.commit()
    print("-> Schemas do PostgreSQL criados/verificados com sucesso!")

def populate_table(db, model, json_filename, date_fields=None, datetime_fields=None):
    file_path = os.path.join(DATA_DIR, json_filename)
    if not os.path.exists(file_path):
        print(f"-> Arquivo {json_filename} não encontrado.")
        return 0

    with open(file_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        if date_fields:
            for field in date_fields:
                if item.get(field):
                    item[field] = date.fromisoformat(item[field])
        if datetime_fields:
            for field in datetime_fields:
                if item.get(field):
                    item[field] = datetime.fromisoformat(item[field])
        db.add(model(**item))

    db.commit()
    return len(items)

def populate_usuarios(db):
    file_path = os.path.join(DATA_DIR, "usuarios.json")
    if not os.path.exists(file_path):
        print("-> Arquivo usuarios.json não encontrado.")
        return 0

    with open(file_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    for item in items:
        senha_plana = item.pop("senha_plana", "123456")
        item["senha_hash"] = hash_password(senha_plana)
        db.add(Usuario(**item))

    db.commit()
    return len(items)

def seed_database():
    print("Criando Schemas e recriando Tabelas no PostgreSQL...")
    criar_schemas()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Iniciando carga de dados nos 7 Schemas e 26 tabelas...")

        # 0. SEGURANÇA
        n_usuarios = populate_usuarios(db)
        print(f"-> Inseridos {n_usuarios} usuários em 'seguranca.usuarios'")

        # 1. VENDAS
        n_cli_vendas = populate_table(db, ClienteVenda, "vendas_clientes.json", date_fields=["data_cadastro"])
        n_prod_vendas = populate_table(db, ProdutoVenda, "vendas_produtos.json")
        n_ped_vendas = populate_table(db, PedidoVenda, "vendas_pedidos.json", date_fields=["data_venda"])
        n_itens_vendas = populate_table(db, ItemPedidoVenda, "vendas_itens_pedido.json")

        # 2. FINANCEIRO
        n_contas_fin = populate_table(db, ContaBancaria, "financeiro_contas.json")
        n_cat_fin = populate_table(db, CategoriaFinanceira, "financeiro_categorias.json")
        n_lanc_fin = populate_table(db, LancamentoFinanceiro, "financeiro_lancamentos.json", date_fields=["data_vencimento", "data_pagamento"])
        n_fat_fin = populate_table(db, FaturaFinanceira, "financeiro_faturas.json", date_fields=["data_emissao", "data_vencimento"])

        # 3. JURÍDICO
        n_contr_jur = populate_table(db, Contrato, "juridico_contratos.json", date_fields=["data_inicio", "data_fim"])
        n_adit_jur = populate_table(db, AditivoContrato, "juridico_aditivos.json", date_fields=["data_assinatura"])
        n_proc_jur = populate_table(db, ProcessoJudicial, "juridico_processos.json", date_fields=["data_abertura"])
        n_doc_jur = populate_table(db, DocumentoJuridico, "juridico_documentos.json", date_fields=["data_emissao", "data_validade"])

        # 4. RH
        n_dep_rh = populate_table(db, Departamento, "rh_departamentos.json")
        n_func_rh = populate_table(db, Funcionario, "rh_funcionarios.json", date_fields=["data_admissao"])
        n_folha_rh = populate_table(db, FolhaPagamento, "rh_folha_pagamento.json")
        n_trein_rh = populate_table(db, Treinamento, "rh_treinamentos.json", date_fields=["data_inicio"])

        # 5. ATENDIMENTO
        n_cli_atend = populate_table(db, ClienteAtendimento, "atendimento_clientes.json")
        n_tick_atend = populate_table(db, TicketAtendimento, "atendimento_tickets.json", datetime_fields=["data_criacao"])
        n_inter_atend = populate_table(db, InteracaoTicket, "atendimento_interacoes.json", datetime_fields=["data_interacao"])
        n_pesq_atend = populate_table(db, PesquisaSatisfacao, "atendimento_pesquisas.json", datetime_fields=["data_resposta"])

        # 6. INFRAESTRUTURA
        n_eq_infra = populate_table(db, EquipamentoInfra, "infra_equipamentos.json")
        n_srv_infra = populate_table(db, ServidorInfra, "infra_servidores.json")
        n_lic_infra = populate_table(db, LicencaSoftware, "infra_licencas.json", date_fields=["data_expiracao"])
        n_manut_infra = populate_table(db, ManutencaoInfra, "infra_manutencoes.json", date_fields=["data_manutencao"])

        # Atualiza a sequência do PostgreSQL para todas as tabelas dentro dos schemas
        tables = [
            "seguranca.usuarios", "seguranca.audit_logs",
            "vendas.clientes", "vendas.produtos", "vendas.pedidos", "vendas.itens_pedido",
            "financeiro.contas_bancarias", "financeiro.categorias", "financeiro.lancamentos", "financeiro.faturas",
            "juridico.contratos", "juridico.aditivos", "juridico.processos", "juridico.documentos",
            "rh.departamentos", "rh.funcionarios", "rh.folha_pagamento", "rh.treinamentos",
            "atendimento.clientes", "atendimento.tickets", "atendimento.interacoes", "atendimento.pesquisas_satisfacao",
            "infra.equipamentos", "infra.servidores", "infra.licencas_software", "infra.manutencoes"
        ]

        print("Ajustando sequências de ID no PostgreSQL...")
        for table in tables:
            db.execute(text(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE((SELECT MAX(id) FROM {table}), 1));"))
        db.commit()

        total_registros = (
            n_usuarios +
            n_cli_vendas + n_prod_vendas + n_ped_vendas + n_itens_vendas +
            n_contas_fin + n_cat_fin + n_lanc_fin + n_fat_fin +
            n_contr_jur + n_adit_jur + n_proc_jur + n_doc_jur +
            n_dep_rh + n_func_rh + n_folha_rh + n_trein_rh +
            n_cli_atend + n_tick_atend + n_inter_atend + n_pesq_atend +
            n_eq_infra + n_srv_infra + n_lic_infra + n_manut_infra
        )

        print(f"✅ Popular banco por Schemas finalizado com SUCESSO! Total de registros: {total_registros}")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao popular banco de dados: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
