from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.database import Base

class ContaBancaria(Base):
    __tablename__ = "contas_bancarias"
    __table_args__ = {"schema": "financeiro"}

    id = Column(Integer, primary_key=True, index=True)
    banco = Column(String(100), nullable=False)
    agencia = Column(String(20), nullable=False)
    conta = Column(String(30), nullable=False)
    tipo = Column(String(30), nullable=False)
    saldo_atual = Column(Numeric(12, 2), nullable=False, default=0.0)

class CategoriaFinanceira(Base):
    __tablename__ = "categorias"
    __table_args__ = {"schema": "financeiro"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    descricao = Column(String(250), nullable=True)

class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos"
    __table_args__ = {"schema": "financeiro"}

    id = Column(Integer, primary_key=True, index=True)
    conta_id = Column(Integer, ForeignKey("financeiro.contas_bancarias.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("financeiro.categorias.id"), nullable=True)
    descricao = Column(String(200), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(String(20), nullable=False)
    data_vencimento = Column(Date, nullable=False)
    data_pagamento = Column(Date, nullable=True)
    status_pagamento = Column(String(20), nullable=False, default="pendente")

class FaturaFinanceira(Base):
    __tablename__ = "faturas"
    __table_args__ = {"schema": "financeiro"}

    id = Column(Integer, primary_key=True, index=True)
    cliente_fornecedor = Column(String(150), nullable=False)
    numero_fatura = Column(String(50), nullable=False)
    valor_total = Column(Numeric(12, 2), nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_vencimento = Column(Date, nullable=False)
    status = Column(String(30), nullable=False, default="pendente")
