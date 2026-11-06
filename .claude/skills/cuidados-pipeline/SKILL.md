---
name: cuidados-pipeline
description: Checklist obrigatório antes de qualquer commit/push neste repositório (regulação/diretores). Use sempre que rodar organizar.py, 05_indexar.py, análises por subagente, conferências, ou ao mexer em scripts que apagam/recriam pastas. Evita perdas como a de agencias/antt/qualidade/ (apagada por organizar.py em nov/2026).
---
# Cuidados com o pipeline (ler antes de commitar)

Erros já ocorridos: `organizar.py` fazia `rmtree(agencias/antt)` e apagou o relatório de qualidade; mandato estimado errado (Felipe Queiroz 2028 → 2027); convenção de «vista» diferente entre análise e conferência; Mac em branch antigo.

1. **Antes de rodar scripts que recriam pastas** (`organizar.py`): confira `PRESERVAR` no script. Pasta feita à mão (qualidade/, notas) NUNCA pode ficar em pasta recriada sem estar em `PRESERVAR`. Script novo que apaga algo: preservar por padrão.
2. **Sempre rode** `python3 pipeline/checar_integridade.py` antes do commit. Se falhar, NÃO commite: restaure (`git checkout -- <arquivo>`) ou explique ao usuário. Contagens subiram legitimamente → `--atualizar`.
3. `git status --short | grep '^ D\|^D'` e `git diff --stat` — leia a lista; apagamento inesperado = parar.
4. **Não versionar** `data/regulacao.db`, `regulacao.db.gz`, `trechos.jsonl.gz` a cada lote (só em marcos): `git checkout -- data/regulacao.db agencias/antt/exportacoes/regulacao.db.gz agencias/antt/exportacoes/trechos.jsonl.gz`.
5. Validação: `validar.py`, `validar_evento.py`; depois `05_indexar.py` → `organizar.py antt` (regera planilha e mandatos).
6. **Conferências cegas**: o subagente nunca abre `*.analise.json`, `amostra_gabarito.json`, `agencias/**`. Convenção de voto única (`amostra.py CAT` = `05_indexar.py categoria`): «voto-vista» conta como acompanha/diverge; «vista» só para quem apenas pediu vista. Relatórios listam discordâncias **por diretor, com RD e item**.
7. **Datas de mandato**: nunca trocar uma data confirmada por estimativa; toda data nova leva fonte (URL) e `confianca`. Estimativa → diga «estimado».
8. **Branch**: o de trabalho está em `docs/CONTINUAR.md`; ao trocar de branch, atualizar `CONTINUAR.md`, `LEVAR_PARA_OUTRA_CONTA.md`, `tarefa_semanal.txt` e avisar o usuário para `git checkout <branch>` no Mac.
9. Dados de cliente (`clientes/`) nunca vão para o GitHub (`.gitignore`).
