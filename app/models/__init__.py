from app.models.usuario import Usuario
from app.models.audit import AuditLog
from app.models.vendas import ClienteVenda, ProdutoVenda, PedidoVenda, ItemPedidoVenda
from app.models.financeiro import ContaBancaria, CategoriaFinanceira, LancamentoFinanceiro, FaturaFinanceira
from app.models.juridico import Contrato, AditivoContrato, ProcessoJudicial, DocumentoJuridico
from app.models.rh import Departamento, Funcionario, FolhaPagamento, Treinamento
from app.models.atendimento import ClienteAtendimento, TicketAtendimento, InteracaoTicket, PesquisaSatisfacao
from app.models.infra import EquipamentoInfra, ServidorInfra, LicencaSoftware, ManutencaoInfra

__all__ = [
    "Usuario",
    "AuditLog",
    # Vendas
    "ClienteVenda",
    "ProdutoVenda",
    "PedidoVenda",
    "ItemPedidoVenda",
    # Financeiro
    "ContaBancaria",
    "CategoriaFinanceira",
    "LancamentoFinanceiro",
    "FaturaFinanceira",
    # Jurídico
    "Contrato",
    "AditivoContrato",
    "ProcessoJudicial",
    "DocumentoJuridico",
    # RH
    "Departamento",
    "Funcionario",
    "FolhaPagamento",
    "Treinamento",
    # Atendimento
    "ClienteAtendimento",
    "TicketAtendimento",
    "InteracaoTicket",
    "PesquisaSatisfacao",
    # Infraestrutura
    "EquipamentoInfra",
    "ServidorInfra",
    "LicencaSoftware",
    "ManutencaoInfra",
]
