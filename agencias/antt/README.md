# ANTT — dados organizados

Gerado por `pipeline/organizar.py` a partir de `data/` (fonte de trabalho). Não edite aqui: rode `python3 pipeline/05_indexar.py && python3 pipeline/organizar.py antt`.

- `reunioes/<ano>/<tipo>/<data>_<numero>_<video_id>/` — `transcricao.json` (legenda com tempos), `leitura.md`, `analise.json` (itens, votos, justificativas), `meta.json` (link do vídeo). Tipos: diretoria, audiencia, participativa, workshop, romeiros.
- `diretores/<nome>/` — `perfil.md`, `perfil_<tema>.md`, `votos.csv` (com link no minuto), `mandato.md`, `falas_audiencias.md`.
- `temas/<tema>.md` — itens por tema, todos os diretores.
- `exportacoes/` — `votos_diretores.xlsx` (planilha: resumo por diretor, diretor × tema, todos os votos com link no minuto, divergências, falas em eventos, mandatos, vacâncias), CSV (reuniões, itens, votos, falas em audiências), `trechos.jsonl.gz` (fala literal com link e minuto), `regulacao.db.gz` (SQLite compactado; descompacte com gunzip, ou regenere com `python3 pipeline/05_indexar.py`).
- `inventario.jsonl`, `COBERTURA.md`, `sem_transcricao.md` (o que NÃO temos e por quê), `mandatos.json`.
