# ANTT — dados organizados

Gerado por `pipeline/organizar.py` a partir de `data/` (fonte de trabalho). Não edite aqui: rode `python3 pipeline/05_indexar.py && python3 pipeline/organizar.py antt`.

- `reunioes/<ano>/<tipo>/<data>_<numero>_<video_id>/` — `transcricao.json` (legenda com tempos), `leitura.md`, `analise.json` (itens, votos, justificativas), `meta.json` (link do vídeo). Tipos: diretoria, audiencia, participativa, workshop, romeiros.
- `diretores/<nome>/` — `perfil.md`, `perfil_<tema>.md`, `votos.csv` (com link no minuto), `mandato.md`, `falas_audiencias.md`.
- `temas/<tema>.md` — itens por tema, todos os diretores.
- `exportacoes/` — CSV (reuniões, itens, votos, falas em audiências), `trechos.jsonl.gz` (fala literal com link e minuto), `regulacao.db` (SQLite com busca).
- `inventario.jsonl`, `COBERTURA.md`, `sem_transcricao.md` (o que NÃO temos e por quê), `mandatos.json`.
