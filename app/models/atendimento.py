from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class ClienteAtendimento(Base):
    __tablename__ = "clientes"
    __table_args__ = {"schema": "atendimento"}

    id = Column(Integer, primary_key=True, index=True)
    nome_contato = Column(String(150), nullable=False)
    empresa = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    telefone = Column(String(30), nullable=False)
    nivel_sla = Column(String(50), nullable=False)

class TicketAtendimento(Base):
    __tablename__ = "tickets"
    __table_args__ = {"schema": "atendimento"}

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("atendimento.clientes.id"), nullable=True)
    cliente_nome = Column(String(150), nullable=False)
    assunto = Column(String(200), nullable=False)
    descricao = Column(String(500), nullable=False)
    prioridade = Column(String(20), nullable=False, default="media")
    status = Column(String(20), nullable=False, default="aberto")
    data_criacao = Column(DateTime, nullable=False)

class InteracaoTicket(Base):
    __tablename__ = "interacoes"
    __table_args__ = {"schema": "atendimento"}

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("atendimento.tickets.id"), nullable=False)
    autor_nome = Column(String(150), nullable=False)
    tipo_autor = Column(String(20), nullable=False)
    mensagem = Column(String(500), nullable=False)
    data_interacao = Column(DateTime, nullable=False)

class PesquisaSatisfacao(Base):
    __tablename__ = "pesquisas_satisfacao"
    __table_args__ = {"schema": "atendimento"}

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("atendimento.tickets.id"), nullable=False)
    nota_satisfacao = Column(Integer, nullable=False)
    comentario = Column(String(500), nullable=True)
    data_resposta = Column(DateTime, nullable=False)
