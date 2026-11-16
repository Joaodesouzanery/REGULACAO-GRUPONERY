# Agências

Cada pasta é a vitrine de uma agência: reuniões por ano, diretores, temas, mandatos, exportações (planilha de votos, CSV) e qualidade. Gerado por `python3 pipeline/organizar.py <ag>` (via `bash pipeline/ag.sh <ag> …`).

| Agência | Setor | Reuniões de diretoria analisadas | Itens · votos | Período | Diretoria hoje (titulares + vagas) | Transparência | Pasta |
|---|---|---|---|---|---|---|---|
| **ANTT** | Transportes terrestres | 283 | 2.382 · 9.398 | 2019-03-12 a 2026-11-09 | 4 + 1 | 9/16 | [`agencias/antt/`](antt/) |
| **ANTAQ** | Portos e navegação | 113 | 5.190 · 16.425 | 2018-01-25 a 2026-11-13 | 4 + 1 | 10/16 | [`agencias/antaq/`](antaq/) |
| **ANM** | Mineração | 130 | 3.619 · 16.245 | 2019-02-19 a 2026-11-04 | 3 + 2 | 10/16 | [`agencias/anm/`](anm/) |
| **ANEEL** | Energia elétrica | 71 | 520 · 1.976 | 2025-09-03 a 2026-10-28 | 4 + 1 | 13/16 | [`agencias/aneel/`](aneel/) |
| **ANP** | Petróleo e gás | coleta iniciando | — | — | 3 + 2 | — | em preparação (`data/anp/`) |
| **ANA** | Águas e saneamento | coleta iniciando | — | — | 3 + 2 | — | em preparação (`data/ana/`) |
| **ANAC** | Aviação civil | coleta iniciando | — | — | 3 + 2 | — | em preparação (`data/anac/`) |

Outros quadros: [vacância das 12 agências](../docs/vacancia_12_agencias.md) · [transparência](../docs/transparencia_agencias.md) · [completude](../COMPLETUDE.md).

ANEEL: as cópias de transcrição e o banco compactado não vão ao GitHub (tamanho); ficam em `data/aneel/` e se reconstroem com `05_indexar.py`.
