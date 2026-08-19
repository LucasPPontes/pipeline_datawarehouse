from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date
from typing import Optional

# 1. Departamentos
class DepartamentoBase(BaseModel):
    nome: str
    sigla: str
    gestor_nome: str
    orcamento_anual: float = 0.0

class DepartamentoCreate(DepartamentoBase):
    pass

class DepartamentoResponse(DepartamentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Funcionários
class FuncionarioBase(BaseModel):
    departamento_id: Optional[int] = None
    nome: str
    cpf: str
    cargo: str
    salario: float
    data_admissao: date
    email: EmailStr
    status: Optional[str] = "ativo"

class FuncionarioCreate(FuncionarioBase):
    pass

class FuncionarioResponse(FuncionarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Folha de Pagamento
class FolhaPagamentoBase(BaseModel):
    funcionario_id: int
    mes_referencia: int
    ano_referencia: int
    salario_bruto: float
    descontos: float
    salario_liquido: float
    status_pagamento: Optional[str] = "pago"

class FolhaPagamentoCreate(FolhaPagamentoBase):
    pass

class FolhaPagamentoResponse(FolhaPagamentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Treinamentos
class TreinamentoBase(BaseModel):
    titulo: str
    carga_horaria: int
    instrutor: str
    data_inicio: date
    status: Optional[str] = "agendado"

class TreinamentoCreate(TreinamentoBase):
    pass

class TreinamentoResponse(TreinamentoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
