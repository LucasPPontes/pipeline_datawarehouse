from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from app.database import Base

class Contrato(Base):
    __tablename__ = "contratos"
    __table_args__ = {"schema": "juridico"}

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    parte_envolvida = Column(String(150), nullable=False)
    tipo_contrato = Column(String(50), nullable=False)
    valor_contrato = Column(Numeric(12, 2), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=True)
    status = Column(String(30), nullable=False, default="vigente")

class AditivoContrato(Base):
    __tablename__ = "aditivos"
    __table_args__ = {"schema": "juridico"}

    id = Column(Integer, primary_key=True, index=True)
    contrato_id = Column(Integer, ForeignKey("juridico.contratos.id"), nullable=False)
    titulo = Column(String(200), nullable=False)
    descricao_alteracao = Column(String(500), nullable=False)
    valor_adicional = Column(Numeric(10, 2), nullable=False, default=0.0)
    data_assinatura = Column(Date, nullable=False)

class ProcessoJudicial(Base):
    __tablename__ = "processos"
    __table_args__ = {"schema": "juridico"}

    id = Column(Integer, primary_key=True, index=True)
    numero_processo = Column(String(100), nullable=False)
    tribunal = Column(String(150), nullable=False)
    parte_contraria = Column(String(150), nullable=False)
    valor_causa = Column(Numeric(12, 2), nullable=False)
    status_processo = Column(String(50), nullable=False, default="em_andamento")
    data_abertura = Column(Date, nullable=False)

class DocumentoJuridico(Base):
    __tablename__ = "documentos"
    __table_args__ = {"schema": "juridico"}

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    tipo_documento = Column(String(50), nullable=False)
    orgao_emissor = Column(String(150), nullable=False)
    data_emissao = Column(Date, nullable=False)
    data_validade = Column(Date, nullable=True)
    status = Column(String(30), nullable=False, default="valido")
