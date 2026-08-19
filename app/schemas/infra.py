from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

# 1. Equipamentos
class EquipamentoInfraBase(BaseModel):
    codigo_patrimonio: str
    nome: str
    tipo: str
    marca_modelo: str
    status: Optional[str] = "em_uso"
    localizacao: str

class EquipamentoInfraCreate(EquipamentoInfraBase):
    pass

class EquipamentoInfraResponse(EquipamentoInfraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 2. Servidores
class ServidorInfraBase(BaseModel):
    nome_host: str
    endereco_ip: str
    sistema_operacional: str
    provedor: str
    status_operacional: Optional[str] = "online"

class ServidorInfraCreate(ServidorInfraBase):
    pass

class ServidorInfraResponse(ServidorInfraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 3. Licenças de Software
class LicencaSoftwareBase(BaseModel):
    nome_software: str
    chave_licenca: str
    fornecedor: str
    quantidade_licencas: int
    data_expiracao: date
    valor_anual: float

class LicencaSoftwareCreate(LicencaSoftwareBase):
    pass

class LicencaSoftwareResponse(LicencaSoftwareBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# 4. Manutenções
class ManutencaoInfraBase(BaseModel):
    equipamento_id: int
    tipo_manutencao: str
    descricao: str
    custo: float = 0.0
    data_manutencao: date
    responsavel: str

class ManutencaoInfraCreate(ManutencaoInfraBase):
    pass

class ManutencaoInfraResponse(ManutencaoInfraBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
