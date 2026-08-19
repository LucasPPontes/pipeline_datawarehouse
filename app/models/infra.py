from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.database import Base

class EquipamentoInfra(Base):
    __tablename__ = "equipamentos"
    __table_args__ = {"schema": "infra"}

    id = Column(Integer, primary_key=True, index=True)
    codigo_patrimonio = Column(String(50), nullable=False)
    nome = Column(String(150), nullable=False)
    tipo = Column(String(50), nullable=False)
    marca_modelo = Column(String(150), nullable=False)
    status = Column(String(30), nullable=False, default="em_uso")
    localizacao = Column(String(150), nullable=False)

class ServidorInfra(Base):
    __tablename__ = "servidores"
    __table_args__ = {"schema": "infra"}

    id = Column(Integer, primary_key=True, index=True)
    nome_host = Column(String(150), nullable=False)
    endereco_ip = Column(String(50), nullable=False)
    sistema_operacional = Column(String(100), nullable=False)
    provedor = Column(String(100), nullable=False)
    status_operacional = Column(String(30), nullable=False, default="online")

class LicencaSoftware(Base):
    __tablename__ = "licencas_software"
    __table_args__ = {"schema": "infra"}

    id = Column(Integer, primary_key=True, index=True)
    nome_software = Column(String(150), nullable=False)
    chave_licenca = Column(String(100), nullable=False)
    fornecedor = Column(String(150), nullable=False)
    quantidade_licencas = Column(Integer, nullable=False)
    data_expiracao = Column(Date, nullable=False)
    valor_anual = Column(Numeric(10, 2), nullable=False)

class ManutencaoInfra(Base):
    __tablename__ = "manutencoes"
    __table_args__ = {"schema": "infra"}

    id = Column(Integer, primary_key=True, index=True)
    equipamento_id = Column(Integer, ForeignKey("infra.equipamentos.id"), nullable=False)
    tipo_manutencao = Column(String(30), nullable=False)
    descricao = Column(String(300), nullable=False)
    custo = Column(Numeric(10, 2), nullable=False, default=0.0)
    data_manutencao = Column(Date, nullable=False)
    responsavel = Column(String(150), nullable=False)
