---
name: triagem-eventos
description: Classifica eventos (audiências, workshops, participativas) por prioridade antes de analisar — alta (audiência/consulta pública, leilão, tarifa, resolução), média, baixa (encerramento de P&D, internacionais, inglês) — com pipeline/triagem_eventos.py. Use quando o Mac trouxer muitos eventos ou antes de mandar analista-evento.
---
# Triagem de eventos
`python3 pipeline/triagem_eventos.py <ag>` → `data/<ag>/eventos_prioridade.json` e resumo (com texto / analisados por prioridade).
- Analise só **alta** com `analista-evento` (depois das reuniões de diretoria); **média** sob demanda; **baixa** fica guardada sem análise.
- Ajuste as regex `ALTA`/`BAIXA` no script quando surgir padrão novo de título e registre aqui.
