---
name: boletim-mensal
description: Gera o boletim mensal de uma agência (produto premium à parte) — mês em números, decisões por tema, divergências/vistas, quem relatou, empresas em pauta, diretoria (vagas, mandatos), eventos, o que esperar e cobertura. Use quando pedir «boletim de outubro da ANTT» ou no lembrete do dia 25.
---
1. Garanta que o mês está completo na base: `python3 pipeline/cobertura_resposta.py <ag> - - AAAA` (reuniões do mês sem texto aparecem na última página; se faltar legenda, rode a coleta no Mac antes).
2. `python3 pipeline/05_indexar.py` (ou `bash pipeline/ag.sh <ag> 05_indexar`) e depois `python3 pipeline/boletim.py <ag> AAAA-MM`.
3. Revise: `auditor-respostas` (números e trechos contra a base) e `revisor-visual` (screenshots; < 1 MB).
4. «O que esperar» é inferência: mantenha o rótulo. Legenda automática pode errar nomes e valores.
5. Saída em `agencias/<ag>/boletins/`; se for para cliente, copie para `clientes/` (fora do git).
