from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

# 1. Clientes Atendimento
class ClienteAtendimentoBase(BaseModel):
    nome_contato: str
    empresa: str
    email: EmailStr
    telefone: str
    nivel_sla: str

class ClienteAtendimentoCreate(ClienteAtendimentoBase):
    pass

class ClienteAtendimentoResponse(ClienteAtendimentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Tickets
class TicketAtendimentoBase(BaseModel):
    cliente_id: Optional[int] = None
    cliente_nome: str
    assunto: str
    descricao: str
    prioridade: Optional[str] = "media"
    status: Optional[str] = "aberto"
    data_criacao: Optional[datetime] = None

class TicketAtendimentoCreate(TicketAtendimentoBase):
    pass

class TicketAtendimentoResponse(TicketAtendimentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Interações do Ticket
class InteracaoTicketBase(BaseModel):
    ticket_id: int
    autor_nome: str
    tipo_autor: str
    mensagem: str
    data_interacao: Optional[datetime] = None

class InteracaoTicketCreate(InteracaoTicketBase):
    pass

class InteracaoTicketResponse(InteracaoTicketBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Pesquisas de Satisfação
class PesquisaSatisfacaoBase(BaseModel):
    ticket_id: int
    nota_satisfacao: int
    comentario: Optional[str] = None
    data_resposta: Optional[datetime] = None

class PesquisaSatisfacaoCreate(PesquisaSatisfacaoBase):
    pass

class PesquisaSatisfacaoResponse(PesquisaSatisfacaoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
