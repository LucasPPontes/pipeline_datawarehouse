from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# 1. Contratos
class ContratoBase(BaseModel):
    titulo: str
    parte_envolvida: str
    tipo_contrato: str
    valor_contrato: float
    data_inicio: date
    data_fim: Optional[date] = None
    status: Optional[str] = "vigente"

class ContratoCreate(ContratoBase):
    pass

class ContratoResponse(ContratoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Aditivos
class AditivoContratoBase(BaseModel):
    contrato_id: int
    titulo: str
    descricao_alteracao: str
    valor_adicional: float = 0.0
    data_assinatura: date

class AditivoContratoCreate(AditivoContratoBase):
    pass

class AditivoContratoResponse(AditivoContratoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Processos Judiciais
class ProcessoJudicialBase(BaseModel):
    numero_processo: str
    tribunal: str
    parte_contraria: str
    valor_causa: float
    status_processo: Optional[str] = "em_andamento"
    data_abertura: date

class ProcessoJudicialCreate(ProcessoJudicialBase):
    pass

class ProcessoJudicialResponse(ProcessoJudicialBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Documentos Jurídicos
class DocumentoJuridicoBase(BaseModel):
    titulo: str
    tipo_documento: str
    orgao_emissor: str
    data_emissao: date
    data_validade: Optional[date] = None
    status: Optional[str] = "valido"

class DocumentoJuridicoCreate(DocumentoJuridicoBase):
    pass

class DocumentoJuridicoResponse(DocumentoJuridicoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
