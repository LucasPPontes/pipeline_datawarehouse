from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.juridico import Contrato, AditivoContrato, ProcessoJudicial, DocumentoJuridico
from app.schemas.juridico import (
    ContratoCreate, ContratoResponse,
    AditivoContratoCreate, AditivoContratoResponse,
    ProcessoJudicialCreate, ProcessoJudicialResponse,
    DocumentoJuridicoCreate, DocumentoJuridicoResponse,
)

router = APIRouter(
    prefix="/juridico",
    tags=["Jurídico"],
    dependencies=[Depends(require_roles(["JURIDICO"]))]
)

# 1. Contratos
@router.get("/contratos", response_model=List[ContratoResponse], summary="Listar contratos")
def listar_contratos(db: Session = Depends(get_db)):
    return db.query(Contrato).all()

@router.post("/contratos", response_model=ContratoResponse, status_code=201, summary="Cadastrar novo contrato")
def criar_contrato(request: Request, contrato: ContratoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["JURIDICO"]))):
    novo = Contrato(**contrato.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_CONTRATO_JURIDICO", "/juridico/contratos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 2. Aditivos
@router.get("/aditivos", response_model=List[AditivoContratoResponse], summary="Listar aditivos contratuais")
def listar_aditivos(db: Session = Depends(get_db)):
    return db.query(AditivoContrato).all()

@router.post("/aditivos", response_model=AditivoContratoResponse, status_code=201, summary="Cadastrar aditivo contratual")
def criar_aditivo(request: Request, aditivo: AditivoContratoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["JURIDICO"]))):
    novo = AditivoContrato(**aditivo.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_ADITIVO_CONTRATO", "/juridico/aditivos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 3. Processos
@router.get("/processos", response_model=List[ProcessoJudicialResponse], summary="Listar processos judiciais")
def listar_processos(db: Session = Depends(get_db)):
    return db.query(ProcessoJudicial).all()

@router.post("/processos", response_model=ProcessoJudicialResponse, status_code=201, summary="Cadastrar processo judicial")
def criar_processo(request: Request, proc: ProcessoJudicialCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["JURIDICO"]))):
    novo = ProcessoJudicial(**proc.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_PROCESSO_JUDICIAL", "/juridico/processos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 4. Documentos / Licenças
@router.get("/documentos", response_model=List[DocumentoJuridicoResponse], summary="Listar documentos e licenças jurídicas")
def listar_documentos(db: Session = Depends(get_db)):
    return db.query(DocumentoJuridico).all()

@router.post("/documentos", response_model=DocumentoJuridicoResponse, status_code=201, summary="Cadastrar documento ou licença")
def criar_documento(request: Request, doc: DocumentoJuridicoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["JURIDICO"]))):
    novo = DocumentoJuridico(**doc.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_DOCUMENTO_JURIDICO", "/juridico/documentos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo
