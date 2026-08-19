from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuditLogResponse(BaseModel):
    id: int
    usuario_email: str
    acao: str
    endpoint: str
    metodo: str
    ip_origem: Optional[str] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
