---
name: analise-lote
description: Analisa em lote as reuniões de diretoria que já têm texto mas ainda não têm .analise.json (qualquer agência; prioridade ANEEL) — fila, workflow de analistas em paralelo, validação, indexação e conferência cega por lote, com retomada. Use quando o Mac mandar transcrições novas ou a completude mostrar «texto» > «analisadas».
---
# Análise em lote

1. **Fila**: `bash pipeline/ag.sh <ag> python3 pipeline/03_preparar.py` (gera `data/<ag>/analise/<id>.md`). Pendentes = `.md` de reunião de diretoria (não duplicata, ≥2018, sem «TESTE» no título) sem `.analise.json`. Ordene da mais recente para a mais antiga.
2. **Lote-piloto de 60** → confira custo, % válido e dúvidas antes de soltar o resto. Depois lotes de 100–150.
3. **Workflow** (o usuário precisa ter aprovado a escala): um agente `analista-reuniao` por reunião, `parallel`, schema `{arquivo, itens, votos, valido, duvidas}`. Script modelo: o último `analise-lote-aneel` em `workflows/scripts/`. Retome com `resumeFromRunId` se cair.
4. **Depois de cada lote**: `bash pipeline/ag.sh <ag> python3 pipeline/validar.py` em tudo · `bash pipeline/ag.sh <ag> python3 pipeline/05_indexar.py` · `python3 pipeline/completude.py`.
5. **Conferência cega**: skill `auditoria`/agente `conferente-cego`. ANEEL/ANP: 30 itens por lote (skill qualidade-maxima); demais: 20.
6. **Commit** só dos `.analise.json` e do `COMPLETUDE.md`; banco grande fica fora do git (ANEEL > 100 MB).
Registrar em `docs/CONTINUAR.md`: lote, nº de reuniões, itens, votos, % válido, taxa da conferência.
