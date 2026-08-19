from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {"schema": "seguranca"}

    id = Column(Integer, primary_key=True, index=True)
    usuario_email = Column(String(150), nullable=False)
    acao = Column(String(100), nullable=False)
    endpoint = Column(String(200), nullable=False)
    metodo = Column(String(10), nullable=False)
    ip_origem = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.now)
