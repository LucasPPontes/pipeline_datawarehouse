from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.database import Base

class Departamento(Base):
    __tablename__ = "departamentos"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    sigla = Column(String(20), nullable=False)
    gestor_nome = Column(String(150), nullable=False)
    orcamento_anual = Column(Numeric(12, 2), nullable=False, default=0.0)

class Funcionario(Base):
    __tablename__ = "funcionarios"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True, index=True)
    departamento_id = Column(Integer, ForeignKey("rh.departamentos.id"), nullable=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(20), nullable=False)
    cargo = Column(String(100), nullable=False)
    salario = Column(Numeric(10, 2), nullable=False)
    data_admissao = Column(Date, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    status = Column(String(20), default="ativo")

class FolhaPagamento(Base):
    __tablename__ = "folha_pagamento"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey("rh.funcionarios.id"), nullable=False)
    mes_referencia = Column(Integer, nullable=False)
    ano_referencia = Column(Integer, nullable=False)
    salario_bruto = Column(Numeric(10, 2), nullable=False)
    descontos = Column(Numeric(10, 2), nullable=False)
    salario_liquido = Column(Numeric(10, 2), nullable=False)
    status_pagamento = Column(String(20), default="pago")

class Treinamento(Base):
    __tablename__ = "treinamentos"
    __table_args__ = {"schema": "rh"}

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    instrutor = Column(String(150), nullable=False)
    data_inicio = Column(Date, nullable=False)
    status = Column(String(30), default="agendado")
