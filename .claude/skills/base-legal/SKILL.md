---
name: base-legal
description: Busca e cita a base legal (leis das agências, Lei 13.848, Lei 9.784, LINDB, LGPD, LAI, conflito de interesses, regimentos internos) com pipeline/consulta.py lei. Use quando a pergunta envolver regra de procedimento (pedido de vista, quórum, recondução, mandato, quarentena, sigilo, prazo de processo) ou quando um relatório precisar dizer «o que a lei manda».
---

# Base legal

1. Garanta o índice: `python3 pipeline/indexar_leis.py` (lê `docs/leis/**/*.md` → `data/leis.db`, ~1 s).
   Se disser «0 arquivos», os textos ainda não foram baixados: ver `docs/leis/README.md` (o Planalto só responde no Mac: `python3 pipeline/baixar_leis.py`). Diga isso ao usuário; não cite de memória como se viesse da base.
2. Busque: `python3 pipeline/consulta.py lei "pedido de vista"` — 5 melhores trechos (lei, artigo, trecho, URL). Refaça com sinônimos (ex.: «vista», «recondução», «mandato», «quarentena», «impedimento»).
3. Leia o artigo inteiro antes de citar: `sqlite3 data/leis.db "select texto from leis where lei like '%13.848%' and artigo='Art. 9º'"`.

## Como citar
- Sempre: **norma + artigo (+ § / inciso)**, trecho literal entre «», e a URL oficial (Planalto ou página da agência).
  Ex.: Lei nº 13.848/2019, art. 9º, § 1º: «…» — https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13848.htm
- Diga a data da coleta do texto (cabeçalho do .md) e que é **texto de referência; confira a versão oficial**.
- Dispositivo marcado «(revogado)» não vale: não cite como regra vigente.
- Regimento interno: diga a resolução/portaria que o aprova e se há alteração posterior não incorporada.
- Combine com a evidência das reuniões (resposta-com-evidencia): a lei diz X; na prática, a diretoria fez Y (reunião, item, link no minuto).

## Limites (dizer sempre)
- **Não é aconselhamento jurídico**; é apoio de pesquisa. Interpretação e estratégia processual: advogado.
- A busca é por palavras (FTS5), não semântica: ausência de resultado não prova ausência de regra.
