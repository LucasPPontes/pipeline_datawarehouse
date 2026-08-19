from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.rh import Departamento, Funcionario, FolhaPagamento, Treinamento
from app.schemas.rh import (
    DepartamentoCreate, DepartamentoResponse,
    FuncionarioCreate, FuncionarioResponse,
    FolhaPagamentoCreate, FolhaPagamentoResponse,
    TreinamentoCreate, TreinamentoResponse,
)

router = APIRouter(
    prefix="/rh",
    tags=["RH - Recursos Humanos"],
    dependencies=[Depends(require_roles(["RH"]))]
)

# 1. Departamentos
@router.get("/departamentos", response_model=List[DepartamentoResponse], summary="Listar departamentos")
def listar_departamentos(db: Session = Depends(get_db)):
    return db.query(Departamento).all()

@router.post("/departamentos", response_model=DepartamentoResponse, status_code=201, summary="Cadastrar departamento")
def criar_departamento(request: Request, dep: DepartamentoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["RH"]))):
    novo = Departamento(**dep.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_DEPARTAMENTO_RH", "/rh/departamentos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 2. Funcionários
@router.get("/funcionarios", response_model=List[FuncionarioResponse], summary="Listar funcionários")
def listar_funcionarios(db: Session = Depends(get_db)):
    return db.query(Funcionario).all()

@router.post("/funcionarios", response_model=FuncionarioResponse, status_code=201, summary="Cadastrar funcionário")
def criar_funcionario(request: Request, func: FuncionarioCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["RH"]))):
    novo = Funcionario(**func.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_FUNCIONARIO_RH", "/rh/funcionarios", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 3. Folha de Pagamento
@router.get("/folha-pagamento", response_model=List[FolhaPagamentoResponse], summary="Listar holerites/folhas de pagamento")
def listar_folha(db: Session = Depends(get_db)):
    return db.query(FolhaPagamento).all()

@router.post("/folha-pagamento", response_model=FolhaPagamentoResponse, status_code=201, summary="Gerar folha de pagamento")
def criar_folha(request: Request, folha: FolhaPagamentoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["RH"]))):
    novo = FolhaPagamento(**folha.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "GERAR_FOLHA_PAGAMENTO_RH", "/rh/folha-pagamento", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 4. Treinamentos
@router.get("/treinamentos", response_model=List[TreinamentoResponse], summary="Listar treinamentos")
def listar_treinamentos(db: Session = Depends(get_db)):
    return db.query(Treinamento).all()

@router.post("/treinamentos", response_model=TreinamentoResponse, status_code=201, summary="Cadastrar treinamento")
def criar_treinamento(request: Request, treino: TreinamentoCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["RH"]))):
    novo = Treinamento(**treino.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_TREINAMENTO_RH", "/rh/treinamentos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo
