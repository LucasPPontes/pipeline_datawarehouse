from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from datetime import datetime

def registrar_auditoria(
    db: Session,
    usuario_email: str,
    acao: str,
    endpoint: str,
    metodo: str,
    ip_origem: str = "127.0.0.1"
):
    try:
        log = AuditLog(
            usuario_email=usuario_email,
            acao=acao,
            endpoint=endpoint,
            metodo=metodo,
            ip_origem=ip_origem,
            timestamp=datetime.now()
        )
        db.add(log)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erro ao registrar audit log: {e}")
