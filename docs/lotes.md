# Lotes de análise (skill retomar-workflow)

| Data | Agência | Lote | Reuniões | runId | Situação |
|---|---|---|---|---|---|
| 16/11/2026 | ANEEL | piloto | 60 | wf_4f0cc294-270 | concluído: 60/60 válidas, 413 itens, 1.619 votos |
| 16/11/2026 | ANEEL | 2 | 200 (lista em `docs/lotes/wf_73310614-164.json`) | wf_73310614-164 | **pausado** pelo usuário (~50 feitas). Retomar: `Workflow({scriptPath: <script de analise-lote-aneel>, resumeFromRunId: "wf_73310614-164", args: <lista>})`; se a sessão for outra, recalcular a fila (só .md sem .analise.json) |

Script do workflow: `docs/lotes/analise-lote-aneel.js`. Fila completa de 16/11: `docs/lotes/aneel_fila_2026-11-16.json` (727 reuniões, da mais recente para a mais antiga).
| 17/11/2026 | ANEEL | 4 | 150 | wf_6190a8e4-c14 | parcial: parte dos analistas não gravou (modo de planejamento ativado durante o lote) |
| 17/11/2026 | ANEEL | 5 | 150 (`docs/lotes/aneel_lote5.json`, inclui os não gravados do lote 4) | wf_642a8778-40b | rodando |

**Atas da ANEEL:** o site das atas (www2.aneel.gov.br) responde com desafio anti-robô (Cloudflare). Não contornamos. Qualidade da ANEEL melhora pelas regras de proclamação no prompt (desde o lote 4) e por amostra de atas baixada à mão para conferência.
