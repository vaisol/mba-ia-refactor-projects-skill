# RefactorArch Skill

Especialista em auditoria e refatoração de código agnóstica de tecnologia, focada em segurança, padrões MVC e princípios SOLID.

## Objetivo
Analisar projetos (Python, Node.js, etc.), detectar anti-patterns, gerar relatórios de auditoria detalhados e realizar refatoração estruturada para o padrão MVC.

---

## 🛠 Fases Sequenciais

### Fase 1 — Análise (Discovery)
1. **Detectar Stack**: Identificar linguagem, frameworks e banco de dados usando `references/analysis.md`.
2. **Mapear Arquitetura**: Avaliar a estrutura atual de arquivos e fluxo de dados.
3. **Resumo**: Imprimir no terminal um resumo da stack detectada e o estado arquitetural.

### Fase 2 — Auditoria (Scan & Report)
1. **Identificar Anti-patterns**: Escanear o código-fonte usando `references/anti_patterns.md`.
2. **Gerar Relatório**: Criar um arquivo `AUDIT_REPORT.md` baseado em `references/report_template.md`.
3. **Classificação**: Categorizar cada item como CRITICAL, HIGH, MEDIUM ou LOW.
4. **Confirmação**: **PAUSAR** e pedir confirmação do usuário antes de prosseguir para a refatoração.

### Fase 3 — Refatoração (MVC Strict)
1. **Executar Playbook**: Aplicar as transformações descritas em `references/refactoring_playbook.md`.
2. **Reestruturar**: Mover o código para as camadas corretas (Model, View, Controller) seguindo `references/architecture_guidelines.md`.
3. **Validar**:
   - Tentar iniciar a aplicação (boot check).
   - Validar endpoints principais se possível.
   - Garantir que não há erros de sintaxe ou dependências quebradas.

---

## 📚 Conhecimento (Referências)
- `references/analysis.md`: Heurísticas de detecção de stack.
- `references/anti_patterns.md`: Catálogo de 10+ anti-patterns e severidades.
- `references/report_template.md`: Template para o relatório de auditoria.
- `references/architecture_guidelines.md`: Regras do MVC alvo.
- `references/refactoring_playbook.md`: Padrões de transformação (Antes/Depois).

---

## 🚀 Como usar
1. Ative a skill: `activate_skill("refactor-arch")`
2. Solicite a análise: "Analise este projeto e gere um relatório de auditoria."
3. Após aprovar o relatório, solicite a refatoração: "Refatore o projeto para o padrão MVC seguindo o relatório."

---
*Mandato: Nunca ignore vulnerabilidades CRITICAL como SQL Injection ou Segredos Hardcoded.*
