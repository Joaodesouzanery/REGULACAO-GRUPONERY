---
name: checagem-mensal
description: Checagem do dia 1 de cada mês — diretoria e superintendentes de cada agência mudaram? (nomeações, reconduções, renúncias, substitutos, vagas). Atualiza mandatos/vacâncias/bios/superintendentes e regenera o quadro da diretoria. Use quando o usuário colar o texto de docs/checagem_mensal.md ou pedir «checagem mensal».
---
1. `python3 pipeline/checagem_mensal.py` → pendências (vota e não está em mandatos, vence em 90 dias, vagas, faltas de minibio/foto/formação).
2. Pesquisa do mês por agência (WebSearch + curl gov.br): Agência Senado/CI (sabatinas), DOU (nomeações, convocações de substitutos, portarias de superintendentes), Agência iNFRA. Subagentes `pesquisador-mandatos` e `pesquisador-dirigentes` em paralelo.
3. **Dirigente novo ou que saiu:** rode `python3 pipeline/dirigentes.py faltas`; para cada pessoa nova ou sem perfil, acione o subagente `pesquisador-dirigentes` (foto, formação, minibio, mandato); quem saiu vira `status: ex-dirigente` (skill `perfis-dirigentes`); depois `python3 pipeline/dirigentes.py gerar`.
4. Atualize `mandatos.json`, `vacancias.json`, `bios.json`, `superintendentes.json` (com fonte e `verificado_em`); rode `vacancias.py <ag>` e `relatorio_diretoria.py <ag>`.
5. Resumo ao usuário: o que mudou (com fonte), o que segue em aberto, o PDF da diretoria atualizado. Commit e push.
