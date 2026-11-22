# Plano comercial com a Circle: fluxo, Radar de Previsibilidade e novos clientes

*22/11/2026. Uso interno. Retirada de pauta é sempre fato com fonte; nunca motivo pessoal ou ilícito atribuído a diretor (cláusula 8 do contrato de parceiro).*

Contatos: `prospects_contatos.xlsx` (gerar de novo com `python3 pipeline/contatos_mac.py && python3 pipeline/contatos_xlsx.py` no Mac). Indicador: `python3 pipeline/retiradas.py <ag> diretores|processo <nº>|empresa <nome>`.

## 0. Fluxo comercial e de entrega — o que fazer, que relatório e que informação em cada etapa
| Etapa | O que fazer | Documento | Informação entregue | Já existe? |
|---|---|---|---|---|
| 1. Abordagem | Primeiro contato (direto ou pelo Marcelo) | **Demo de 4 páginas** (`demo_empresa.py`) ou **panorama da agência** (`documentos_agencia.py`) | Quem decide os temas da empresa, como votam, prazos médios, casos públicos parecidos — só dado público | Sim (script pronto) |
| 2. Reunião de diagnóstico | Ouvir dores e pegar 2–3 processos | **Prévia completa** (`previa_completa.py`) | Relatório inteiro com dado público + o que fica de fora sem contrato | Sim |
| 3. Piloto pago (1–2 semanas) | Monitorar os 2–3 processos reais | **Raio-X** + **8 blocos** + **alerta de retirada/pauta** | Linha do tempo, prazo esperado × semelhantes, relator e histórico dele, retiradas, próximos passos | Raio-X e 8 blocos sim; alerta de retirada **a construir** (§1) |
| 4. Contrato (mensal) | Rotina de acompanhamento | **Pacote mensal**: relatório da empresa, boletim, raio-X, agenda comparativa, 8 blocos, planilha | Mês da agência, processos, diretoria/mandatos, previsão rotulada como estimativa | Sim (rodando na CS Portos) |
| 5. Evento urgente | Pauta nova ou retirada de processo do cliente | **Alerta pré-pauta** / **alerta de retirada** (1 página, no mesmo dia) | Item, relator, como votou em casos parecidos, motivo dito na sessão com link no minuto | Pré-pauta sim; retirada **a construir** |
| 6. Ação da Circle | Circle decide a via institucional | (informação do alerta; a decisão é da Circle) | Fatos com fonte; nunca hipótese de motivo | — |
| Escritórios (atacado) | Licença da ferramenta | Painel/dashboard + alertas | Monitoramento dos processos dos clientes deles + mapa dos diretores | Dashboard existe; versão "escritório" (vários clientes) **a adaptar** |

### Situação por empresa-alvo
| Alvo | Agência | Material pronto hoje | Falta |
|---|---|---|---|
| CS Portos | ANTAQ | Pacote completo (5 docs), dashboard, demo | Alerta de retirada |
| CCR, EcoRodovias, Vinci (rodovias) | ANTT | Base madura; **nenhum demo gerado ainda** | Gerar demos (minutos, só dado público) |
| Infraamerica, Vinci aeroportos, aéreas | ANAC | **Nada** — ANAC tem só 11 de ~850 reuniões | Coleta no Mac (§1b) + análise em lote combinado |
| Hidrovias, Santos Brasil, Rumo | ANTAQ/ANTT | Demos/prévia/relatório de exemplo | — |
| Energisa, Neoenergia, Enel SP | ANEEL | Demos | Qualidade ANEEL em ajuste |
| SIMINERAL / Vale | ANM | Panorama PDF + relatório de exemplo | — |
| Escritórios | várias | One-pager geral | One-pager específico + painel multi-cliente |

## 0b. Serviço novo que gera cliente novo e alimenta a consultoria do Marcelo: **Radar de Previsibilidade Regulatória**
Tudo o que a Circle já faz (monitoramento em Brasília, relacionamento) depende de saber **antes** onde agir. O Radar junta, por empresa, 4 sinais que já temos ou estão perto:
1. **Retirada de pauta atípica** do processo da empresa (§1) — fato, com motivo dito na sessão e histórico do relator.
2. **Sucessão de diretoria**: mandato do relator vencendo, cadeira vaga, indicação ao Senado, sabatina marcada (já temos `mandatos_agencias.json`, `vacancias.py`, `cadeiras.json`). É a janela legítima de interlocução institucional — é onde a Circle mais agrega.
3. **Agenda regulatória e consultas abertas** que tocam o setor da empresa (prazo para contribuir).
4. **Prazo esperado × prazo real** do processo (`prazos.py`): atraso acima do normal vira alerta.
- **Por que traz cliente novo:** é uma dor de toda concessionária (não só de quem já tem jurídico grande) e se vende com uma página de demo por empresa; o próximo passo natural é "e agora, quem fala com quem?" → consultoria do Marcelo.
- **Preço ao Nery:** dentro da linha de R$ 6–7 mil/mês (escritório/monitoramento) e R$ 10–20 mil (concessionária via Circle).
- **Entrega:** 1 página semanal por empresa + alerta no mesmo dia; reaproveita `alerta_pauta.py`, `notas_cliente.py`, `monitor_8blocos.py`.
- **Limite fixo:** só fatos com fonte; nada de hipótese de motivo (ver Contexto).

## 0c. Plano para conseguir clientes novos
| Semana | Ação | Material |
|---|---|---|
| 1 | Demos do Radar para 10 concessionárias ANTT (Motiva/CCR, Ecorodovias, Arteris, Vinci Rodovias, Rumo, VLI etc.) e 5 portuárias ANTAQ | `demo_empresa.py` + página "Radar" |
| 1 | One-pager para escritórios (linha atacado) | `apresentacao_nery.py` versão curta |
| 2 | Contato direto: 20 empresas A + 15 escritórios de regulatório/infra, cadência de 3 e-mails (`emails.md`) + LinkedIn | lista XLSX (abaixo) |
| 2–3 | Pelo Marcelo: as 5–8 concessionárias que ele conhece (Motiva, Ecorodovias, Infraamerica, Vinci, aéreas) | demos + Radar |
| 3–4 | Associações (ABCR, ABTP, ANTF, SIMINERAL, ABEAR, ABDIB) | panorama da agência como isca |
| contínuo | Post semanal com dado agregado (vacância, prazos, retiradas por agência) | skill `post-setor` |
Meta: 15 demos enviadas/mês → 5 reuniões → 1–2 pilotos → 1 contrato/mês.

## 0d. Lista XLSX de contatos (`documentos/comercial/prospects_contatos.xlsx`)
- Base: os 203 prospects de `prospects.csv` (hoje **sem nenhum e-mail/telefone**), mais duas abas novas: **escritórios de advocacia regulatória/infra** (~40) e **aviação** (aeroportos concedidos e aéreas, ~15).
- Colunas: empresa, segmento, agência, por que é alvo (dado da base), prioridade, canal da Circle (sim/não), site, telefone institucional, e-mail institucional (contato/RI/imprensa/relações institucionais), página do LinkedIn da empresa, **cargo-alvo** (diretor regulatório, jurídico, RI, relações institucionais), fonte e data.
- **LGPD:** só contato institucional público (site, RI publicado na CVM, fale-conosco). Nada de e-mail ou celular pessoal; o nome de executivo só se estiver publicado pela própria empresa/CVM como cargo.
- Como preencher: agentes `pesquisador-prospects` em paralelo por bloco (rodovias, portos, aviação, energia, escritórios). A nuvem bloqueia vários sites; o que não abrir fica marcado "conferir" — e dou um comando para o Mac completar os sites bloqueados.
- Revisão pelo `revisor-comercial` antes de entregar.

## 0e. Agências que faltam e reuniões novas dos últimos dias
**Agências ainda sem análise de votos:**
| Agência | Situação | Próximo passo |
|---|---|---|
| ANAC | 11 de ~850 vídeos coletados | Coleta no Mac (§1b); prioridade alta (aeroportos/aéreas) |
| ANP | 237 com texto, 0 analisadas | Lista histórica de diretores no config → lote teste de 20 + conferência cega → lotes combinados |
| ANA | 152 com texto, 0 analisadas | Idem, depois da ANP |
| ANATEL, ANVISA, ANS, ANCINE, ANPD | Só mandatos/vacância | `iniciar_agencia.py` + inventário do canal + lista histórica de diretores; coleta no Mac numa só fila. Ordem: ANATEL, ANVISA, ANS, ANPD, ANCINE |
| ARTESP | Sem canal de vídeo confirmado | Usuário confere no YouTube; sem vídeo, só Diário Oficial |
- Para incluir as 5 novas na fila do Mac: acrescentar em `FILA` de `pipeline/coletar_todas.sh` e passar um único comando (`coletar_todas.sh`), um terminal só.

**Reuniões novas das agências já cobertas (checagem rápida, sem gastar análise):**
- `git pull` traz o que o Mac coletou; rodar `completude.py` e listar `.md` sem `.analise.json` em ANTT, ANTAQ, ANM e ANEEL.
- Se houver poucas (esperado: 1–3 por agência desde o dia 14), analisar com Sonnet num lote pequeno, indexar e atualizar o pacote da CS Portos (ANTAQ). Se o Mac não coletou nos últimos dias, passar o comando rápido:
```bash
cd ~/REGULACAO-GRUPONERY && git pull && caffeinate -i bash pipeline/coletar_todas.sh
```

