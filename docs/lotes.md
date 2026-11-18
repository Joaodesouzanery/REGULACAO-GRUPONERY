# Lotes de análise (skill retomar-workflow)

| Data | Agência | Lote | Reuniões | runId | Situação |
|---|---|---|---|---|---|
| 16/11/2026 | ANEEL | piloto | 60 | wf_4f0cc294-270 | concluído: 60/60 válidas, 413 itens, 1.619 votos |
| 16/11/2026 | ANEEL | 2 | 200 (lista em `docs/lotes/wf_73310614-164.json`) | wf_73310614-164 | **pausado** pelo usuário (~50 feitas). Retomar: `Workflow({scriptPath: <script de analise-lote-aneel>, resumeFromRunId: "wf_73310614-164", args: <lista>})`; se a sessão for outra, recalcular a fila (só .md sem .analise.json) |

Script do workflow: `docs/lotes/analise-lote-aneel.js`. Fila completa de 16/11: `docs/lotes/aneel_fila_2026-11-16.json` (727 reuniões, da mais recente para a mais antiga).
| 17/11/2026 | ANEEL | 4 | 150 | wf_6190a8e4-c14 | parcial: parte dos analistas não gravou (modo de planejamento ativado durante o lote) |
| 17/11/2026 | ANEEL | 5 | 150 (`docs/lotes/aneel_lote5.json`, inclui os não gravados do lote 4) | wf_642a8778-40b | rodando |

**Atas da ANEEL:** o site das atas (www2.aneel.gov.br) responde com desafio anti-robô (Cloudflare). Não contornamos. Qualidade da ANEEL melhora pelas regras de proclamação no prompt (desde o lote 4) e por amostra de atas baixada à mão para conferência.

- 17/11/2026 · lote 5 concluído (150/150 válidas, 875 itens, 3.650 votos). Lote 6 lançado: run wf_4cf76a3b-7e4, task whq63j35e, 150 reuniões (lista em scratchpad lote6.json; retomar com resumeFromRunId).
- 17/11/2026 · lote 6 concluído (150/150, 667 itens, 2.801 votos). Lote 7 lançado: run wf_5be5043c-0da, task wgkzm4ao7, 150 das 210 restantes (as 60 finais vão no lote 8).
- 17/11/2026 · lote 7 (Opus) pausado pelo usuário com ~38 prontas. A partir daqui o padrão é **Sonnet** (model: sonnet no script). Lote 8: run wf_8848ffa5-bec, task w0o2am2q3, 150 reuniões; restam 22 para o lote 9.
- 18/11/2026 · corrigido o bug vista/não-votou em amostra.py e 05_indexar.py (votos 2018-2023: 77,2% -> 85,4%; 2024-2026 seguem 87,3%). Reanálise com Opus das reuniões ANEEL 2022-2023 (187 no total): lote 1/2 com 94, run wf_63e9521a-afa, task w6xeb0do1; lote 2/2 com as 93 restantes fica para depois.
- 18/11/2026 · reanálise Opus ANEEL 2022-2023: lote 1/2 concluído (94/94, 539 itens, 2.192 votos). Lote 2/2 lançado: run wf_ef0a9c60-2a0, task w3ucekkpj, 93 reuniões.
- 18/11/2026 · reanálise Opus ANEEL 2022-2023 lote 2/2 (93 reuniões) **pausada a pedido do usuário** (gasto de token), não por limite. 0/93 feitas. Retomar com Workflow resumeFromRunId wf_ef0a9c60-2a0 quando o usuário autorizar.

- 18/11/2026 · ANAC: usuário achou a playlist oficial "Reuniões da Diretoria Colegiada" (850 vídeos) no canal @OficialANAC — nossa coleta só tinha 11. Passar o comando `coletar_tudo_e_enviar.sh anac @OficialANAC --total` no Mac para recoletar com playlists. NÃO lançar análise até combinar o tamanho real pós-coleta. ANA (163 vs 158) está ok, diferença normal.
- 18/11/2026 · ARTESP: usuário pediu para abrir como agência nova (contato com Metrô-SP). Pesquisa do canal/diretoria/mandatos em andamento (agente a9f6143682d51a24e).
