from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, ForeignKey
from app.database import Base

class ClienteVenda(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "vendas"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cnpj_cpf = Column(String(20), nullable=False)
    email = Column(String(150), nullable=False)
    telefone = Column(String(30), nullable=False)
    segmento = Column(String(100), nullable=False)
    data_cadastro = Column(Date, nullable=False)

class ProdutoVenda(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema": "vendas"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    categoria = Column(String(100), nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    estoque_disponivel = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, default=True)

class PedidoVenda(Base):
    __tablename__ = "pedidos"
    __table_args__ = {"schema": "vendas"}

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("vendas.clientes.id"), nullable=True)
    cliente_nome = Column(String(150), nullable=False)
    data_venda = Column(Date, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False, default="pendente")
    canal_venda = Column(String(50), nullable=False, default="Venda Direta")
    vendedor_id = Column(Integer, nullable=True)

class ItemPedidoVenda(Base):
    __tablename__ = "itens_pedido"
    __table_args__ = {"schema": "vendas"}

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("vendas.pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("vendas.produtos.id"), nullable=False)
    produto_nome = Column(String(150), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
