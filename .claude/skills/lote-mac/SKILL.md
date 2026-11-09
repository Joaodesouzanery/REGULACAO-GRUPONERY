---
name: lote-mac
description: O que fazer quando o Mac do usuário envia um lote novo ao GitHub (legendas da coleta, transcrições Whisper, DOU). Use quando o usuário disser «dei push no Mac», «rodei a coleta», «pode analisar o Whisper», ou quando git pull trouxer transcricoes/ novas.
---
# Lote vindo do Mac

1. `git fetch origin <branch> && git log --oneline HEAD..FETCH_HEAD` — confirme que chegou (se não chegou: peça `git status && git log -3 --oneline && git push` e mostre o erro; comandos em `docs/MAC_COMANDOS.md`). `git pull --no-rebase`.
2. Descubra o que é novo: `git diff --stat HEAD@{1} -- 'data/**/transcricoes/*'` e `transcricoes_whisper.jsonl`.
3. Para cada agência afetada: `03_preparar.py` (via `ag.sh` se não for ANTT) → subagentes `analista-reuniao` (um por reunião nova) → `validar.py` → `05_indexar.py` → `cobertura.py` → `organizar.py <sigla>`.
4. Whisper: marque no relatório/consulta que a fonte é «Whisper (áudio)», não legenda; confira 1–2 itens por amostra (trecho perto do minuto).
5. `python3 pipeline/auditar.py` (base) e `checar_integridade.py`; commit e push (skill `cuidados-pipeline`).
6. Conte ao usuário: reuniões novas, itens, votos, o que ficou sem texto e por quê.
