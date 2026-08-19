from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token, TokenData
from app.schemas.audit import AuditLogResponse
from app.schemas.vendas import (
    ClienteVendaCreate, ClienteVendaResponse,
    ProdutoVendaCreate, ProdutoVendaResponse,
    PedidoVendaCreate, PedidoVendaResponse,
    ItemPedidoVendaCreate, ItemPedidoVendaResponse,
)
from app.schemas.financeiro import (
    ContaBancariaCreate, ContaBancariaResponse,
    CategoriaFinanceiraCreate, CategoriaFinanceiraResponse,
    LancamentoFinanceiroCreate, LancamentoFinanceiroResponse,
    FaturaFinanceiraCreate, FaturaFinanceiraResponse,
)
from app.schemas.juridico import (
    ContratoCreate, ContratoResponse,
    AditivoContratoCreate, AditivoContratoResponse,
    ProcessoJudicialCreate, ProcessoJudicialResponse,
    DocumentoJuridicoCreate, DocumentoJuridicoResponse,
)
from app.schemas.rh import (
    DepartamentoCreate, DepartamentoResponse,
    FuncionarioCreate, FuncionarioResponse,
    FolhaPagamentoCreate, FolhaPagamentoResponse,
    TreinamentoCreate, TreinamentoResponse,
)
from app.schemas.atendimento import (
    ClienteAtendimentoCreate, ClienteAtendimentoResponse,
    TicketAtendimentoCreate, TicketAtendimentoResponse,
    InteracaoTicketCreate, InteracaoTicketResponse,
    PesquisaSatisfacaoCreate, PesquisaSatisfacaoResponse,
)
from app.schemas.infra import (
    EquipamentoInfraCreate, EquipamentoInfraResponse,
    ServidorInfraCreate, ServidorInfraResponse,
    LicencaSoftwareCreate, LicencaSoftwareResponse,
    ManutencaoInfraCreate, ManutencaoInfraResponse,
)

__all__ = [
    "UsuarioCreate", "UsuarioResponse", "Token", "TokenData",
    "AuditLogResponse",
    # Vendas
    "ClienteVendaCreate", "ClienteVendaResponse",
    "ProdutoVendaCreate", "ProdutoVendaResponse",
    "PedidoVendaCreate", "PedidoVendaResponse",
    "ItemPedidoVendaCreate", "ItemPedidoVendaResponse",
    # Financeiro
    "ContaBancariaCreate", "ContaBancariaResponse",
    "CategoriaFinanceiraCreate", "CategoriaFinanceiraResponse",
    "LancamentoFinanceiroCreate", "LancamentoFinanceiroResponse",
    "FaturaFinanceiraCreate", "FaturaFinanceiraResponse",
    # Jurídico
    "ContratoCreate", "ContratoResponse",
    "AditivoContratoCreate", "AditivoContratoResponse",
    "ProcessoJudicialCreate", "ProcessoJudicialResponse",
    "DocumentoJuridicoCreate", "DocumentoJuridicoResponse",
    # RH
    "DepartamentoCreate", "DepartamentoResponse",
    "FuncionarioCreate", "FuncionarioResponse",
    "FolhaPagamentoCreate", "FolhaPagamentoResponse",
    "TreinamentoCreate", "TreinamentoResponse",
    # Atendimento
    "ClienteAtendimentoCreate", "ClienteAtendimentoResponse",
    "TicketAtendimentoCreate", "TicketAtendimentoResponse",
    "InteracaoTicketCreate", "InteracaoTicketResponse",
    "PesquisaSatisfacaoCreate", "PesquisaSatisfacaoResponse",
    "EquipamentoInfraCreate", "EquipamentoInfraResponse",
    "ServidorInfraCreate", "ServidorInfraResponse",
    "LicencaSoftwareCreate", "LicencaSoftwareResponse",
    "ManutencaoInfraCreate", "ManutencaoInfraResponse",
]
