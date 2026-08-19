from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app.routers import (
    auth_router,
    rh_router,
    vendas_router,
    financeiro_router,
    juridico_router,
    atendimento_router,
    infra_router,
)
from app.seed import seed_database, criar_schemas

# Configuração do Rate Limiter (Slowapi)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Cria os Schemas no PostgreSQL antes de mapear as tabelas
criar_schemas()

# Inicializa as tabelas no banco de dados ao carregar a aplicação
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini ERP API - Pequenas Empresas (Segura)",
    description="API RESTful para gestão ERP com Autenticação JWT, Controle de Acesso por Função (RBAC), Rate Limiting e Auditoria.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Adiciona estado do Limiter e handler de erro HTTP 429
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 1. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens confiáveis (ex: https://erp.suaempresa.com)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 2. Security Headers Middleware (OWASP)
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Aplica Content-Security-Policy apenas fora das rotas de documentação para permitir o funcionamento do Swagger UI
    if not request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
        response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response


# Registra os roteadores
app.include_router(auth_router)
app.include_router(vendas_router)
app.include_router(financeiro_router)
app.include_router(juridico_router)
app.include_router(rh_router)
app.include_router(atendimento_router)
app.include_router(infra_router)

@app.on_event("startup")
def startup_event():
    # Executa a carga inicial dos dados JSON no PostgreSQL se as tabelas estiverem vazias
    seed_database()

@app.get("/", tags=["Início"])
def root():
    return {
        "mensagem": "Bem-vindo à API Segura do Mini ERP",
        "seguranca": {
            "autenticacao": "JWT (OAuth2 Bearer Token)",
            "autorizacao": "RBAC por setor (ADMIN, VENDAS, FINANCEIRO, JURIDICO, RH, ATENDIMENTO, INFRA)",
            "rate_limiting": "Ativo (100 req/min)",
            "audit_trail": "Ativo em audit_logs"
        },
        "documentacao": "/docs",
        "login": "/auth/login"
    }
