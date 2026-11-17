# Estudo de produtos para empresas reguladas que atuam em 2–3 agências (Grupo Nery)

*17/11/2026. Uso interno. Pesquisa web em português. Números de terceiros (imprensa, relatórios de gestão, estimativas de mercado) estão marcados **(não conferido)**. Nenhum cliente é citado. Preços em R$/mês, referência: pacotes de R$ 18 / 38 / 85 mil (`precos.md`).*

**Limite da pesquisa:** os sites gov.br, dados.antt.gov.br e dadosabertos.aneel.gov.br não abriram neste ambiente (rede restrita). A existência de cada base abaixo vem de **resultados de busca** que citam a página. Antes de construir, confirmar formato, dicionário de dados, licença e data da última atualização abrindo cada página.

## 0. Resumo
- **Tese:** a empresa regulada que atua em 2–3 agências (ex.: grupo logístico em ANTAQ + ANTT; geradora/distribuidora em ANEEL + ANP; mineradora em ANM + ANTAQ + ANTT) não tem hoje quem junte, num só lugar, **o que a agência fez com ela e com os pares** (multa, recurso, consulta, reequilíbrio) e **como a diretoria decide esse tipo de caso**. Nós já temos o segundo termo; os dados públicos externos dão o primeiro.
- **Seis candidatos avaliados** (§3). Dois se destacam: **Radar de sanções e recursos de multa** e **Monitor de consultas públicas com o que a diretoria acatou**.
- **Recomendação:** começar pelo Radar de sanções (MVP em 4–5 semanas, R$ 22–32 mil/mês), com o Monitor de consultas como segundo (3–4 semanas, R$ 15–25 mil/mês). Venda por piloto pago de 1–2 semanas e depois anual (§5).
- **Dependência crítica:** a base de multas de **ANEEL** não foi localizada como conjunto aberto; ANTT, ANP e ANTAQ têm material público confirmado em parte. O MVP deve começar por onde o dado existe (ANTT, ANP, ANTAQ) e tratar ANEEL por pedido de acesso à informação ou leitura das pautas e dos votos (que já temos).

## 1. Dados externos: o que existe de fato
Chave: **Confirmado** = a busca trouxe a página ou o arquivo da fonte; **Parcial** = só relatório, painel ou PDF; **Não localizado** = a busca não achou.

| Dado | Agência/órgão | Situação | O que traz | Fonte |
|---|---|---|---|---|
| Controle de penalidades aplicadas (CSV) | ANTT | **Confirmado** | Histórico de processos de fiscalização com autos de infração e análises de 1ª e 2ª instância, quando cabíveis | [dados.antt.gov.br](https://dados.antt.gov.br/id/dataset/controle-de-penalidades-aplicadas/resource/70b3de9b-f93d-4b17-b059-35d8cabad380) |
| SISMULTAS: autos de infração de passageiros 2025 | ANTT | **Confirmado** | Autos do transporte rodoviário interestadual e internacional de passageiros | [dados.antt.gov.br](https://dados.antt.gov.br/en/dataset/ca8a6851-d941-478e-b97c-d760d51fadaa/resource/c5f6e8c1-16d2-4f75-9a44-93f7207247d1) |
| Editais de autuação e penalidade, sanções administrativas | ANTT | **Confirmado** (PDF/página) | Editais com autuações e penalidades; consulta ao Portal de Multas | [sanções administrativas](https://www.gov.br/antt/pt-br/acesso-a-informacao/sancoes-administrativas) |
| Multas aplicadas desde 2016 (CSV e PDF; metadados no dados.gov.br) | ANP | **Confirmado** | Nº do auto, CNPJ/CPF do autuado, valor aplicado e pago; posição anual | [metadados](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/mav/metadados-multas-aplicadas-2016a2019.pdf) |
| Ações de fiscalização (abastecimento) | ANP | **Confirmado** | Relatórios de fiscalização, autos, interdições; painel dinâmico | [metadados](https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/arquivos/arquivos-acoes-de-fiscalizacao/metadados-acoes-fiscalizacao.pdf) |
| Processos sancionadores (participações governamentais) | ANP | **Confirmado** (painel, abr/2026) | Autos desde 2019 ligados a royalties e participações; valores cobrados e pagos | [AgênciaiNFRA](https://agenciainfra.com/blog/?p=39948) |
| Planilhas de processos sancionadores por superintendência | ANP | **Parcial** | Arquivos .xlsx por área (ex.: infraestrutura e movimentação) | [ANP SIM](https://www.gov.br/anp/pt-br/acesso-a-informacao/processos-sancionadores/sim/processossancionadoressim1220.xlsx/view) |
| Bases abertas (18 até 2025) e Plano de Dados Abertos | ANTAQ | **Parcial** | Lista de bases; não confirmei multas nem contratos por arrendamento | [página de dados abertos](https://www.gov.br/antaq/pt-br/acesso-a-informacao/dados-abertos) |
| Relatório de gestão: autos e multas, arrendamentos | ANTAQ | **Parcial** | 312 autos e R$ 4,4 mi em multas (2024); 155 arrendamentos vigentes e 13 análises de reequilíbrio no sumário mais recente **(não conferido)** | [relatório 2024](https://www.gov.br/antaq/pt-br/acesso-a-informacao/prestacao_de_contas/relatorio-geral-2024_fase-4-pag-simples.pdf), [sumário executivo](https://www.gov.br/antaq/pt-br/acesso-a-informacao/prestacao_de_contas/relatorio-de-gestao/sumario_executivo_rgi.pdf) |
| Autos de infração, multas, penalidades | ANEEL | **Não localizado** como conjunto aberto | Só casos citados em atas, imprensa e apresentações; norma de penalidades REN 846/2019 | [REN 846](https://www.legisweb.com.br/legislacao/?id=378638) |
| DEC/FEC e limites por concessionária | ANEEL | **Parcial** | Séries apuradas e limites 2014–2023 aparecem em apresentação; CSV no portal de dados abertos não confirmado | [Câmara](https://www2.camara.leg.br/atividade-legislativa/comissoes/comissoes-permanentes/cdeic/apresentacoes-e-arquivos-audiencias-e-seminarios/aneel-05-06.2024) |
| SCM (processos minerários) e CFEM | ANM | **Confirmado** (plano de dados abertos) | Fases, titulares, substâncias; CFEM com maior relevância; **autos e multas não achados** | [Plano de dados abertos](https://www.gov.br/anm/pt-br/acesso-a-informacao/acoes-e-programas/PlanodeDadosAbertos_Reviso2018_2020_V3.pdf) |
| Contribuições a audiências e consultas | ANTAQ | **Confirmado** (PDF) | Relatórios com nome, CNPJ, contribuição, análise técnica e resultado, por audiência | [exemplo](https://www.gov.br/antaq/pt-br/acesso-a-informacao/participacao-social/audiencias-e-consultas-publicas/Relatrio102024Audincia082024.pdf), [lista](https://www.gov.br/antaq/pt-br/acesso-a-informacao/participacao-social/audiencias-e-consultas-publicas/ListaAudincia082024.pdf) |
| Contribuições a consultas (notas técnicas com tabela por agente) | ANEEL | **Parcial** (PDF no SEI/anexos) | Ex.: CP 51/2021, 179 contribuições de 25 agentes; CP 28/2023, 57 entidades **(não conferido)** | [nota CP 28/23](https://abraceel.com.br/wp-content/uploads/post/2023/12/Nota-Tecnica-Aneel-Analise-das-contribuicoes-da-CP-28-23-Aprimoramento-da-comercializacao-varejista.pdf) |
| Acórdãos, jurisprudência selecionada, súmulas (arquivos abertos) | TCU | **Confirmado** | Cinco bases em formato aberto; inteiro teor desde 1992; resumos por IA reutilizáveis com crédito. API própria **não confirmada** | [dados abertos TCU](https://portal.tcu.gov.br/carta-de-servicos/sessoes-jurisprudencia-e-normativos/jurisprudencia-dados-abertos) |
| DOU em XML (INLABS) | Imprensa Nacional | **Confirmado** | Edições completas em XML e PDF, gratuito, com cadastro | [GitHub Imprensa Nacional](https://github.com/Imprensa-Nacional) |
| API pública DataJud | CNJ | **Confirmado** | Metadados de processos (capa, movimentos) por tribunal; chave pública; limites de volume; termos de uso vedam coleta de dados pessoais de terceiros sem consentimento | [CNJ](https://www.cnj.jus.br/sistemas/datajud/api-publica/) |
| Agenda Regulatória | ANEEL, ANTAQ, ANTT, ANP | **Confirmado** (PDF/boletim) | ANEEL 2026–2027 com 91 atividades **(não conferido)**; ANTAQ 2025–2028 com boletim mensal; ANTT em revisão; ANP com agenda congelada segundo imprensa **(não conferido)** | [ANEEL](https://cenarioenergia.com.br/2025/12/02/aneel-aprova-agenda-regulatoria-2026-2027-e-define-91-temas-que-vao-orientar-a-modernizacao-do-setor-eletrico/), [ANTAQ](https://www.gov.br/antaq/pt-br/acesso-a-informacao/acoes-e-programas/governanca-regulatoria/agenda-regulatoria-ar/18.BoletimAR20252028junho26.pdf) |
| STJ (jurimetria por tema) | STJ | **Não localizado** como dado aberto estruturado | Pesquisa de jurisprudência por palavra-chave; sem base aberta confirmada | — |
| Leilões (resultados, editais) | ANTT/ANTAQ/ANP/ANEEL, B3 | **Parcial** | Editais e resultados em páginas e comunicados; meta de 13–14 leilões rodoviários em 2026 **(não conferido)** | [AgênciaiNFRA](https://agenciainfra.com/blog/governo-faz-13-leiloes-de-rodovias-em-2025-com-investimento-de-r-135-bi/) |

**Leitura:** o dado mais rico para o Radar de sanções está em **ANTT e ANP** (CSV com CNPJ e valor). ANTAQ tem o dado mais rico de **consultas** (tabela por CNPJ). ANEEL exige trabalho manual ou pedido de acesso. TCU e DOU são insumos de contexto, não o produto.

Números de mercado para dimensionar **(não conferido)**: ANTT com 31 contratos rodoviários ativos e cerca de 15,8 mil km ([relatório de gestão 2025](https://www.gov.br/antt/pt-br/acesso-a-informacao/transparencia-e-prestacao-de-contas/prestacao-de-contas-anuais/2025/relatorio-de-gestao-antt-2025-27-04.pdf/@@download/file)); ANP com 17.341 ações de fiscalização e 4.600 autos em 2024 ([Monitor Mercantil](https://monitormercantil.com.br/anp-fez-mais-de-17-mil-acoes-de-fiscalizacao-em-2024/)); uma distribuidora de energia com cerca de R$ 606 milhões em multas em cinco anos, dos quais só R$ 119,6 milhões pagos ([Viva](https://viva.com.br/cidadania-e-direitos/enel-acumula-mais-de-600-milhoes-em-multas-a-maioria-em-sp.html)); teto de multa ANEEL de 3% do faturamento por infração ([Lei 9.427/1996](https://www2.camara.leg.br/legin/fed/lei/1996/lei-9427-26-dezembro-1996-366792-normaatualizada-pl.docx)).

## 2. O que já existe no repositório (reaproveitável em todos os produtos)
| Ativo | Arquivo | Serve para |
|---|---|---|
| Votos por diretor, falas com minuto, relator, vista | `data/regulacao.db`, `pipeline/consulta.py`, `mapa_tema.py` | «Como a diretoria julgou recursos e pleitos parecidos» |
| Prazo mediano por tipo de processo | `pipeline/prazos.py` | «Quando será decidido» |
| Casos semelhantes com desfecho e justificativa | `pipeline/similares.py`, `desfecho.py` | Precedentes por multa, consulta ou reequilíbrio |
| Alerta quando o item entra em pauta | `pipeline/alerta_pauta.py`, `pautas.py`, calendários | Aviso antes da sessão que julga o recurso |
| Documento mensal de processos (8 blocos) e raio-X | `monitor_8blocos.py`, `raio_x.py`, `clientes/<x>/processos.json` | Molde de entrega; estrutura de dados do cliente fora do git |
| Notas de condicionante com prazo | `notas_cliente.py` | Embrião de obrigações e prazos |
| DOU por termos (hoje para mandatos) | `baixar_dou_mac.py`, `conferir_dou.py`, `dou_buscas.json` | Extensão para atos e penalidades por razão social |
| Mandatos, vacância, calendário, pautas de 12 agências | `data/mandatos_agencias.json`, `vacancias.py` | Contexto de quem decide e quando |
| Microtemas | `data/microtemas.json` | Classificar itens por tema (multa, reequilíbrio, consulta) |
| Governança de dados do cliente e contrato | skills `dados-do-cliente`, `contratos`, `conformidade-entrega` | LGPD, DPA, sigilo |

## 3. Os seis produtos candidatos

### P1. Radar de sanções e recursos de multa
- **Dor:** a empresa recebe autos de infração em mais de uma agência, com regras, prazos de defesa e valores diferentes. Não sabe quanto pesa o histórico (reincidência conta, por exemplo, quatro anos de antecedentes na ANEEL), nem como a diretoria costuma tratar o recurso: mantém, reduz, anula. Quem decide quanto provisionar e se recorre precisa de taxa de êxito por tema e por relator.
- **Agências:** ANTT, ANP, ANTAQ (dados abertos); ANEEL (via pautas, votos e pedido de acesso); ANM (sem base de autos localizada; só pelas reuniões).
- **Empresas-alvo (estimativa nossa, não conferida):** 150–250 grupos: concessionárias rodoviárias (31 contratos ativos, não conferido), operadoras ferroviárias e de passageiros, arrendatários portuários, distribuidoras e transmissoras de energia, grandes distribuidores e refinarias de combustíveis.
- **Dados nossos:** votos e falas em recursos de multa, relator, vista, prazo mediano do recurso, casos semelhantes.
- **Dados externos:** CSV de penalidades ANTT e SISMULTAS; multas aplicadas e ações de fiscalização ANP; processos sancionadores ANP; relatórios ANTAQ; editais de autuação; DOU (penalidades e inscrição em dívida ativa); acórdãos do TCU sobre fiscalização (contexto de pressão sobre a agência).
- **Já existe:** similares, prazos, alerta de pauta, raio-X, DOU.
- **Falta:** (1) carga e normalização dos CSV por CNPJ (grupo econômico: casar razão social e CNPJs do cliente); (2) classificador de itens «recurso de multa» nas reuniões analisadas; (3) painel «exposição»: autos abertos, valor, fase, prazo para defesa, pagos × aplicados; (4) comparador de pares anônimo; (5) ANEEL: série manual das penalidades citadas em pauta e pedido LAI.
- **Esforço:** 4–5 semanas para ANTT + ANP + ANTAQ; +2 semanas para ANEEL.
- **Preço sugerido:** R$ 22–32 mil/mês (1–2 agências); R$ 40–55 mil/mês com 3 agências e briefing de recurso por trimestre. Implantação R$ 25–50 mil.
- **Concorrência:** Inteligov e Sigalei monitoram texto e andamento no SEI (ANTT e ANP aparecem) mas não medem como a diretoria julga o recurso; escritórios de contencioso administrativo fazem caso a caso, sem estatística. Brecha clara.
- **Risco:** dados pessoais de responsáveis (usar só pessoa jurídica); autos em curso podem ser sigilosos; o CSV tem defasagem (a ANP fotografa a posição ao fim de cada ano).

### P2. Monitor de consultas e audiências públicas, com o que a diretoria acatou
- **Dor:** a empresa gasta semanas para contribuir e não sabe se valeu a pena. Falta saber: quem mais contribuiu, o que a área técnica aceitou, o que a diretoria mudou na votação e qual diretor defendeu cada ponto.
- **Agências:** ANTAQ (tabela por CNPJ confirmada), ANEEL (nota técnica com tabela por agente), ANTT, ANP, ANM (formato a confirmar).
- **Empresas-alvo (estimativa):** 300–500, incluindo associações e escritórios que contribuem por conta de clientes.
- **Dados nossos:** voto e fala do diretor no item que aprovou a norma; relator; divergências; prazo entre fim da consulta e decisão.
- **Dados externos:** relatórios de contribuições e notas técnicas por consulta; texto da norma aprovada; Agenda Regulatória (o que entra em consulta nos próximos 12 meses); DOU.
- **Já existe:** busca textual, similares, falas com minuto, calendário, pautas.
- **Falta:** (1) extrator de tabelas de contribuições (PDF) por agência, com CNPJ; (2) ligação consulta → resolução → item de diretoria; (3) «taxa de acolhimento» por contribuinte e por tema; (4) alerta de consulta aberta que toca os temas do cliente; (5) rascunho de contribuição com precedentes (serviço, não software).
- **Esforço:** 3–4 semanas (começando por ANTAQ e ANEEL).
- **Preço sugerido:** R$ 15–25 mil/mês; R$ 8–15 mil por contribuição assistida (avulso).
- **Concorrência:** Sigalei e Inteligov avisam que a consulta abriu; ninguém mostra o que foi acatado nem o voto. JOTA e iNFRA noticiam os casos grandes.
- **Risco:** PDFs sem padrão; comparar contribuição e texto final exige revisão humana.

### P3. Reequilíbrio, prorrogação e renovação multiagência
- **Dor:** pleitos de reequilíbrio econômico-financeiro, prorrogação antecipada e renovação correm em anos, com prazo, perícia e vista. A empresa precisa de precedentes por tipo de pleito e de uma estimativa do custo de cada mês de atraso.
- **Agências:** ANTAQ (155 arrendamentos vigentes e 13 análises de reequilíbrio, não conferido; recomposição cautelar na agenda para 2027), ANTT (reequilíbrio de concessões; revisão de contratos), ANEEL (renovação de distribuidoras e transmissoras), ANM (mais limitada).
- **Empresas-alvo (estimativa):** 120–200 (arrendatários, concessionárias, distribuidoras com contrato a vencer).
- **Dados nossos:** desfecho dos pleitos, vistas, prazo mediano, argumentos recorrentes, relator.
- **Dados externos:** relatórios de gestão (contagem), agenda regulatória, acórdãos do TCU sobre arrendamento e concessão, DOU (aditivos, portarias), editais e minutas publicados.
- **Já existe:** `prazos.py`, `similares.py`, `monitor_8blocos.py` e os casos já feitos para este tema.
- **Falta:** tabela única «pleito → agência → tipo → fase → decisão» comparável entre agências; base de contratos com data de término e opção de prorrogação (só em parte pública; o resto o cliente envia); quantificação de custo do atraso.
- **Esforço:** 3–4 semanas para tabela e relatório; recorrente por analista.
- **Preço sugerido:** R$ 25–45 mil/mês (acompanhamento de 3–5 pleitos); briefing de sustentação avulso R$ 25–60 mil (tabela vigente).
- **Concorrência:** advocacia regulatória (forte em tese jurídica, fraca em estatística da diretoria); nenhuma ferramenta mede o comportamento decisório.
- **Risco:** número de casos por agência pequeno (n baixo); exige rótulo de inferência e intervalo.

### P4. Calendário de obrigações com risco de sanção
- **Dor e desenho:** já estudados em `produto_compliance_regulatorio.md`. Aqui entra só como **módulo do P1**: cada obrigação mostra a multa típica e como a diretoria tratou o descumprimento.
- **Agências:** as cinco (obrigações repetitivas: SIMP/ANP, DEC/FEC/ANEEL, relatórios de arrendamento/ANTAQ, PER/ANTT).
- **Empresas-alvo:** 200–400.
- **Esforço e preço:** 4–6 semanas; R$ 15–40 mil/mês adicionais (valores do estudo anterior).
- **Concorrência:** SOGI, LegisMap, Cority etc. (ver estudo anterior).
- **Veredito:** não repetir como produto próprio; vender junto do P1.

### P5. Risco TCU e judicial por tema
- **Dor:** decisões da diretoria viram alvo de auditoria do TCU e de ações judiciais (caducidade, reequilíbrio, qualidade do serviço). Investidores e conselhos querem saber a probabilidade de a decisão ser revista.
- **Agências:** ANTT, ANTAQ, ANEEL (mais acórdãos); ANP e ANM em menor volume.
- **Empresas-alvo (estimativa):** 60–100 (concessionárias com investidor financeiro, fundos, bancos de projeto).
- **Dados nossos:** itens e temas decididos, vistas, divergências.
- **Dados externos:** acórdãos TCU em arquivo aberto (confirmado); DataJud para movimentos de processos conhecidos (confirmado, com limites e restrição a dados pessoais); STJ não estruturado; DOU.
- **Já existe:** busca textual e `consulta.py`; nada de TCU nem de tribunais.
- **Falta:** carga dos acórdãos, ligação acórdão ↔ item de diretoria por processo e tema (a numeração SEI aparece em ambos), carga de DataJud por número de processo informado pelo cliente.
- **Esforço:** 5–7 semanas (a ligação entre bases é o trabalho difícil).
- **Preço sugerido:** R$ 20–35 mil/mês; carteira para investidor R$ 60–150 mil/mês (tabela vigente, «risco regulatório de carteira»).
- **Concorrência:** Sigalei acompanha o Judiciário por texto; jurimetria genérica (fora do nosso foco); advocacia.
- **Risco:** só dá para falar de risco com base em casos conhecidos; não prometer probabilidade de reforma.

### P6. Benchmark do mesmo tema entre agências
- **Dor:** o mesmo assunto (qualidade do serviço, tarifa, caducidade, sanção, consulta, transparência) é tratado de modo diferente por agência; o grupo com ativos em duas ou três agências quer saber onde o risco é maior e onde há precedente para argumentar em outra.
- **Agências:** as cinco, com base de votos em ANTT, ANM, ANTAQ e as outras em andamento.
- **Empresas-alvo (estimativa):** 80–150 grupos multiagência, associações e investidores.
- **Dados nossos:** vacância e mandatos das 12 agências, transparência, prazos por tipo, votos, taxa de divergência.
- **Dados externos:** agenda regulatória, relatórios de gestão (autos e multas por agência), dados abertos para o tema escolhido.
- **Já existe:** vacância, transparência, prazos, comparador de diretores; produto avulso «comparativo entre agências» (R$ 80–150 mil).
- **Falta:** taxonomia de temas comum entre agências, normalização de indicadores, texto analítico por tema.
- **Esforço:** 2–3 semanas por estudo; cada estudo é um projeto.
- **Preço sugerido:** estudo avulso R$ 80–150 mil; acompanhamento trimestral R$ 12–20 mil/mês.
- **Concorrência:** nenhuma comparável; consultorias de risco político fazem em texto.
- **Veredito:** ótimo para marketing e como prova de valor; baixa recorrência por si só.

### Quadro comparativo
| Produto | Dor | Dado externo aberto | Reuso do repo | Semanas | R$/mês | Recorrência | Nota |
|---|---|---|---|---|---|---|---|
| P1 Radar de sanções | alta | alto (ANTT, ANP, ANTAQ) | alto | 4–5 | 22–32 mil | alta | **A** |
| P2 Consultas públicas | média-alta | médio (PDF) | alto | 3–4 | 15–25 mil | alta | **A** |
| P3 Reequilíbrio e prorrogação | alta | baixo | muito alto | 3–4 | 25–45 mil | média | B+ |
| P4 Calendário de obrigações | média | médio | médio | 4–6 | 15–40 mil | alta | B (módulo) |
| P5 Risco TCU e judicial | média | médio (TCU), baixo (STJ) | baixo | 5–7 | 20–35 mil | média | B- |
| P6 Benchmark entre agências | média | médio | alto | 2–3 por estudo | 12–20 mil (acomp.) | baixa | B (marketing) |

## 4. Concorrência: onde cada um para
- **Inteligov:** cobertura declarada de Legislativo, diários oficiais e agências, com «Termômetro» de aprovação de projetos de lei ([Âmbito Jurídico](https://ambitojuridico.com.br/termometro-nova-ferramenta-da-inteligov-mede-a-probabilidade-de-aprovacao-das-proposicoes-da)). Não mostra voto de diretor nem resultado de recurso.
- **Sigalei:** módulo regulatório com triagem, prazos e trilha de auditoria, acompanhamento de processos no SEI de órgãos como ANP e ANTT ([módulo](https://www.sigalei.com.br/regulatorio)). É o mais próximo: pode juntar sanção e consulta por texto. Não mede o comportamento da diretoria.
- **Jornalismo (JOTA PRO, iNFRA, MegaWhat, eixos):** noticia os casos grandes de multa e consulta; sem base estruturada.
- **Advocacia regulatória e contencioso:** concorrente real em P1 e P3; vira **canal** se entregarmos a estatística como insumo.
- **Lá fora (referência de preço, não conferida):** Regology cerca de US$ 1.700 por usuário por mês segundo terceiros; Politico Pro cerca de US$ 5 mil por vertical por ano.
- **Defesa:** base histórica conferida, qualidade medida, ligação entre dado público da empresa e voto da diretoria.

## 5. Recomendação
**Fazer primeiro, nesta ordem:**
1. **P1 Radar de sanções e recursos de multa**, com o calendário de obrigações (P4) como módulo opcional.
2. **P2 Monitor de consultas públicas**, aproveitando a mesma carga por CNPJ e a mesma tabela de «grupo econômico» do cliente.

**Por quê:** (a) o dado aberto existe e foi confirmado em ANTT, ANP e ANTAQ; (b) a dor aparece todo mês, o que dá recorrência; (c) o nosso diferencial (como a diretoria julga recursos e aprova normas) é exatamente o que falta nessas bases; (d) o piloto cabe em 1–2 semanas com dado público; (e) as duas partes compartilham a ficha da empresa e o motor de alertas, então o custo do segundo é menor.

**P3** vem em seguida como venda cruzada nos contratos grandes. **P5** só depois de um cliente pedir. **P6** como material de entrada e pauta de imprensa.

### MVP do P1 (4–5 semanas)
- Semana 1: carga ANTT (penalidades, SISMULTAS) e ANP (multas aplicadas, fiscalização), com chave por CNPJ; tabela de grupos econômicos de 10 empresas de teste (dados públicos).
- Semana 2: ANTAQ (relatórios de gestão e editais) e classificador de itens «recurso de multa» nas reuniões já analisadas; taxa de manutenção, redução e anulação por agência e por relator.
- Semana 3: documento mensal «Exposição a sanções»: autos abertos, valor, fase, prazo mediano do recurso, 3 precedentes com link no minuto; alerta de pauta para o recurso do cliente.
- Semana 4: comparação anônima com pares do mesmo segmento; revisão humana e conferência por amostra; checagem de português e de links.
- Semana 5 (opcional): ANEEL por pedido de acesso e leitura de pauta.
- **Entrega ao cliente:** PDF mensal + planilha + alerta por e-mail. Sem plataforma nova.
- **Critério de pronto:** 100% dos trechos literais encontrados na transcrição; todo número de multa com fonte e data da extração; aviso de defasagem das bases.

### Como vender
1. **Lista:** empresas com presença em 2–3 agências (grupos logísticos, de energia, de combustíveis, mineradoras com porto e ferrovia) a partir de `prospects.csv`, priorizando as que têm auto recente em dado público.
2. **Abordagem:** prévia gratuita de 1 página com o nº de autos da empresa na base pública e a taxa de êxito de recursos parecidos na diretoria (só dado público).
3. **Piloto pago de 1–2 semanas:** R$ 25–35 mil, com 3 autos ou consultas reais do cliente. Entrega: exposição, precedentes, prazo previsto, agenda. Abatido do primeiro mês se fechar o anual em 30 dias (regra de `precos.md`).
4. **Conversão combinada antes:** o cliente diz o que precisa ver («quanto provisionar», «recorrer ou pagar com desconto», «quem relata»). Conferimos item a item na devolutiva.
5. **Anual:** P1 sozinho R$ 22–32 mil/mês; P1 + P2 R$ 35–50 mil/mês (abaixo da soma, para incentivar); dentro do pacote Inteligência (R$ 38 mil) como bônus de 3 meses para quem já é cliente.
6. **Canais:** parceiros de advocacia e consultoria (50/50), associações setoriais com relatório patrocinado, e o comparativo entre agências (P6) como peça de conteúdo.

## 6. Riscos gerais e pendências
- **Dado:** defasagem, mudança de formato e falta de dicionário. Registrar a data de extração em todo documento.
- **LGPD:** só pessoa jurídica no cadastro; nomes de pessoas físicas em autos não entram; dados do cliente em `clientes/` (fora do git) sob DPA.
- **Promessa:** mostrar frequência histórica com n e rótulo de inferência; nunca «a multa será reduzida».
- **Responsabilidade:** serviço de apoio; não substitui o jurídico nem o responsável pelo prazo.
- **Pendências para confirmar abrindo as páginas (rede liberada):** ANEEL (existência de CSV de fiscalização e de DEC/FEC), ANTAQ (bases abertas de contratos), ANM (autos e multas), licença e atualização dos CSV da ANTT e da ANP, existência de API no TCU, termos de uso do DataJud para uso comercial.
