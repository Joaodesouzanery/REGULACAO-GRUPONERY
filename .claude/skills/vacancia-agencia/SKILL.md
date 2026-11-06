---
name: vacancia-agencia
description: Mantém sempre atualizado o tempo de vacância de diretoria (cadeira titular vaga) de cada agência reguladora — média, mediana, máximo, vagas em aberto e % de dias-cadeira vagos — e o comparativo entre agências. Use quando entrar/sair diretor, mudar mandatos.json/vacancias.json, iniciar nova agência, ou quando o usuário perguntar sobre vacância.
---
# Vacância por agência

Fontes: ANTT em `data/mandatos.json` + `data/vacancias.json`; outras agências em `data/<sigla>/mandatos.json` + `data/<sigla>/vacancias.json` (mesmo formato: `id, cadeira, inicio, fim (null = em aberto), preenchida_por, interinos, confianca, fonte`).

1. **Atualizar vacâncias** quando houver fato novo (fim de mandato, renúncia, posse, convocação de substituto):
   - vaga começa no dia seguinte ao fim do titular (fim legal ou saída efetiva) e termina na véspera da posse/1º voto do novo titular;
   - substituto/interino NÃO encerra a vaga (registrar em `interinos`);
   - vaga sem titular hoje: `fim: null` (conta até hoje automaticamente).
2. Rode `python3 pipeline/vacancias.py <sigla>` → `agencias/<sigla>/mandatos/README.md` (estatísticas + tabela de mandatos com fontes) e `agencias/VACANCIA_AGENCIAS.md` (comparativo). Depois `organizar.py <sigla>` para a aba «Vacâncias» da planilha.
3. Ao responder: cite média/mediana/máx, vagas em aberto (com dias até hoje), a % de dias-cadeira vagos desde 2023, a confiança e que posses não confirmadas no DOU são estimadas.
4. Semanalmente (tarefa de monitoramento): checar notícias de nomeação/renúncia/convocação (Agência Senado, DOU, Agência iNFRA) de cada agência e atualizar.
