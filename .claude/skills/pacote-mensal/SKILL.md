---
name: pacote-mensal
description: Gera o pacote mensal completo de um cliente (1 relatório da empresa, 2 boletim, 3 raio-X, 4 agenda comparativa + planilha) com todas as checagens (densidade, falas, auditor, guardião) e copia para entrega/. Use todo mês por cliente ou quando pedirem «o pacote do cliente X».
---
# Pacote mensal
`bash pipeline/pacote_mensal.sh clientes/<x>/<pasta> AAAA-MM`
O script: reindexa a agência → gera os 4 PDFs → roda `auditar_falas.py` em cada HTML → copia para `entrega/` com os nomes padrão → imprime os avisos de densidade/estouro.
Depois, no chat: agente `auditor-respostas` (afirmações e números), `guardiao-dados-cliente`, `revisor-visual` (screenshots) e skill `conformidade-entrega`. Só envie com zero «não encontrado» e zero «estouro».


## Etapa obrigatória antes de enviar (nov/2026)
Marca perguntada ao usuário (skill marca-relatorio) e conferência tripla: `auditar_falas.py`, agente `auditor-respostas` e agente `conferente-final` (regras na skill relatorio-escritorio). Corrigir no gerador e gerar de novo.
