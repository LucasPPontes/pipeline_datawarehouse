from app.routers.auth import router as auth_router
from app.routers.rh import router as rh_router
from app.routers.vendas import router as vendas_router
from app.routers.financeiro import router as financeiro_router
from app.routers.juridico import router as juridico_router
from app.routers.atendimento import router as atendimento_router
from app.routers.infra import router as infra_router

__all__ = [
    "auth_router",
    "rh_router",
    "vendas_router",
    "financeiro_router",
    "juridico_router",
    "atendimento_router",
    "infra_router",
]
