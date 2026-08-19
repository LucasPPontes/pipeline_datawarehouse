from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date
from typing import Optional

# 1. Clientes
class ClienteVendaBase(BaseModel):
    nome: str
    cnpj_cpf: str
    email: EmailStr
    telefone: str
    segmento: str
    data_cadastro: date

class ClienteVendaCreate(ClienteVendaBase):
    pass

class ClienteVendaResponse(ClienteVendaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Produtos
class ProdutoVendaBase(BaseModel):
    nome: str
    categoria: str
    preco_unitario: float
    estoque_disponivel: int = 0
    ativo: Optional[bool] = True

class ProdutoVendaCreate(ProdutoVendaBase):
    pass

class ProdutoVendaResponse(ProdutoVendaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Pedidos
class PedidoVendaBase(BaseModel):
    cliente_id: Optional[int] = None
    cliente_nome: str
    data_venda: date
    valor_total: float
    status: Optional[str] = "pendente"
    canal_venda: Optional[str] = "Venda Direta"
    vendedor_id: Optional[int] = None

class PedidoVendaCreate(PedidoVendaBase):
    pass

class PedidoVendaResponse(PedidoVendaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Itens do Pedido
class ItemPedidoVendaBase(BaseModel):
    pedido_id: int
    produto_id: int
    produto_nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

class ItemPedidoVendaCreate(ItemPedidoVendaBase):
    pass

class ItemPedidoVendaResponse(ItemPedidoVendaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
