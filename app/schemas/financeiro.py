from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# 1. Contas Bancárias
class ContaBancariaBase(BaseModel):
    banco: str
    agencia: str
    conta: str
    tipo: str
    saldo_atual: float = 0.0

class ContaBancariaCreate(ContaBancariaBase):
    pass

class ContaBancariaResponse(ContaBancariaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Categorias Financeiras
class CategoriaFinanceiraBase(BaseModel):
    nome: str
    tipo: str
    descricao: Optional[str] = None

class CategoriaFinanceiraCreate(CategoriaFinanceiraBase):
    pass

class CategoriaFinanceiraResponse(CategoriaFinanceiraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Lançamentos
class LancamentoFinanceiroBase(BaseModel):
    conta_id: Optional[int] = None
    categoria_id: Optional[int] = None
    descricao: str
    valor: float
    tipo: str
    data_vencimento: date
    data_pagamento: Optional[date] = None
    status_pagamento: Optional[str] = "pendente"

class LancamentoFinanceiroCreate(LancamentoFinanceiroBase):
    pass

class LancamentoFinanceiroResponse(LancamentoFinanceiroBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Faturas
class FaturaFinanceiraBase(BaseModel):
    cliente_fornecedor: str
    numero_fatura: str
    valor_total: float
    data_emissao: date
    data_vencimento: date
    status: Optional[str] = "pendente"

class FaturaFinanceiraCreate(FaturaFinanceiraBase):
    pass

class FaturaFinanceiraResponse(FaturaFinanceiraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
