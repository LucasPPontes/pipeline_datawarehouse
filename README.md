# 🚀 Mini ERP Backend, Database Schemas & Apache Airflow Data Warehouse

> ⚠️ **Aviso Importante:** Todos os dados, métricas e informações contidos neste projeto são **100% fictícios**. Este repositório foi desenvolvido estritamente para uso pessoal, fins de estudo e composição de portfólio profissional.

Sistema ERP corporativo completo para pequenas e médias empresas, integrando **API RESTful de Alta Performance (FastAPI)**, **Banco de Dados Relacional Multi-Schema (PostgreSQL)**, **Arquitetura de Segurança de Nível Corporativo (JWT + RBAC + Rate Limit + Audit)** e **Pipelines ETL/ELT e Data Warehouse (Apache Airflow 3.3)**.

---

## 📌 Visão Geral da Arquitetura

```
               +-------------------------------------------------------+
               |                  APLICAÇÃO / USUÁRIO                   |
               +-------------------------------------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |          API RESTFUL EM FASTAPI (Porta 8000)          |
               |  - Autenticação JWT (OAuth2) & Bcrypt                  |
               |  - Controle de Acesso por Setor (RBAC)                |
               |  - Slowapi Rate Limiting & OWASP Headers              |
               |  - Trilha de Auditoria (seguranca.audit_logs)         |
               +-------------------------------------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |          POSTGRESQL 16 - SCHEMAS OPERACIONAIS         |
               |                                                       |
               |  📁 seguranca  : usuarios, audit_logs                 |
               |  📁 vendas     : clientes, produtos, pedidos, itens   |
               |  📁 financeiro : contas, categorias, lancamentos...   |
               |  📁 juridico   : contratos, aditivos, processos...    |
               |  📁 rh         : departamentos, funcionarios...       |
               |  📁 atendimento: clientes, tickets, interacoes...     |
               |  📁 infra      : equipamentos, servidores, licencas   |
               +-------------------------------------------------------+
                                           |
                                           v (Pipelines ETL/ELT)
               +-------------------------------------------------------+
               |           APACHE AIRFLOW 3.3 (Porta 8080)             |
               |  - 5 DAGs Analíticas Automatizadas em Python          |
               +-------------------------------------------------------+
                                           |
                                           v
               +-------------------------------------------------------+
               |          POSTGRESQL 16 - DATA WAREHOUSE               |
               |  📁 dw         : fato_vendas_mensal,                  |
               |                  fato_fluxo_caixa_mensal,             |
               |                  fato_rh_metricas_departamento,       |
               |                  fato_atendimento_kpis,               |
               |                  fato_infra_juridico_custos,          |
               |                  dim_desempenho_produtos              |
               +-------------------------------------------------------+
```

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12
- **Framework Web**: FastAPI (com Pydantic v2 & Uvicorn)
- **Banco de Dados**: PostgreSQL 16 (Containerizado via Docker)
- **ORM & Conexão**: SQLAlchemy & Psycopg2
- **Orquestrador de Dados**: Apache Airflow 3.3.0 (com CeleryExecutor & Redis)
- **Segurança**: PyJWT, Passlib (Bcrypt), Slowapi (Rate Limit)

---

## 🔒 Arquitetura de Segurança

1. **Autenticação JWT (`/auth/login`)**: Geração de tokens OAuth2 Bearer com validade de 12 horas e senhas criptografadas em `Bcrypt`.
2. **Controle de Acesso por Função (RBAC)**: Restrição de rotas por setor. Ex: Usuários com papel `VENDAS` só acessam `/vendas/*`. Papel `ADMIN` possui acesso irrestrito.
3. **Trilha de Auditoria (`seguranca.audit_logs`)**: Registro automático de eventos de escrita (`POST`), logins e alterações com e-mail, método, IP e timestamp.
4. **Rate Limiting**: Proteção global de 100 requisições/minuto por IP contra força bruta.
5. **Cabeçalhos OWASP**: Injeção de `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection` e `Strict-Transport-Security`.

---

## 🔑 Credenciais Fictícias de Teste

| Setor / Papel | E-mail de Usuário | Senha Padrão | Permissões de Acesso |
|---|---|---|---|
| **ADMIN** | `admin@empresa-exemplo.com.br` | `admin123` | Acesso Total + Logs de Auditoria |
| **VENDAS** | `vendedor@empresa-exemplo.com.br` | `vendas123` | `/vendas/*` |
| **FINANCEIRO** | `financeiro@empresa-exemplo.com.br` | `fin123` | `/financeiro/*` |
| **JURÍDICO** | `juridico@empresa-exemplo.com.br` | `jur123` | `/juridico/*` |
| **RH** | `rh@empresa-exemplo.com.br` | `rh123` | `/rh/*` |
| **ATENDIMENTO** | `atendimento@empresa-exemplo.com.br` | `atend123` | `/atendimento/*` |
| **INFRA** | `infra@empresa-exemplo.com.br` | `infra123` | `/infra/*` |

---

## 📊 Data Warehouse (Schema `dw`) & DAGs no Airflow

O Apache Airflow executa 5 pipelines ETL para consolidar os dados brutos operacionais e alimentar as tabelas analíticas no schema `dw`:

| DAG no Airflow | Tabela Analítica Gerada | Métricas & KPIs Calculados |
|---|---|---|
| `dag_dw_vendas_analytics` | `dw.fato_vendas_mensal`<br>`dw.dim_desempenho_produtos` | Faturamento mensal, ticket médio, pedidos por status e ranking de produtos mais vendidos. |
| `dag_dw_financeiro_analytics` | `dw.fato_fluxo_caixa_mensal`<br>`dw.kpi_saude_financeira` | Receitas vs Despesas por mês, resultado líquido (lucro/prejuízo) e percentual de adimplência. |
| `dag_dw_rh_analytics` | `dw.fato_rh_metricas_departamento` | Headcount por departamento, custo mensal total da folha salarial, salário médio e uso de orçamento. |
| `dag_dw_atendimento_analytics` | `dw.fato_atendimento_kpis` | Taxa de resolução de chamados (%), pontuação média de satisfação (CSAT 1-5) e tickets por prioridade. |
| `dag_dw_infra_juridico_analytics` | `dw.fato_infra_juridico_custos` | Custo de manutenção de TI, licenças anuais de software, valor de contratos vigentes e passivos judiciais. |

---

## 📂 Estrutura do Projeto

```
.
├── app/                        # Código-fonte da API em FastAPI
│   ├── models/                 # Modelos SQLAlchemy organizados por Schema do Postgres
│   ├── schemas/                # Schemas Pydantic para validação de entrada/saída
│   ├── routers/                # Endpoints RESTful por setor (vendas, rh, fin, etc.)
│   ├── auth.py                 # Módulo de Autenticação JWT, Bcrypt e RBAC
│   ├── audit.py                # Módulo de gravação da Trilha de Auditoria
│   ├── database.py             # Configuração da engine e sessão SQLAlchemy
│   ├── seed.py                 # Script de criação de Schemas e Carga Inicial (212 registros)
│   └── main.py                 # Entrypoint da API FastAPI com Middlewares de Segurança
├── data/                       # 25 Arquivos JSON com dados fictícios anonimizados
├── airflow/                    # Ambiente Docker do Apache Airflow 3.3
│   ├── docker-compose.yaml     # Cluster Airflow (Webserver, Scheduler, Worker, Redis, Postgres)
│   └── dags/                   # DAGs em Python para ETL do Data Warehouse (dw)
├── test_api.py                 # Suíte de testes automatizados da API REST (Auth, RBAC, Headers)
├── test_dags_dw.py             # Script de execução e verificação do Data Warehouse (dw)
└── verify_schemas.py           # Script de verificação da estrutura de Schemas do PostgreSQL
```

---

## 🚀 Como Executar o Projeto Completo

### 1. Iniciar o Banco de Dados PostgreSQL Operacional
```bash
docker compose up -d
```

### 2. Iniciar o Cluster do Apache Airflow
```bash
cd airflow
docker compose up -d
cd ..
```

### 3. Recriar Schemas e Popular Dados Operacionais
```bash
PYTHONPATH=. ./venv/bin/python app/seed.py
```

### 4. Executar as Pipelines ETL do Data Warehouse (`dw`)
```bash
PYTHONPATH=. ./venv/bin/python test_dags_dw.py
```

### 5. Executar os Testes Automatizados da API
```bash
PYTHONPATH=. ./venv/bin/python test_api.py
```

### 6. Iniciar o Servidor da API FastAPI
```bash
PYTHONPATH=. ./venv/bin/uvicorn app.main:app --reload --port 8000
```

---

## 🌐 Endereços dos Serviços na Web

- **Documentação Interativa da API (Swagger UI)**:
  👉 **[http://localhost:8000/docs](http://localhost:8000/docs)** *(com suporte a Login via botão Authorize)*
- **Painel do Apache Airflow Web UI**:
  👉 **[http://localhost:8080](http://localhost:8080)** *(Usuário: `airflow` | Senha: `airflow`)*
