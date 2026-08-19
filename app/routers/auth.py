from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List

from app.database import get_db
from app.models.usuario import Usuario
from app.models.audit import AuditLog
from app.schemas.usuario import Token, UsuarioResponse
from app.schemas.audit import AuditLogResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user, require_roles
from app.audit import registrar_auditoria

router = APIRouter(prefix="/auth", tags=["Autenticação & Segurança"])

class LoginJSONRequest(BaseModel):
    email: EmailStr
    senha: str

@router.post("/login", response_model=Token, summary="Autenticação e geração de token JWT")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm envia o email no campo 'username'
    user = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo no sistema"
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    
    # Registrar no audit log
    client_ip = request.client.host if request.client else "127.0.0.1"
    registrar_auditoria(db, user.email, "LOGIN_SUCESSO", "/auth/login", "POST", client_ip)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_email": user.email,
        "role": user.role
    }

@router.get("/me", response_model=UsuarioResponse, summary="Obter dados do usuário logado")
def obter_usuario_logado(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.get("/logs-auditoria", response_model=List[AuditLogResponse], summary="Listar logs de auditoria (Apenas ADMIN)")
def listar_logs_auditoria(
    current_user: Usuario = Depends(require_roles(["ADMIN"])),
    db: Session = Depends(get_db)
):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
