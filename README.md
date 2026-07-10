# Desafio Skills — Refatoração Arquitetural Automatizada

Skill `refactor-arch` para OpenCode que analisa, audita e refatora qualquer projeto web para o padrão MVC.

---

## A) Análise Manual

### Projeto 1: code-smells-project (Python/Flask — E-commerce API)

| # | Severidade | Problema | Localização |
|---|-----------|----------|-------------|
| 1 | CRITICAL | SQL Injection via concatenação de strings em todas as queries | `models.py:28,48-49,68,92,110,127-128,140,174,188,220,224,280,291-297` |
| 2 | CRITICAL | Endpoint `/admin/query` executa SQL arbitrário | `app.py:59-78` |
| 3 | CRITICAL | SECRET_KEY hardcoded (`"minha-chave-super-secreta-123"`) | `app.py:7` |
| 4 | CRITICAL | Secret key exposta na resposta do health check | `controllers.py:289` |
| 5 | HIGH | God File: `controllers.py` contém toda lógica de negócio (292 linhas) | `controllers.py:1-292` |
| 6 | HIGH | God File: `models.py` contém todas as operações de banco (314 linhas) | `models.py:1-314` |
| 7 | HIGH | N+1 queries em `get_pedidos_usuario()` e `get_todos_pedidos()` | `models.py:171-233` |
| 8 | MEDIUM | Notificações via `print()` em vez de serviço dedicado | `controllers.py:208-210,248-250` |
| 9 | MEDIUM | Senhas expostas na resposta de `get_todos_usuarios()` | `models.py:79-86` |
| 10 | LOW | `print()` de debug espalhados pelo código | `controllers.py` (vários) |
| 11 | LOW | `except Exception` genérico em todas as rotas | `controllers.py` (vários) |
| 12 | LOW | Construção manual de dicts em vez de `to_dict()` | `models.py` (vários) |

### Projeto 2: ecommerce-api-legacy (Node.js/Express — LMS API)

| # | Severidade | Problema | Localização |
|---|-----------|----------|-------------|
| 1 | CRITICAL | Credenciais hardcoded (DB user/pass, payment key) | `utils.js:2-4` |
| 2 | CRITICAL | `badCrypto()` não é criptografia real (base64 loop) | `utils.js:17-23` |
| 3 | CRITICAL | Checkout aceita número de cartão em plaintext e loga no console | `AppManager.js:33,45` |
| 4 | HIGH | God Object: `AppManager` (init DB + rotas + lógica) | `AppManager.js:4-139` |
| 5 | HIGH | Callback hell: relatório financeiro com 4 níveis de nesting | `AppManager.js:80-128` |
| 6 | HIGH | Estado global mutável (`globalCache`, `totalRevenue`) | `utils.js:9-10` |
| 7 | MEDIUM | Sem validação de input no checkout | `AppManager.js:28-35` |
| 8 | MEDIUM | Registros órfãos ao deletar usuário | `AppManager.js:131-137` |
| 9 | LOW | Dados sensíveis em console.log | `AppManager.js:45` |
| 10 | LOW | Strings mágicas espalhadas pelo código | `AppManager.js` (vários) |

### Projeto 3: task-manager-api (Python/Flask — Task Manager API)

| # | Severidade | Problema | Localização |
|---|-----------|----------|-------------|
| 1 | CRITICAL | Credenciais SMTP hardcoded | `services/notification_service.py:9-10` |
| 2 | CRITICAL | Hash de senha com MD5 (quebrado) | `models/user.py:29,32` |
| 3 | CRITICAL | Hash de senha exposto no `to_dict()` | `models/user.py:21` |
| 4 | HIGH | Token JWT falso (`'fake-jwt-token-' + str(user.id)`) | `routes/user_routes.py:210` |
| 5 | HIGH | Lógica de negócio nas rotas, sem controllers | `routes/task_routes.py`, `routes/user_routes.py` |
| 6 | HIGH | Lógica de overdue duplicada 3x | `routes/task_routes.py:30-39`, `routes/report_routes.py:33-43`, `routes/user_routes.py:171-180` |
| 7 | MEDIUM | CRUD de categorias misturado com reports | `routes/report_routes.py:157-223` |
| 8 | MEDIUM | Validação duplicada (rotas vs helpers) | `routes/task_routes.py` vs `utils/helpers.py` |
| 9 | LOW | Imports não utilizados | `app.py:7`, `routes/task_routes.py:7` |
| 10 | LOW | `NotificationService` nunca utilizado | `services/notification_service.py` |
| 11 | LOW | `except:` sem tipo específico | `routes/task_routes.py:62,236` |

---

## B) Construção da Skill

### Estrutura da Skill

A skill foi criada em `.opencode/skills/refactor-arch/` com 6 arquivos:

| Arquivo | Função |
|---------|--------|
| `SKILL.md` | Instrução principal — 3 fases: Análise → Auditoria → Refatoração |
| `project-analysis.md` | Heurísticas para detecção de linguagem, framework, DB e domínio |
| `anti-pattern-catalog.md` | 14 anti-patterns com sinais de detecção e severidade |
| `report-template.md` | Template padronizado do relatório de auditoria |
| `architecture-guidelines.md` | Regras do MVC alvo para Python/Flask e Node.js/Express |
| `refactoring-playbook.md` | 10 padrões de transformação com código antes/depois |

### Decisões de Design

1. **Detecção por heurísticas:** A skill detecta stack lendo `requirements.txt`, `package.json` e padrões de import — nunca assume uma tecnologia específica.

2. **Catálogo com 14 anti-patterns:** Cobertura ampla incluindo SQL Injection, Hardcoded Secrets, God Class, N+1 Queries, Callback Hell, Missing Validation, Global Mutable State, Deprecated APIs, Broken Cryptography, Duplicated Code, Fat Controller, Exposed Sensitive Data, Orphaned Records, Missing Error Handling.

3. **Playbook com 10 transformações:** Cada padrão tem exemplo "antes/depois" em Python e Node.js, tornando a refatoração acionável.

4. **Pausa obrigatória:** A Fase 2 sempre para e pede confirmação antes de qualquer modificação.

5. **Validação na Fase 3:** Instrui o agente a testar boot da aplicação e endpoints após refatoração.

### Como a Skill é Agnóstica

- Não menciona Flask, Express ou qualquer framework no SKILL.md
- As heurísticas de detecção usam sinais genéricos (extensões, imports, dependências)
- O playbook tem exemplos em ambas as stacks
- As guidelines de arquitetura cobrem Python e Node.js separadamente

### Desafios Encontrados

1. **Import paths quebrados:** Projetos anteriores criavam imports como `from src.config import settings` quando `src/` não existia como pacote. Solução: instruir a skill a manter imports relativos à raiz do projeto.

2. **Lógica deletada em vez de movida:** Em refatorações anteriores do ecommerce-api-legacy, toda a lógica de checkout/usuarios/cursos sumiu em vez de ser redistribuída em camadas MVC. Solução: regra explícita no SKILL.md — "NUNCA delete business logic, MOVA para a camada correta".

3. **Projetos parcialmente organizados:** O task-manager-api já tinha models/routes mas faltava controllers. A skill precisava identificar o que melhorar sem reestruturar tudo.

---

## C) Resultados

### Resumo dos Relatórios de Auditoria

| Projeto | Stack | CRITICAL | HIGH | MEDIUM | LOW | Total |
|---------|-------|----------|------|--------|-----|-------|
| code-smells-project | Python/Flask | 4 | 4 | 2 | 3 | **13** | [Relatório](reports/audit-project-1.md) |
| ecommerce-api-legacy | Node.js/Express | 3 | 4 | 2 | 2 | **11** | [Relatório](reports/audit-project-2.md) |
| task-manager-api | Python/Flask | 3 | 3 | 3 | 3 | **12** | [Relatório](reports/audit-project-3.md) |
| **Total** | | **10** | **11** | **7** | **8** | **36** |

### Comparação Antes/Depois

#### code-smells-project

| Antes | Depois |
|-------|--------|
| 4 arquivos flat | 7 diretórios MVC (config/, models/, controllers/, routes/, services/, middlewares/) |
| SQL injection em toda query | Queries parametrizadas com `?` |
| SECRET_KEY hardcoded | Variável de ambiente via `config/settings.py` |
| God files (controllers.py 292 linhas, models.py 314 linhas) | Controllers e models por domínio |
| `print()` como notificação | Serviço de notificação via logging |
| Erro handling genérico | Middleware centralizado de erros |

📄 **Relatório completo:** [reports/audit-project-1.md](reports/audit-project-1.md)

#### ecommerce-api-legacy

| Antes | Depois |
|-------|--------|
| 3 arquivos, 1 God class | 7 módulos MVC (config/, models/, controllers/, routes/, services/, middlewares/) |
| `badCrypto()` (base64 loop) | bcrypt com salt rounds |
| Credenciais hardcoded | Variáveis de ambiente |
| Callback hell (4 níveis) | Async/await com helpers promisificados |
| Card number em plaintext + log | Serviço de pagamento sem exposição |
| Registros órfãos no delete | Cascade delete implementado |

📄 **Relatório completo:** [reports/audit-project-2.md](reports/audit-project-2.md)

#### task-manager-api

| Antes | Depois |
|-------|--------|
| Sem controllers, lógica nas rotas | Controllers dedicados (task, user, category, report) |
| MD5 para senhas | werkzeug.security (pbkdf2) |
| Senhas no `to_dict()` | Senhas removidas do response |
| Overdue duplicado 3x | `is_overdue()` no model, usado em todos os lugares |
| Categorias misturadas com reports | `category_routes.py` separado |
| Erro handling em cada rota | Middleware centralizado |

📄 **Relatório completo:** [reports/audit-project-3.md](reports/audit-project-3.md)

### Checklist de Validação

#### Projeto 1: code-smells-project

- [x] Linguagem detectada: Python
- [x] Framework detectado: Flask 3.1.1
- [x] Domínio: E-commerce API (produtos, pedidos, usuários)
- [x] Arquivos analisados: 4
- [x] >= 5 findings: 13 findings
- [x] Pelo menos 1 CRITICAL/HIGH: 8 (4 CRITICAL + 4 HIGH)
- [x] Estrutura MVC criada
- [x] Config extraída para env vars
- [x] Models com `to_dict()` sem senhas
- [x] Controllers por domínio
- [x] Routes thin (só HTTP)
- [x] Error handling centralizado
- [x] **App inicia sem erros**
- [x] **Todos os endpoints respondem**

#### Projeto 2: ecommerce-api-legacy

- [x] Linguagem detectada: JavaScript (Node.js)
- [x] Framework detectado: Express 4.18.2
- [x] Domínio: LMS API com checkout
- [x] Arquivos analisados: 3
- [x] >= 5 findings: 11 findings
- [x] Pelo menos 1 CRITICAL/HIGH: 7 (3 CRITICAL + 4 HIGH)
- [x] Estrutura MVC criada
- [x] Config extraída para env vars
- [x] Models por entidade (user, course, enrollment, payment, audit)
- [x] Controllers (checkout, financial)
- [x] Async/await substitui callbacks
- [x] bcrypt substitui badCrypto
- [x] **App inicia sem erros**
- [x] **Todos os endpoints respondem**

#### Projeto 3: task-manager-api

- [x] Linguagem detectada: Python
- [x] Framework detectado: Flask 3.0.0
- [x] Domínio: Task Manager API
- [x] Arquivos analisados: 12
- [x] >= 5 findings: 12 findings
- [x] Pelo menos 1 CRITICAL/HIGH: 6 (3 CRITICAL + 3 HIGH)
- [x] Controllers adicionados
- [x] Config extraída para env vars
- [x] MD5 → werkzeug password hashing
- [x] Senhas removidas de responses
- [x] Overdue centralizado no model
- [x] Categorias em routes separadas
- [x] Error handling centralizado
- [x] **App inicia sem erros**
- [x] **Todos os endpoints respondem**

### Logs de Validação

```
=== PROJECT 1: code-smells-project ===
Boot: OK | Health: 200 | Products: 10 | Users: 3

=== PROJECT 2: ecommerce-api-legacy ===
Boot: OK | Financial Report: 200 | Courses: 2

=== PROJECT 3: task-manager-api ===
Boot: OK | Health: 200 | Tasks: 10 | Users: 3 | Categories: 4 | Report: OK
```

---

## D) Como Executar

### Pré-requisitos

- [OpenCode](https://opencode.ai) instalado e configurado
- Python 3.x instalado (para projetos 1 e 3)
- Node.js 18+ instalado (para projeto 2)

### Executar a Skill

```bash
# Projeto 1 — Python/Flask E-commerce
cd code-smells-project
opencode "/refactor-arch"

# Projeto 2 — Node.js/Express LMS
cd ../ecommerce-api-legacy
opencode "/refactor-arch"

# Projeto 3 — Python/Flask Task Manager
cd ../task-manager-api
opencode "/refactor-arch"
```

### Validar Resultado

```bash
# Projeto 1
cd code-smells-project && python3 app.py
# Testar: curl http://localhost:5000/health

# Projeto 2
cd ecommerce-api-legacy && npm start
# Testar: curl http://localhost:3000/api/admin/financial-report

# Projeto 3
cd task-manager-api && python3 seed.py && python3 app.py
# Testar: curl http://localhost:5000/health
```

### Relatórios de Auditoria

Os relatórios completos estão em:

- `reports/audit-project-1.md` — code-smells-project (13 findings)
- `reports/audit-project-2.md` — ecommerce-api-legacy (11 findings)
- `reports/audit-project-3.md` — task-manager-api (12 findings)

---

## Referências

- [OpenCode Skills](https://opencode.ai/docs/skills/) — Documentação oficial de Skills
- [OpenCode Overview](https://opencode.ai/docs/) — Visão geral do OpenCode
