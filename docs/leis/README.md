# Base legal (leis e regimentos) — busca por FTS5

- Textos: `docs/leis/<id>.md` (leis) e `docs/leis/regimentos/<ag>.md` (regimentos internos). Vão para o git.
- Índice: `python3 pipeline/indexar_leis.py` → `data/leis.db` (gerado, fora do git).
- Busca: `python3 pipeline/consulta.py lei "pedido de vista"` (5 melhores: lei, artigo, trecho, URL).
- Skill: `.claude/skills/base-legal/SKILL.md`.

## Situação em 15/11/2026: textos AINDA NÃO BAIXADOS

Na nuvem do chat, o Planalto responde `302 → gov.br/planalto` (bloqueio BigIP de IP de nuvem, como o YouTube).
Os sites de legislação das agências também ficaram fora do alcance (proxy recusou `anttlegis.antt.gov.br`,
`anmlegis.datalegis.net`, `sophia.antaq.gov.br`, `leis.org`). **Rodar no Mac:**

```
python3 pipeline/baixar_leis.py      # baixa e converte as 13 leis → docs/leis/*.md
python3 pipeline/indexar_leis.py
git add docs/leis && git commit -m "base legal: leis compiladas" && git push
```

### Leis (URLs do texto compilado no Planalto, em `pipeline/baixar_leis.py`)

| id | norma | URL provável |
|---|---|---|
| lei-13848-2019 | Lei 13.848/2019 (agências reguladoras) | https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13848.htm |
| lei-9784-1999 | Lei 9.784/1999 (processo administrativo) | https://www.planalto.gov.br/ccivil_03/leis/l9784.htm |
| dl-4657-1942-lindb | DL 4.657/1942 (LINDB) | https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm |
| lei-9427-1996 | Lei 9.427/1996 (ANEEL) | https://www.planalto.gov.br/ccivil_03/leis/l9427compilada.htm |
| lei-9478-1997 | Lei 9.478/1997 (ANP) | https://www.planalto.gov.br/ccivil_03/leis/l9478.htm |
| lei-10233-2001 | Lei 10.233/2001 (ANTT/ANTAQ) | https://www.planalto.gov.br/ccivil_03/leis/leis_2001/l10233.htm |
| lei-12815-2013 | Lei 12.815/2013 (portos) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12815.htm |
| lei-13575-2017 | Lei 13.575/2017 (ANM) | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13575.htm |
| lei-13709-2018-lgpd | Lei 13.709/2018 (LGPD) | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm |
| lei-12527-2011-lai | Lei 12.527/2011 (LAI) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm |
| lei-12846-2013 | Lei 12.846/2013 (anticorrupção) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12846.htm |
| lei-12813-2013 | Lei 12.813/2013 (conflito de interesses) | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12813.htm |
| lei-9986-2000 | Lei 9.986/2000 (RH das agências) | https://www.planalto.gov.br/ccivil_03/leis/l9986.htm |

Se algum arquivo do Planalto tiver versão «compilado/compilada» com outro nome, o script avisa «sem Art. 1» — corrigir a URL no dicionário `LEIS`.

### Regimentos internos (faltam; baixar no Mac e gravar em `docs/leis/regimentos/<ag>.md`)

Formato: `# Regimento Interno da <AG> — <resolução>`, linha `URL: <fonte>`, data da coleta, aviso; texto com «Art. N». PDF → `pdftotext -layout`.

| ag | ato vigente identificado | onde está |
|---|---|---|
| antt | Resolução ANTT nº 5.976/2022 (Regimento Interno) | página gov.br https://www.gov.br/antt/pt-br/acesso-a-informacao/institucional/base-juridica-da-estrutura-organizacional-e-das-competencias-1/regimento-interno redireciona para https://anttlegis.antt.gov.br/action/ActionDatalegis.php?acao=detalharAto&tipo=RES&numeroAto=00005976&seqAto=000&valorAno=2022&orgao=DG/ANTT/MI&codTipo=&desItem=&desItemFim=&cod_menu=5408&cod_modulo=161&pesquisa=true (conferir se há alterações posteriores) |
| anm | Resolução ANM nº 211, de 9/7/2025, alterada pela Resolução ANM nº 236, de 1º/4/2026 | https://www.gov.br/anm/pt-br/acesso-a-informacao/institucional/base-juridica-da-estrutura-organizacional-e-das-competencias/regimento-interno (links levam a anmlegis.datalegis.net) |
| antaq | Regimento Interno (acervo Sophia, registro 37131) | https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/base-juridica-1 → https://sophia.antaq.gov.br/Terminal/acervo/detalhe/37131 |
| aneel | Portaria ANEEL nº 6.980, de 16/6/2025 (aprova o Regimento Interno) | https://www.gov.br/aneel/pt-br/centrais-de-conteudos/normas-internas-de-organizacao (link externo para leis.org/aneel) |
