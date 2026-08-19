from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "seguranca"}

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    cargo = Column(String(100), nullable=False)
    role = Column(String(30), nullable=False, default="VENDAS")
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.now)
