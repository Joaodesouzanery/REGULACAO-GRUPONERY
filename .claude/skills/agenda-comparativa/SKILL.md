---
name: agenda-comparativa
description: Gera o documento 4 (agenda e comparativa — blocos 4, 6 e 7) com pipeline/agenda_comparativa.py: próximas pautas, precedentes e contradições da diretoria nos temas do cliente. Use quando pedir «agenda comparativa», «o que vem na pauta e como já decidiram» ou na rodada mensal.
---
- `python3 pipeline/agenda_comparativa.py clientes/<x>/<pasta>` (lê os temas/processos de `processos.json`).
- Bloco **4** agenda: pautas e calendário oficiais (`pautas.py`, skill `agenda-pauta`); item ainda sem pauta = «previsto», não «pautado».
- Bloco **6** precedentes: `similares.py` / `mapa_tema.py` (skills `casos-semelhantes`, `mapa-assunto`), ≥ 5 por tema com voto por diretor e link `&t=`.
- Bloco **7** contradições: agente `detector-contradicao` (mesmo tema, desfecho oposto em < 24 meses); toda contradição é **inferência** com as duas justificativas lado a lado.
- Pronto quando: cada tema tem agenda + precedentes + (contradições ou «nenhuma encontrada»); falsos positivos conferidos nos 5 primeiros; `auditor-respostas` e cobertura no fim.
