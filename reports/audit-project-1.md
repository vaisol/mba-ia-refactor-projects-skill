# Auditoria de Código: code-smells-project

## 1. Resumo Executivo
- **Stack Detectada**: Python / Flask
- **Arquitetura Atual**: Monolítica com lógica misturada em models/controllers
- **Total de Problemas**: 6 identificados
- **Severidade**: 
  - CRITICAL: 2
  - HIGH: 2
  - MEDIUM: 1
  - LOW: 1

## 2. Detalhamento dos Achados

| ID | Severidade | Anti-Pattern | Localização | Descrição |
|----|------------|--------------|-------------|-----------|
| 001 | 🔴 CRITICAL | SQL Injection | `models.py:22,38,52,118,138,206,214,242` | Uso de concatenação de strings para montar queries SQL. |
| 002 | 🔴 CRITICAL | Admin Backdoor | `app.py:61` | Endpoint `/admin/query` permite execução de SQL arbitrário vindo do usuário. |
| 003 | 🟠 HIGH | Hardcoded Secrets | `app.py:8` | `SECRET_KEY` definida diretamente no código. |
| 004 | 🟠 HIGH | Sensitive Data Exposure | `app.py:168` | Endpoint `/health` expõe a `SECRET_KEY` e o caminho do banco. |
| 005 | 🟡 MEDIUM | N+1 Query Problem | `models.py:158,187` | Queries de itens de pedido dentro de loop de pedidos. |
| 006 | 🟢 LOW | Print Debugging | Vários arquivos | Uso de `print()` em vez de logging estruturado. |

## 3. Exemplos de Código (Antes)

### [001] - SQL Injection
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
```

### [002] - Admin Backdoor
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    dados = request.get_json()
    query = dados.get("sql", "")
    cursor.execute(query) # EXTREMAMENTE PERIGOSO
```

## 4. Plano de Refatoração Proposto
- [x] Remover endpoint de backdoor SQL.
- [x] Migrar para Parameterized Queries em todas as funções de model.
- [x] Mover segredos para variáveis de ambiente (simulado via config).
- [x] Extrair lógica de negócio para Services (E-commerce Business Logic).
- [x] Implementar Joins para resolver N+1 nas listagens de pedidos.
- [x] Organizar em pastas `models/`, `controllers/`, `services/`, `config/`.

---
*Este relatório foi gerado automaticamente pela RefactorArch Skill.*
