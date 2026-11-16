---
name: lacunas-agencias
description: Fecha as lacunas recorrentes de todas as agências — calendário/pautas, fotos e minibios de superintendentes, mandatos ainda não confirmados no DOU e conferência cega pendente (ANEEL) — usando os agentes certos e atualizando COMPLETUDE.md. Use quando a completude mostrar buracos ou na checagem mensal.
---
# Lacunas das agências
Rode `python3 pipeline/completude.py` e trate cada coluna com zero ou incompleta:
| Lacuna | Quem resolve | Pronto quando |
|---|---|---|
| Agenda «0 / — / 0» | skill `calendario-agencias` + agente `pesquisador-calendario` | calendário do semestre com fonte |
| Superintendentes sem foto | agente `pesquisador-dirigentes` (skill `fotos-oficiais`; foto ≥600 px de gov.br/Flickr oficial) | n/foto iguais na completude |
| Mandatos sem confirmação | agente `pesquisador-mandatos` (DOU/Senado; campo `nomeacao_dou`, `confirmado: sim`) | «confirmados» = «n» |
| Conferência cega 0 (ANEEL) | agente `conferente-cego` + `pipeline/amostra.py` (30 itens; skill `qualidade-maxima`) | taxa registrada em `data/aneel/qualidade/` |
| Controle por cadeira | skill `controle-diretoria` | `cadeiras.json` existe |
Se o gov.br/DOU não abrir da nuvem, liste os links para o usuário abrir no Mac. Nunca preencher sem fonte.
