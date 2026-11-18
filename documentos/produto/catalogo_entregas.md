# Catálogo completo — documentos, dados e serviços (Grupo Nery)

*Atualizado 18/11/2026. Para cada item: o que é, de onde vem o dado, status e script.*

## 1. Pacote mensal do cliente (empresa regulada)
| Entrega | O que traz | Fonte do dado | Script | Status |
|---|---|---|---|---|
| Relatório da empresa | Processos/calendário, diretoria (minibio/mandato), decisões setoriais, previsão (placar/backtest) | `data/regulacao.db` (votos, falas, mandatos) + `clientes/<x>/processos.json` | `relatorio_empresa.py`, `relatorio_nery.py` | pronto |
| Boletim mensal | Mês em números, decisões por tema, vistas/divergências, quem relatou, empresas em pauta, diretoria/vagas, eventos, cobertura | base + `data/<ag>/calendario.json` | `boletim_cliente.py`, `boletim.py` | pronto |
| Raio-X dos processos | Linha do tempo, prazo estimado vs. ≥20 semelhantes, condicionantes com prazo | `clientes/<x>/processos.json` + `pipeline/prazos.py`/`similares.py` | `raio_x.py` | pronto |
| Agenda comparativa | Próximas pautas, precedentes, contradições da diretoria nos temas do cliente | pautas publicadas + base de votos | `agenda_comparativa.py` | pronto |
| Monitoramento 8 blocos | Visão geral, mapeamento, prazo, agenda, agência, busca, comparativa, visão do cliente, para 1–3 processos | `clientes/<x>/processos.json` | `monitor_8blocos.py` | pronto |
| Alerta pré-pauta | Item do cliente na pauta nova: relator, como cada diretor votou em casos parecidos, previsão rotulada como inferência | pauta publicada + base | `alerta_pauta.py` | pronto |
| Dossiê de perguntas com evidência | N perguntas → PDF ~13 páginas, trecho literal + link no minuto, auditado | base + transcrições | `relatorio_v2.py`, auditor-respostas | pronto |
| Planilha viva (votos/processos/prazos) | Votos por diretor em Excel | base | `planilha_votos.py`, `planilha_cliente.py` | pronto |
| Previsão de voto/placar | Placar provável de um item futuro, com backtest e n por diretor | base + `mapa_tema.py` | `previsao.py` | pronto |
| Casos semelhantes/precedentes | Decisões parecidas com voto de cada diretor e link no minuto | base | `similares.py` | pronto |
| Comparador de diretores | Todos os diretores em exercício lado a lado nos mesmos indicadores | base | `relatorio_diretoria.py` | pronto |

## 2. Documentos públicos por agência (sem dado de cliente — podem ir ao GitHub)
| Entrega | O que traz | Fonte | Script | Status |
|---|---|---|---|---|
| Panorama da agência | Números/temas, quem decide (mandatos/cadeiras), quanto tempo leva, transparência | base da agência + `data/<ag>/transparencia.json` | `documentos_agencia.py` | pronto (ANTT, ANM, ANTAQ, ANEEL) |
| Vacância de diretoria | Média/mediana/máximo de dias-cadeira vaga, comparativo entre agências | `data/*/mandatos.json`, `vacancias.json` | `vacancias.py` | pronto |
| Transparência comparada | Nota 0–2 por critério (transmissão, legenda, pauta, ata, calendário, sigilo) por agência | pesquisa pública + agente auditor-transparencia | `transparencia.py` | pronto (12 agências) |
| Auditoria de mandatos | Composição da diretoria x DOU, link por link | `data/mandatos_agencias.json` + DOU | agente pesquisador-mandatos + `conferir_dou.py` | pronto (2ª rodada) |
| Dashboard geral (todas as agências, várias empresas) | 8 abas, filtro por empresa/período/agência | base consolidada | `dashboard_geral.py` | pronto |
| Dashboard por cliente | Painel privado do cliente | `clientes/<x>/` | `dashboard.py` | pronto (CS Portos) |

## 3. Material comercial (Grupo Nery)
| Entrega | O que é | Script/arquivo | Status |
|---|---|---|---|
| Apresentação institucional (15 páginas) + one-pager | Posicionamento, produto, como trabalhamos | `apresentacao_nery.py` | pronto |
| Demo de prospecção (4 páginas, só dado público) | Gancho comercial para uma empresa-alvo | `demo_empresa.py` | pronto |
| Prévia completa gratuita | Versão cheia do relatório para converter prospect | `previa_completa.py` | pronto |
| Posts/carrossel (setor, agência) | Conteúdo para Instagram/LinkedIn, sem citar cliente nem método | skill `post-setor` | pronto |
| Planilha de prospects | Empresas-alvo por setor com motivo de interesse | `documentos/comercial/prospects.csv/.xlsx` | 203 linhas, contatos institucionais pendentes |
| E-mails de cadência | Sequência de prospecção personalizada | `documentos/comercial/emails.md` | pronto, revisão comercial pendente |
| Estudos de posicionamento/preço | Preços (`precos.md`), estratégia (`estrategia.md`), concorrentes (`concorrentes.md`), casos (`casos_detalhados.md`), valor (`valor_e_produtos.md`, `exemplos_de_valor.md`), referência Palantir (`referencia_palantir.md`) | `documentos/comercial/` | prontos |

## 4. Produtos novos em estudo (ainda não construídos — ordenados por prioridade)
| Produto | Dor | Dado nosso | Dado externo que falta | Esforço | Preço sugerido | Documento |
|---|---|---|---|---|---|---|
| **Radar de sanções e recursos de multa** | Multas em mais de uma agência, sem saber taxa de êxito do recurso | Votos/falas em recursos, prazo, similares | CSV de multas ANTT/ANP (confirmado); ANTAQ parcial; ANEEL manual | 4–5 semanas | R$ 22–32 mil/mês | `produtos_empresas_reguladas.md` |
| **Monitor de consultas públicas** | Não sabe o que foi acatado nem quem decidiu | Voto/fala no item que aprovou a norma | Tabelas de contribuição por CNPJ (ANTAQ confirmado, ANEEL parcial) | 3–4 semanas | R$ 15–25 mil/mês | idem |
| Calendário de obrigações regulatórias | Prazos de envio (SIMP, DEC/FEC etc.), risco de multa por atraso | Notas de condicionante, prazos | Cadastro de obrigações por setor (a construir) | 4–6 semanas | R$ 15–40 mil/mês (módulo) | `produto_compliance_regulatorio.md` |
| Reequilíbrio/prorrogação multiagência | Precedentes e prazo por tipo de pleito, várias agências | Desfechos, vistas, prazo mediano | Relatórios de gestão, TCU | 3–4 semanas | R$ 25–45 mil/mês | `produtos_empresas_reguladas.md` |
| Risco TCU e judicial por tema | Decisão pode ser revista pelo TCU/Justiça | Itens/temas decididos | Acórdãos TCU (confirmado); DataJud (confirmado, limitado) | 5–7 semanas | R$ 20–35 mil/mês | idem |
| Benchmark do mesmo tema entre agências | Mesmo assunto, tratamento diferente por agência | Vacância, transparência, prazos, votos | Agenda regulatória, relatórios de gestão | 2–3 semanas/estudo | R$ 80–150 mil/estudo | idem |
| Fontes de alto impacto a incorporar nos produtos acima: CVM (fatos relevantes), Receita Federal/CNPJ (grupo econômico), indicadores setoriais (DEC/FEC, SIMP), consultas/audiências públicas | — | — | ver `pesquisa_dados_alto_impacto.md` | — | — | `pesquisa_dados_alto_impacto.md` |

## 5. Agências cobertas
| Agência | Status |
|---|---|
| ANTT, ANM, ANTAQ | Base madura (~97% analisado), conferência cega ~94–95% |
| ANEEL | 739 reuniões analisadas, conferência cega em correção (85,4% nos votos 2018–2023 após ajuste de regra) |
| ANP, ANA, ANAC | Coleta em andamento; análise ainda não iniciada |
| ARTESP | Em avaliação (agência nova, estadual — ver docs/lotes.md) |
| ATEL, ANVISA, ANS, ANCINE, ANPD | Só mandatos/vacância, sem votos |
