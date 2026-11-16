---
name: auditoria-falas
description: Confere automaticamente cada trecho literal com link no minuto de um documento (HTML do relatório, boletim, raio-X, agenda, demo) contra a transcrição — existe? o minuto bate (±2 min)? Use antes de toda entrega e depois de mudar textos ou narrativas.
---
# Auditoria de falas
`python3 pipeline/auditar_falas.py <documento.html> --ag <agência>` (o HTML fica ao lado do PDF).
- Saída: contagem `ok · minuto distante · não encontrado` e `<doc>.auditoria_falas.json`.
- **não encontrado** → bloqueia a entrega: corrigir a citação (narrativas.json ou dado da base).
- **minuto distante** (> 2 min) → ajustar o `&t=` para o `t_achado` (no narrativas.json) ou aceitar se for o início do item.
- Registre o resultado no LEIA-ME da entrega («N falas conferidas, X no minuto»).
Complementa o agente `auditor-respostas` (que confere números e afirmações) e a skill `pagina-cheia`.
