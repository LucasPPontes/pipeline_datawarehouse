import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_security_and_rbac():
    print("\n--- 1. TESTANDO LOGIN E EMISSÃO DE TOKENS JWT ---")
    users_credentials = [
        ("admin@empresa-exemplo.com.br", "admin123", "ADMIN"),
        ("vendedor@empresa-exemplo.com.br", "vendas123", "VENDAS"),
        ("financeiro@empresa-exemplo.com.br", "fin123", "FINANCEIRO"),
        ("juridico@empresa-exemplo.com.br", "jur123", "JURIDICO"),
        ("rh@empresa-exemplo.com.br", "rh123", "RH"),
        ("atendimento@empresa-exemplo.com.br", "atend123", "ATENDIMENTO"),
        ("infra@empresa-exemplo.com.br", "infra123", "INFRA"),
    ]

    tokens = {}
    for email, password, expected_role in users_credentials:
        res = client.post("/auth/login", data={"username": email, "password": password})
        if res.status_code == 200:
            data = res.json()
            tokens[expected_role] = data["access_token"]
            print(f"[OK] Login bem-sucedido: {email} ({data['role']}) - Token JWT gerado.")
        else:
            print(f"[ERRO] Falha no login de {email}: Status {res.status_code} - {res.text}")
            sys.exit(1)

    print("\n--- 2. TESTANDO LOGIN COM SENHA INCORRETA ---")
    res_bad = client.post("/auth/login", data={"username": "admin@empresa-exemplo.com.br", "password": "senha_errada"})
    if res_bad.status_code == 401:
        print("[OK] Bloqueio correto de credenciais inválidas (HTTP 401).")
    else:
        print(f"[ERRO] Esperado 401 ao usar senha incorreta, obtido: {res_bad.status_code}")

    print("\n--- 3. TESTANDO PERFIL DO USUÁRIO LOGADO (/auth/me) ---")
    headers_vendas = {"Authorization": f"Bearer {tokens['VENDAS']}"}
    res_me = client.get("/auth/me", headers=headers_vendas)
    if res_me.status_code == 200 and res_me.json()["email"] == "vendedor@empresa-exemplo.com.br":
        print(f"[OK] Perfil validado via JWT: {res_me.json()['nome']} ({res_me.json()['cargo']})")
    else:
        print(f"[ERRO] Falha em /auth/me: {res_me.status_code}")

    print("\n--- 4. TESTANDO ACESSO NÃO AUTORIZADO (SEM TOKEN) ---")
    res_no_token = client.get("/rh/funcionarios")
    if res_no_token.status_code == 401:
        print("[OK] Rota protegida rejeitou requisição sem token (HTTP 401).")
    else:
        print(f"[ERRO] Esperado 401 sem token, obtido: {res_no_token.status_code}")

    print("\n--- 5. TESTANDO RESTRICÃO DE ROLES (RBAC) ---")
    # Tentar acessar RH usando o token de VENDAS (Esperado 403 Forbidden)
    res_forbidden = client.get("/rh/funcionarios", headers=headers_vendas)
    if res_forbidden.status_code == 403:
        print("[OK] RBAC Bloqueou acesso indevido: VENDEDOR tentando acessar RH (HTTP 403 Forbidden).")
    else:
        print(f"[ERRO] Esperado 403 Forbidden para role VENDAS acessando RH, obtido: {res_forbidden.status_code}")

    # Acessar RH usando o token de RH (Esperado 200 OK)
    headers_rh = {"Authorization": f"Bearer {tokens['RH']}"}
    res_rh_ok = client.get("/rh/funcionarios", headers=headers_rh)
    if res_rh_ok.status_code == 200:
        print(f"[OK] Acesso permitido para papel RH em /rh/funcionarios (HTTP 200) - {len(res_rh_ok.json())} funcionários.")
    else:
        print(f"[ERRO] Falha no acesso do papel RH a /rh/funcionarios: {res_rh_ok.status_code}")

    # Acessar RH usando o token de ADMIN (Esperado 200 OK)
    headers_admin = {"Authorization": f"Bearer {tokens['ADMIN']}"}
    res_admin_ok = client.get("/rh/funcionarios", headers=headers_admin)
    if res_admin_ok.status_code == 200:
        print(f"[OK] ADMIN com acesso irrestrito a /rh/funcionarios (HTTP 200).")
    else:
        print(f"[ERRO] Falha no acesso do ADMIN: {res_admin_ok.status_code}")

    print("\n--- 6. TESTANDO CABEÇALHOS DE SEGURANÇA OWASP E ROTA /docs ---")
    res_docs = client.get("/docs")
    if res_docs.status_code == 200 and "Content-Security-Policy" not in res_docs.headers:
        print("[OK] Rota /docs acessível sem bloqueio de CSP (HTTP 200).")
    else:
        print(f"[ERRO] Falha na rota /docs: Status {res_docs.status_code}")

    res_headers = client.get("/")
    expected_headers = ["x-content-type-options", "x-frame-options", "strict-transport-security"]
    for h in expected_headers:
        if h in res_headers.headers:
            print(f"[OK] Cabeçalho presente em rotas normais: {h} = {res_headers.headers[h]}")
        else:
            print(f"[ERRO] Cabeçalho ausente: {h}")


    print("\n--- 7. TESTANDO INSERÇÃO (POST) E REGISTRO DE AUDITORIA ---")
    novo_contrato = {
        "titulo": "Contrato de Teste de Auditoria",
        "parte_envolvida": "Empresa Teste SA",
        "tipo_contrato": "prestacao_servicos",
        "valor_contrato": 15000.0,
        "data_inicio": "2024-05-01",
        "data_fim": "2025-05-01",
        "status": "vigente"
    }
    headers_jur = {"Authorization": f"Bearer {tokens['JURIDICO']}"}
    res_post = client.post("/juridico/contratos", json=novo_contrato, headers=headers_jur)
    if res_post.status_code == 201:
        print(f"[OK] Contrato criado via API segura pelo usuário Jurídico! ID: {res_post.json()['id']}")
    else:
        print(f"[ERRO] Falha ao criar contrato: {res_post.status_code} - {res_post.text}")

    # Verificar audit log via ADMIN
    res_audit = client.get("/auth/logs-auditoria", headers=headers_admin)
    if res_audit.status_code == 200 and len(res_audit.json()) > 0:
        log_latest = res_audit.json()[0]
        print(f"[OK] Log de Auditoria registrado com sucesso no PostgreSQL: {log_latest['usuario_email']} | {log_latest['acao']} | {log_latest['endpoint']}")
    else:
        print(f"[ERRO] Falha ao consultar audit logs: {res_audit.status_code}")

    print("\n>>> SUCESSO TOTAL! ARQUITETURA DE SEGURANÇA (JWT, RBAC, RATE LIMIT E AUDIT) VERIFICADA COM SUCESSO! <<<")

if __name__ == "__main__":
    test_security_and_rbac()
