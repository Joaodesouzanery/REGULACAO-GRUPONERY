# Lotes de análise (skill retomar-workflow)

| Data | Agência | Lote | Reuniões | runId | Situação |
|---|---|---|---|---|---|
| 16/11/2026 | ANEEL | piloto | 60 | wf_4f0cc294-270 | concluído: 60/60 válidas, 413 itens, 1.619 votos |
| 16/11/2026 | ANEEL | 2 | 200 (lista em `docs/lotes/wf_73310614-164.json`) | wf_73310614-164 | **pausado** pelo usuário (~50 feitas). Retomar: `Workflow({scriptPath: <script de analise-lote-aneel>, resumeFromRunId: "wf_73310614-164", args: <lista>})`; se a sessão for outra, recalcular a fila (só .md sem .analise.json) |

Script do workflow: `docs/lotes/analise-lote-aneel.js`. Fila completa de 16/11: `docs/lotes/aneel_fila_2026-11-16.json` (727 reuniões, da mais recente para a mais antiga).
