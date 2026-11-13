# Os 8 blocos do «dashboard» viram entregas (sem sistema): como começar cada um
| Bloco | Entrega | Base já pronta | Primeiro passo | Esforço |
|---|---|---|---|---|
| 4. Agenda regulatória | **Agenda semanal + alerta de pauta** (e-mail ou PDF de 1 página) | reuniões passadas e resultados | `pipeline/pautas.py`: baixar pautas publicadas no gov.br de ANTT, ANM e ANTAQ (curl, já liberado), extrair itens e processos e ligar ao resultado depois da reunião | médio, uma vez; depois automático |
| 5. Inteligência sobre agências | **Quadro da diretoria + comparador** (já existe) | perfis, mandatos, superintendentes | incluir no relatório de 10 perguntas; checagem do dia 1 | pronto |
| 6. Busca e banco ≥ 3 anos | **Consulta sob demanda** (chat) + **planilha por cliente** | `consulta.py`, SQLite, planilhas | criar `entidades.json` da ANTAQ; busca unificada nas 3 agências (`consulta.py busca --todas`) | baixo |
| 7. Inteligência comparativa | **Casos semelhantes** (dentro do alerta e do raio-X) | votos, justificativas, temas, desfecho | `pipeline/similares.py`: top 20 por tema + empresa + palavras do assunto, com desfecho e justificativa | baixo |
| 3. Inteligência de prazo | **Raio-X trimestral** (prazo estimado) | datas de pauta, vista, retirada e decisão | `pipeline/prazos.py`: duração do primeiro aparecimento em pauta até a decisão, por tipo de processo (mediana e faixa); depois ampliar com datas do SEI que o cliente informar | médio |
| 1, 2. Visão geral e mapeamento do processo | **Raio-X do processo** (linha do tempo) | aparições do processo nas reuniões | `clientes-privado/<cliente>/processos.json` (nº SEI e andamentos que o cliente repassa) + o que está na base e nas pautas | médio |
| 8. Visão do cliente | **Pacote mensal do cliente** (relatório por empresa + raio-X + alertas do mês) | `relatorio_empresa.py` | comando `/cliente <nome>` que gera tudo o que o cliente contratou | baixo |
| Boletim mensal (produto à parte) | **Boletim da agência** | base completa e diretoria | piloto da ANTT (abaixo) | médio |

**SEI:** sem contornar CAPTCHA. Usar o nº e os andamentos informados pelo cliente, as intimações que ele recebe, o DOU e a consulta pública só quando não houver bloqueio.


## Ordem sugerida
1. Boletim mensal da ANTT (piloto pronto: `pipeline/boletim.py antt 2026-10`).
2. `pautas.py` (agenda e alerta), que destrava os blocos 1, 2 e 4.
3. `similares.py` e `prazos.py` (blocos 3 e 7).
4. `/cliente <nome>` (bloco 8), juntando relatório por empresa, raio-X e alertas.
