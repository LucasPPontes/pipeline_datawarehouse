# 🚀 Mini ERP Backend, Database Schemas & Apache Airflow Data Warehouse

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-3.3-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.2-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-OAuth2_&_RBAC-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

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
               |          API RESTFUL EM FASTAPI (Porta 8001)          |

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

## ⚡ Configuração via Variáveis de Ambiente (`.env`)

A porta da API e demais parâmetros do projeto são totalmente configuráveis através do arquivo [`.env`](file:///home/lucas/%C3%81rea%20de%20trabalho/database/.env) (baseado no modelo [`.env.example`](file:///home/lucas/%C3%81rea%20de%20trabalho/database/.env.example)):

```env
# Alterando a porta da API (Valor padrão: 8001)
API_PORT=8001
```

A variável `API_PORT` é lida de forma transparente por:
- **Docker Compose**: Mapeia `${API_PORT}:${API_PORT}` automaticamente.
- **Python / FastAPI**: Lida pelo `python-dotenv` em [`app/config.py`](file:///home/lucas/%C3%81rea%20de%20trabalho/database/app/config.py).

---

## ⚡ Inicialização Unificada (Um Único Comando)


Todo o ecossistema (PostgreSQL + API FastAPI + Carga Automática de Dados + Cluster Apache Airflow) é inicializado com um único comando:

```bash
docker compose up -d --build
```

---

## 🌐 Endereços dos Serviços na Web

- **Documentação Interativa da API (Swagger UI)**:
  👉 **[http://localhost:8001/docs](http://localhost:8001/docs)** *(com suporte a Login via botão Authorize)*

- **Painel do Apache Airflow Web UI**:
  👉 **[http://localhost:8080](http://localhost:8080)** *(Usuário: `airflow` | Senha: `airflow`)*

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
├── docker-compose.yaml         # Orquestração unificada de todo o ecossistema
├── Dockerfile                  # Containerização da API FastAPI + Carga Automática (seed.py)
├── .gitignore                  # Arquivo de exclusão do Git (ignora venv, env, logs)
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
├── airflow/                    # Diretórios e DAGs do Apache Airflow
│   └── dags/                   # DAGs em Python para ETL do Data Warehouse (dw)
├── test_api.py                 # Suíte de testes automatizados da API REST
├── test_dags_dw.py             # Script de verificação do Data Warehouse (dw)
└── verify_schemas.py           # Script de verificação dos Schemas do PostgreSQL
```
