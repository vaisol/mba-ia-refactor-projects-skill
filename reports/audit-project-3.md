# Auditoria de Código: task-manager-api

## 1. Resumo Executivo
- **Stack Detectada**: Python / Flask / SQLAlchemy
- **Arquitetura Atual**: Parcialmente organizada, mas com vazamento de lógica de negócio para os Controllers (Routes).
- **Total de Problemas**: 6 identificados
- **Severidade**: 
  - CRITICAL: 0
  - HIGH: 2
  - MEDIUM: 2
  - LOW: 2

## 2. Detalhamento dos Achados

| ID | Severidade | Anti-Pattern | Localização | Descrição |
|----|------------|--------------|-------------|-----------|
| 001 | 🟠 HIGH | Business Logic in Presentation Layer | `task_routes.py:23,98` | Cálculos de tarefas atrasadas e validações complexas dentro das rotas. |
| 002 | 🟠 HIGH | Hardcoded Secrets | `notification_service.py:9,10` | Credenciais de e-mail (usuário e senha) expostas no código. |
| 003 | 🟡 MEDIUM | N+1 Query Problem | `task_routes.py:44,51` | Busca de usuário e categoria individualmente para cada task em uma listagem. |
| 004 | 🟡 MEDIUM | Inconsistent Error Handling | `task_routes.py:73` | Bloco `except` genérico que esconde erros reais e retorna 500 sem contexto. |
| 005 | 🟢 LOW | Code Duplication | Múltiplos arquivos | Lógica de `is_overdue` repetida em `models/task.py` e `routes/task_routes.py`. |
| 006 | 🟢 LOW | Hardcoded Magic Strings | `task_routes.py:112` | Lista de status permitidos duplicada e hardcoded no controller. |

## 3. Exemplos de Código (Antes)

### [001] - Logic in Routes
```python
if t.due_date:
    if t.due_date < datetime.utcnow():
        if t.status != 'done' and t.status != 'cancelled':
            task_data['overdue'] = True
```

### [003] - N+1 Query
```python
for t in tasks:
    user = User.query.get(t.user_id) # Query dentro do loop
```

## 4. Plano de Refatoração Proposto
- [x] Extrair lógica de "Overdue" e validações para uma camada de Service.
- [x] Utilizar `joinedload` do SQLAlchemy para resolver N+1.
- [x] Mover credenciais de e-mail e secret keys para arquivo de config/env.
- [x] Padronizar respostas de erro com um helper centralizado.
- [x] Garantir que o Model contenha apenas definições e comportamentos básicos do domínio.

---
*Este relatório foi gerado automaticamente pela RefactorArch Skill.*
