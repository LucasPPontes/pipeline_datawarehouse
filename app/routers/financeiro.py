from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.financeiro import ContaBancaria, CategoriaFinanceira, LancamentoFinanceiro, FaturaFinanceira
from app.schemas.financeiro import (
    ContaBancariaCreate, ContaBancariaResponse,
    CategoriaFinanceiraCreate, CategoriaFinanceiraResponse,
    LancamentoFinanceiroCreate, LancamentoFinanceiroResponse,
    FaturaFinanceiraCreate, FaturaFinanceiraResponse,
)

router = APIRouter(
    prefix="/financeiro",
    tags=["Financeiro"],
    dependencies=[Depends(require_roles(["FINANCEIRO"]))]
)

# 1. Contas Bancárias
@router.get("/contas", response_model=List[ContaBancariaResponse], summary="Listar contas bancárias")
def listar_contas(db: Session = Depends(get_db)):
    return db.query(ContaBancaria).all()

@router.post("/contas", response_model=ContaBancariaResponse, status_code=201, summary="Cadastrar conta bancária")
def criar_conta(request: Request, conta: ContaBancariaCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["FINANCEIRO"]))):
    nova_conta = ContaBancaria(**conta.model_dump())
    db.add(nova_conta)
    db.commit()
    db.refresh(nova_conta)
    registrar_auditoria(db, current_user.email, "CRIAR_CONTA_BANCARIA", "/financeiro/contas", "POST", request.client.host if request.client else "127.0.0.1")
    return nova_conta

# 2. Categorias
@router.get("/categorias", response_model=List[CategoriaFinanceiraResponse], summary="Listar categorias financeiras")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(CategoriaFinanceira).all()

@router.post("/categorias", response_model=CategoriaFinanceiraResponse, status_code=201, summary="Cadastrar categoria financeira")
def criar_categoria(request: Request, cat: CategoriaFinanceiraCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["FINANCEIRO"]))):
    nova_cat = CategoriaFinanceira(**cat.model_dump())
    db.add(nova_cat)
    db.commit()
    db.refresh(nova_cat)
    registrar_auditoria(db, current_user.email, "CRIAR_CATEGORIA_FINANCEIRA", "/financeiro/categorias", "POST", request.client.host if request.client else "127.0.0.1")
    return nova_cat

# 3. Lançamentos
@router.get("/lancamentos", response_model=List[LancamentoFinanceiroResponse], summary="Listar lançamentos financeiros")
def listar_lancamentos(db: Session = Depends(get_db)):
    return db.query(LancamentoFinanceiro).all()

@router.post("/lancamentos", response_model=LancamentoFinanceiroResponse, status_code=201, summary="Criar lançamento financeiro")
def criar_lancamento(request: Request, lancamento: LancamentoFinanceiroCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["FINANCEIRO"]))):
    novo = LancamentoFinanceiro(**lancamento.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_LANCAMENTO_FINANCEIRO", "/financeiro/lancamentos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 4. Faturas
@router.get("/faturas", response_model=List[FaturaFinanceiraResponse], summary="Listar faturas")
def listar_faturas(db: Session = Depends(get_db)):
    return db.query(FaturaFinanceira).all()

@router.post("/faturas", response_model=FaturaFinanceiraResponse, status_code=201, summary="Emitir fatura")
def criar_fatura(request: Request, fatura: FaturaFinanceiraCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["FINANCEIRO"]))):
    nova_fat = FaturaFinanceira(**fatura.model_dump())
    db.add(nova_fat)
    db.commit()
    db.refresh(nova_fat)
    registrar_auditoria(db, current_user.email, "CRIAR_FATURA_FINANCEIRA", "/financeiro/faturas", "POST", request.client.host if request.client else "127.0.0.1")
    return nova_fat
