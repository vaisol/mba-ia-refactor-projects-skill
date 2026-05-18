# Audit Report Template

The audit report must follow this structure:

# Auditoria de Código: [Nome do Projeto]

## 1. Resumo Executivo
- **Stack Detectada**: [Linguagem/Framework]
- **Arquitetura Atual**: [Descritivo]
- **Total de Problemas**: [Número]
- **Severidade**: [Contagem por nível]

## 2. Detalhamento dos Achados

| ID | Severidade | Anti-Pattern | Localização | Descrição |
|----|------------|--------------|-------------|-----------|
| 001 | 🔴 CRITICAL | SQL Injection | `models.py:45` | Concatenação de string em query... |
| ... | ... | ... | ... | ... |

## 3. Exemplos de Código (Antes)

### [ID] - [Anti-Pattern]
```[linguagem]
// Snippet do código problemático
```

## 4. Plano de Refatoração Proposto
- [ ] Extração de lógica para camada Service
- [ ] Implementação de Parameterized Queries
- [ ] ...

---
*Este relatório foi gerado automaticamente pela RefactorArch Skill.*
