from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.atendimento import ClienteAtendimento, TicketAtendimento, InteracaoTicket, PesquisaSatisfacao
from app.schemas.atendimento import (
    ClienteAtendimentoCreate, ClienteAtendimentoResponse,
    TicketAtendimentoCreate, TicketAtendimentoResponse,
    InteracaoTicketCreate, InteracaoTicketResponse,
    PesquisaSatisfacaoCreate, PesquisaSatisfacaoResponse,
)

router = APIRouter(
    prefix="/atendimento",
    tags=["Atendimento ao Cliente"],
    dependencies=[Depends(require_roles(["ATENDIMENTO"]))]
)

# 1. Clientes Atendimento
@router.get("/clientes", response_model=List[ClienteAtendimentoResponse], summary="Listar contatos de clientes para suporte")
def listar_clientes_atendimento(db: Session = Depends(get_db)):
    return db.query(ClienteAtendimento).all()

@router.post("/clientes", response_model=ClienteAtendimentoResponse, status_code=201, summary="Cadastrar contato de suporte")
def criar_cliente_atendimento(request: Request, cli: ClienteAtendimentoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ATENDIMENTO"]))):
    novo = ClienteAtendimento(**cli.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_CLIENTE_ATENDIMENTO", "/atendimento/clientes", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 2. Tickets
@router.get("/tickets", response_model=List[TicketAtendimentoResponse], summary="Listar tickets de suporte")
def listar_tickets(db: Session = Depends(get_db)):
    return db.query(TicketAtendimento).all()

@router.post("/tickets", response_model=TicketAtendimentoResponse, status_code=201, summary="Abrir ticket de suporte")
def criar_ticket(request: Request, ticket: TicketAtendimentoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ATENDIMENTO"]))):
    data = ticket.model_dump()
    if not data.get("data_criacao"):
        data["data_criacao"] = datetime.now()
    novo = TicketAtendimento(**data)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_TICKET_ATENDIMENTO", "/atendimento/tickets", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 3. Interações do Ticket
@router.get("/interacoes", response_model=List[InteracaoTicketResponse], summary="Listar interações dos tickets")
def listar_interacoes(db: Session = Depends(get_db)):
    return db.query(InteracaoTicket).all()

@router.post("/interacoes", response_model=InteracaoTicketResponse, status_code=201, summary="Adicionar resposta ao ticket")
def criar_interacao(request: Request, inter: InteracaoTicketCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ATENDIMENTO"]))):
    data = inter.model_dump()
    if not data.get("data_interacao"):
        data["data_interacao"] = datetime.now()
    novo = InteracaoTicket(**data)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_INTERACAO_TICKET", "/atendimento/interacoes", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 4. Pesquisas de Satisfação
@router.get("/pesquisas", response_model=List[PesquisaSatisfacaoResponse], summary="Listar pesquisas de satisfação")
def listar_pesquisas(db: Session = Depends(get_db)):
    return db.query(PesquisaSatisfacao).all()

@router.post("/pesquisas", response_model=PesquisaSatisfacaoResponse, status_code=201, summary="Enviar pesquisa de satisfação")
def criar_pesquisa(request: Request, pesq: PesquisaSatisfacaoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["ATENDIMENTO"]))):
    data = pesq.model_dump()
    if not data.get("data_resposta"):
        data["data_resposta"] = datetime.now()
    novo = PesquisaSatisfacao(**data)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_PESQUISA_SATISFACAO", "/atendimento/pesquisas", "POST", request.client.host if request.client else "127.0.0.1")
    return novo
