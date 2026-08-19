from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_roles
from app.audit import registrar_auditoria
from app.models.infra import EquipamentoInfra, ServidorInfra, LicencaSoftware, ManutencaoInfra
from app.schemas.infra import (
    EquipamentoInfraCreate, EquipamentoInfraResponse,
    ServidorInfraCreate, ServidorInfraResponse,
    LicencaSoftwareCreate, LicencaSoftwareResponse,
    ManutencaoInfraCreate, ManutencaoInfraResponse,
)

router = APIRouter(
    prefix="/infra",
    tags=["Infraestrutura"],
    dependencies=[Depends(require_roles(["INFRA"]))]
)

# 1. Equipamentos
@router.get("/equipamentos", response_model=List[EquipamentoInfraResponse], summary="Listar equipamentos de TI")
def listar_equipamentos(db: Session = Depends(get_db)):
    return db.query(EquipamentoInfra).all()

@router.post("/equipamentos", response_model=EquipamentoInfraResponse, status_code=201, summary="Cadastrar equipamento de TI")
def criar_equipamento(request: Request, eq: EquipamentoInfraCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["INFRA"]))):
    novo = EquipamentoInfra(**eq.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_EQUIPAMENTO_INFRA", "/infra/equipamentos", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 2. Servidores
@router.get("/servidores", response_model=List[ServidorInfraResponse], summary="Listar servidores e instâncias cloud")
def listar_servidores(db: Session = Depends(get_db)):
    return db.query(ServidorInfra).all()

@router.post("/servidores", response_model=ServidorInfraResponse, status_code=201, summary="Cadastrar servidor")
def criar_servidor(request: Request, srv: ServidorInfraCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["INFRA"]))):
    novo = ServidorInfra(**srv.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_SERVIDOR_INFRA", "/infra/servidores", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 3. Licenças de Software
@router.get("/licencas", response_model=List[LicencaSoftwareResponse], summary="Listar licenças de software")
def listar_licencas(db: Session = Depends(get_db)):
    return db.query(LicencaSoftware).all()

@router.post("/licencas", response_model=LicencaSoftwareResponse, status_code=201, summary="Cadastrar licença de software")
def criar_licenca(request: Request, lic: LicencaSoftwareCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["INFRA"]))):
    novo = LicencaSoftware(**lic.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_LICENCA_INFRA", "/infra/licencas", "POST", request.client.host if request.client else "127.0.0.1")
    return novo

# 4. Manutenções
@router.get("/manutencoes", response_model=List[ManutencaoInfraResponse], summary="Listar históricos de manutenção")
def listar_manutencoes(db: Session = Depends(get_db)):
    return db.query(ManutencaoInfra).all()

@router.post("/manutencoes", response_model=ManutencaoInfraResponse, status_code=201, summary="Registrar manutenção")
def criar_manutencao(request: Request, manut: ManutencaoInfraCreate, db: Session = Depends(get_db), current_user=Depends(require_roles(["INFRA"]))):
    novo = ManutencaoInfra(**manut.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    registrar_auditoria(db, current_user.email, "CRIAR_MANUTENCAO_INFRA", "/infra/manutencoes", "POST", request.client.host if request.client else "127.0.0.1")
    return novo
