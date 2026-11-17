# Estudo de viabilidade: «Compliance Regulatório do Cliente» (Grupo Nery)

*Novembro de 2026. Pesquisa web em português e inglês. Valores de terceiros estão marcados **(não conferido)**: vêm de imprensa ou de páginas de fornecedores e não foram checados em fonte primária. Nenhum cliente é citado.*

## 0. Resumo
- **Produto:** passar de «como a diretoria decide» para «o que **a minha empresa** deve à agência e quando»: cadastro de obrigações (contrato de concessão ou arrendamento, outorga, resoluções, licenças), calendário de prazos, alertas, evidência de cumprimento e risco de multa, ligado ao que a Grupo Nery já sabe sobre a diretoria (como ela pune, em quanto tempo decide, quem relata).
- **Veredito:** **vale, como extensão premium e não como software isolado.** O mercado de GRC/EHS genérico está ocupado; o que não existe é a ligação entre a obrigação contratual e o comportamento decisório da agência setorial (ANTT, ANTAQ, ANEEL, ANP, ANM).
- **MVP:** 4–6 semanas. **Venda:** piloto pago de 1–2 semanas com 3 obrigações ou processos reais, depois contrato anual.
- **Preço sugerido:** R$ 15–40 mil por mês de adicional, conforme o número de contratos e de agências (ver §4.4).

## 1. Referência: Palantir × The Nuclear Company e casos parecidos
| Caso | O que foi entregue | Fonte |
|---|---|---|
| **The Nuclear Company (TNC), 2025** | «Nuclear Operating System» (NOS): plataforma de IA para construir reatores com fluxo padronizado e repetível; inclui gêmeos digitais, análise preditiva, **monitoramento de conformidade regulatória** e cadeia de suprimentos. Engenheiros da Palantir trabalham junto da equipe da TNC. Cerca de **US$ 100 mi em 5 anos (não conferido)**. | [Baxtel](https://baxtel.com/news/palantir-to-develop-ai-software-for-the-nuclear-company), [GuruFocus](https://www.gurufocus.com/news/2948538/palantir-teams-up-to-build-ai-operating-system-for-nuclear-power), [Mezha](https://mezha.media/en/news/palantir-develops-ai-software-for-nuclear-reactors-302962) |
| **PG&E (distribuidora, EUA), desde 2021** | Foundry para confiabilidade da rede e risco de incêndio; apoio às decisões de desligamento preventivo (PSPS), que **precisam ser reportadas ao regulador**. | [Motley Fool](https://www.fool.com/investing/2021/01/19/palantir-partners-with-pge-to-improve-californias), [PG&E Currents](https://pgecurrents.com/articles/3051-pg-e-investing-centralized-data-analytics-drive-data-informed-decisions-reduce-risk), [docs Palantir PSPS](https://palantir.com/docs/foundry/use-case-examples/public-safety-power-shutoff-psps-scoping/) |
| **BP (O&G), desde 2014** | Gêmeo digital da produção com dados de mais de 2 milhões de sensores (não conferido); foco operacional, não regulatório. | [World Oil](https://worldoil.com/news/2024/9/9/bp-to-deploy-palantir-technologies-ai-digital-twin-software-to-support-oil-and-gas-operations) |
| **APA (O&G)** | Cadeia de suprimentos, manutenção e **anomalias em contratos e faturas**. | [Offshore Technology](https://www.offshore-technology.com/news/apa-partners-with-palantir/) |
| **Trafigura** | Rastreamento de emissões na cadeia de petróleo e metais (relato ambiental). | [Hart Energy](https://www.hartenergy.com/exclusives/palantir-trafigura-aim-track-carbon-emissions-oil-metals-industry-200355) |

**Lição para a Grupo Nery:** a Palantir vende uma **camada de integração com engenheiros embarcados** que transforma regra em fluxo de trabalho. O caso TNC mostra que empresas reguladas pagam caro por «saber o que devo, a quem e quando, com prova». Não temos escala Palantir; a versão possível é o **serviço com engenharia leve**: cadastro curado por analista e alertas automáticos, sobre a base pública que já temos.

## 2. Concorrentes e ferramentas
### Brasil
| Ferramenta | O que faz | Sobreposição | Preço público |
|---|---|---|---|
| **Inteligov** (2014) | Monitoramento legislativo e regulatório, extração de dados públicos, compliance jurídico. [B2B Stack](https://www.b2bstack.com.br/compare/legalbusiness-vs-inteligov) | Média: avisa o que muda na norma, não o que o contrato do cliente exige | Não encontrado |
| **SigaLei** (2015, São Carlos) | Monitoramento do Legislativo; seed de US$ 310 mil (não conferido). [CB Insights](https://www.cbinsights.com/company/sigalei), [DCI](https://www.dci.com.br/dci-mais/noticias/empresas-de-olho-nos-passos-do-legislativo/2493) | Baixa: foco em projetos de lei | Não encontrado |
| **Verde Ghaia: SOGI** | Requisitos legais aplicáveis (ISO 14001/45001), gestão documental e prazos; módulo de IA (SOGI LIA). [Capterra](https://www.capterra.com/p/10008377/SOGI/), [Forbes BV](https://forbes.com.br/brand-voice/2021/05/saiba-como-se-adequar-a-politica-ambiental-brasileira-formada-por-mais-de-140-mil-leis/) | **Alta em licenças ambientais**; baixa em contratos de concessão | Não publicado |
| **LegisMap** | «Gestão de compliance regulatório», requisitos legais. [legismap.com.br](https://legismap.com.br/) | Média–alta em requisitos legais/EHS | Não encontrado |
| **eixos PRO** | Inteligência legislativa e regulatória (energia). [eixos](https://eixos.com.br/eixos-pro/) | Média em energia (notícia e monitoramento) | Não encontrado |
| **Ideagri** | Não confirmado como ferramenta de compliance regulatório: aparenta ser software de gestão agropecuária. **Descartado.** | — | — |
| ERPs (ex.: TOTVS) | Geram arquivos obrigatórios (ex.: envio ao SIMP da ANP). [TDN TOTVS](https://tdn.totvs.com.br/download/attachments/528455576/Orienta%C3%A7oes%20Consultoria%20de%20Segmentos%20-%207876836%20-%20SIMP%20-%20Remessa%20de%20Informa%C3%A7%C3%B5es%20%C3%A0%20ANP%20para%20combust%C3%ADveis%20e%20lubrificantes.pdf?api=v2) | Baixa: geram o arquivo, não controlam a obrigação | — |

Escritórios de advocacia regulatória e as próprias áreas internas de regulação (planilhas) são o **concorrente real** na maioria das empresas.

### Exterior (GRC/EHS)
- **Cority**: gestão de compliance e módulo de licenças (permits) que acompanha a operação contra cada exigência do órgão; linha para utilities. [Cority](https://cority.com/ehsq-software/safety/compliance-management), [Utilities](https://cority.com/industries/utility-and-energy-ehs-software)
- **Intelex**: conteúdo regulatório Enhesa/RegScan dentro do EHSQ. [Intelex](https://intelex.com/products/applications/regulatory-content-gateways)
- **Sphera**: obrigações de compliance corporativas e biblioteca CyberRegs. [Sphera](https://sphera.com/resources/glossary/what-is-compliance-management-and-why-do-we-need-compliance-software/)
- **Enhesa**: conteúdo legal; 14 de 21 plataformas EHS avaliadas pela Verdantix têm parceria com ela (não conferido). [Verdantix](https://www.verdantix.com/insights/blog/compliance-is-king--how-compliance-management-differentiates-ehs-software-firms-in-the-european-market)
- **V-Comply / Nimonik**: obrigações regulatórias para utilities (NERC/FERC no caso dos EUA). [V-Comply](https://www.v-comply.com/blog/energy-and-utilities-compliance-software/), [Nimonik](https://nimonik.com/blog/comparative-analysis-best-regulatory-compliance-management-software/)
- Preços: em geral sob consulta, contratos anuais de cinco a seis dígitos em US$ (estimativa de mercado, **não conferida**).

**Lacuna de mercado:** nenhum deles lê o **contrato de arrendamento ou concessão brasileiro**, o **SEI** da agência nem cruza a obrigação com **como a diretoria pune e decide**. Os de EHS cobrem licença ambiental; os de monitoramento cobrem a norma nova. O «meio», a obrigação contratual e regulatória setorial, fica em planilha.

## 3. Dores reais por setor
**Portos (ANTAQ).** A Resolução 75/2022 impõe deveres a autoridade portuária, arrendatário e autorizatário (serviço adequado, canais com o usuário etc.); a Resolução 112/2024 criou infrações com multa de **até R$ 100 mil** (não conferido) ligadas à armazenagem e a cobranças indevidas; a norma de fiscalização está **em revisão** na Agenda Regulatória 2025–2028. Fontes: [LegisWeb Res. 75](https://www.legisweb.com.br/legislacao/?id=456572), [Res. 112](https://www.contadores.cnt.br/legislacoes/resolucao-no-112-de-13-03-2024.html), [Boletim AR jul/2026](https://www.gov.br/antaq/pt-br/acesso-a-informacao/acoes-e-programas/governanca-regulatoria/agenda-regulatoria-ar/19.BoletimAR20252028julho26.pdf). Dor: contratos de arrendamento com dezenas de obrigações (investimento mínimo, movimentação mínima, seguros, garantias, relatórios periódicos), regra mudando e reequilíbrios que dependem de cumprir prazos.

**Rodovias e ferrovias (ANTT).** O TCU auditou o inadimplemento das concessões (Acórdão 2190/2019) e cobrou da ANTT fiscalização e penalidades; os acordos de reprogramação de obras foram considerados ineficazes; a **Res. ANTT 6.063/2025** traz hipóteses de caducidade, como a reincidência em infrações já sancionadas. Fontes: [TCU auditoria](https://portal.tcu.gov.br/data/files/AF/00/0F/89/1F237810ED256058E18818A8/010.222-2019-7-AAA%20-%20auditoria_inadimplencia_concessoes_rodovias.pdf), [Agência iNFRA](https://agenciainfra.com/blog/?p=14980), [Res. 6.063](https://www.legisweb.com.br/legislacao/?id=498581), [TCU descontos no pedágio](https://portal.tcu.gov.br/imprensa/noticias/tribunal-determina-que-obras-nao-executadas-em-rodovias-federais-se-transformem-em-descontos-nos-pedagios). Dor: cronograma do PER, parâmetros de desempenho, desconto de reequilíbrio e risco de caducidade, com cada infração acumulando histórico.

**Energia (ANEEL).** Distribuidoras enviam dados em fluxo contínuo (indicadores, reclamações, ocorrências); DEC/FEC e seus expurgos (PRODIST, Módulo 8) são alvo de autos de infração e de questionamento no TCU; multas de **R$ 32 mi em 13 fiscalizações** em um caso (não conferido). Fontes: [Parecer AGU/ANEEL](https://www.gov.br/agu/pt-br/composicao/procuradoria-geral-federal-1/subprocuradoria-federal-de-consultoria-juridica/PARECERn.002752023PFANEELPGFAGU.NUP48500.004386202238Seq.2.pdf), [Instrução TCU](https://agenciainfra.com/blog/wp-content/uploads/2026/02/Instrucao-TCU-Enel-RJ.pdf), [ANEEL fiscalização econômico-financeira](https://www.gov.br/aneel/pt-br/empreendedores/fiscalizacao-economica-e-financeira). Dor: volume de envios e de prazos, qualidade dos dados, expurgos defensáveis e processos sancionadores longos.

**Petróleo, gás e combustíveis (ANP).** O envio mensal ao SIMP vence **no dia 15** (ou no primeiro dia útil seguinte), é devido **mesmo sem operação**, e o atraso gera multa com base na Lei 9.847/1999, mantida na Justiça em ao menos um caso; há transição do i-SIMP para o DPP. Fontes: [Manual i-SIMP refino](https://www.gov.br/anp/pt-br/assuntos/producao-de-derivados-de-petroleo-e-processamento-de-gas-natural/producao-de-derivados-de-petroleo-e-processamento-de-gas-natural/arquivos-refino/manual-i-simp-refino.pdf), [ANP apresentação 2025](https://www.gov.br/anp/pt-br/centrais-de-conteudo/apresentacoes-palestras/2025/arquivos/apresentacao_sdl_jornada-anp-brasilcom.pdf), [jurisprudência TRF2](https://www.vademecumprevidenciario.com.br/jurisprudencia/eme/854.1512.3941.1619). Dor: obrigações repetitivas e numerosas, multas «bobas» mas frequentes e mudança de sistema.

**Licenças ambientais (todas).** A Lei 15.190/2025, do licenciamento, muda prazos e modalidades ([Senado](https://legis.senado.leg.br/norma/41198421/publicacao/41198980)); as condicionantes da licença convivem com as condicionantes da outorga, e ninguém as vê juntas.

## 4. Avaliação
### 4.1 O que já temos e reaproveitamos
| Ativo atual | Uso no novo produto |
|---|---|
| Base de decisões (votos, falas, relator) de ANTT, ANTAQ, ANEEL, ANM e ANP | «Como a diretoria tratou descumprimentos parecidos»: multa mantida ou reduzida, caducidade, acordo |
| `pipeline/prazos.py` (prazos medianos por tipo de processo) | Previsão de quando um processo sancionador ou um reequilíbrio será decidido |
| `pipeline/alerta_pauta.py` + calendário/pautas | Alerta quando um processo do cliente ou um tema seu entra em pauta |
| `pipeline/notas_cliente.py` (condicionantes com prazo) | Já extrai «condicionante com prazo» das decisões: é o embrião do cadastro de obrigações |
| `pipeline/raio_x.py` + `clientes/<x>/processos.json` | Estrutura de dados do cliente fora do git, já com regra de sigilo |
| `pipeline/monitor_8blocos.py` | Molde de documento mensal: basta somar o bloco «obrigações e prazos» |
| `baixar_dou_mac.py`, `conferir_dou.py`, `dou_buscas.json` | Leitura do DOU já iniciada (hoje para mandatos) |
| Skills `dados-do-cliente`, `conformidade-entrega`, `contratos` (DPA LGPD) | Governança pronta |

### 4.2 O que falta
1. **Cadastro de obrigações** (`clientes/<x>/obrigacoes.json`): fonte (cláusula, resolução, licença), periodicidade, prazo, responsável, evidência, sanção prevista e status. Extração assistida por IA a partir do PDF do contrato ou da licença, **sempre revisada por analista**.
2. **Calendário de prazos** com recorrência (mensal, anual, «X dias após evento»), dias úteis e feriados, e saída em ICS/e-mail.
3. **Leitura de DOU e SEI**: DOU por termos (razão social, nº do contrato) usando o que já existe; SEI só com **pesquisa pública** ou documentos que o cliente envia (sem credencial do cliente no MVP).
4. **Biblioteca de obrigações-modelo por setor** (SIMP, envios do PRODIST, relatórios do arrendamento, PER da ANTT): ativo reaproveitável entre clientes, só com regra pública.
5. Painel simples (HTML/PDF mensal + alerta por e-mail). Sem SaaS no começo.

### 4.3 Esforço
| Bloco | Semanas (1 pessoa + Claude) |
|---|---|
| Esquema de obrigações + extração assistida + revisão | 1,5 |
| Calendário, recorrência e alertas | 1 |
| Ligação com prazos, pautas e decisões (bloco «risco e precedentes») | 1 |
| Monitor de DOU por cliente | 0,5–1 |
| Biblioteca-modelo do 1º setor (ex.: portos ou ANP) | 1 |
| **Total MVP** | **4–6 semanas** |
Custo recorrente: cerca de 4–10 h de analista por mês por cliente (revisar mudanças, conferir evidências).

### 4.4 Preço sugerido (R$)
- **Piloto pago (1–2 semanas, 3 obrigações ou processos reais):** R$ 15–25 mil, abatido do contrato anual se fechar em 60 dias.
- **Adicional ao pacote atual:** R$ 15 mil/mês (1 contrato, 1 agência, até ~50 obrigações); R$ 25–40 mil/mês (vários contratos ou 2–3 agências, licenças incluídas).
- **Implantação:** R$ 30–80 mil, uma vez (leitura dos contratos e montagem do cadastro).
- Racional: uma única multa evitada ou um prazo de reequilíbrio não perdido costuma valer mais que o ano; o produto fica abaixo de uma ferramenta GRC internacional mais implantação e é coerente com os pacotes atuais de dezenas de milhares por mês.

### 4.5 Riscos e mitigação
| Risco | Mitigação |
|---|---|
| **LGPD e sigilo** (contratos, autos de infração, dados pessoais de responsáveis) | Dados do cliente **nunca no repositório**: só em `clientes/` (fora do git), sob DPA; minimizar dados pessoais (cargo em vez de nome); apagar no fim do contrato (skill `dados-do-cliente`) |
| **Responsabilidade** por prazo perdido | Contrato: serviço de apoio, não substitui a área jurídica nem o responsável legal; teto de responsabilidade; cadastro validado pelo cliente; alertas com antecedência dupla |
| Erro de extração por IA | Revisão humana obrigatória e citação da cláusula ou página em cada obrigação |
| Virar «mais um GRC» | Vender o diferencial (obrigação + comportamento da diretoria + prazos medianos), não o calendário |
| Dependência de SEI e credenciais | MVP sem login no SEI; o cliente envia os documentos |
| Escala de serviço (horas de analista) | Biblioteca-modelo por setor; cobrar implantação |
| Conflito com escritórios parceiros | Posicionar como insumo para o jurídico, com canal de revenda |

## 5. Recomendação
**Vale fazer**, como módulo premium para clientes que já compram o monitoramento (venda cruzada barata) e como porta de entrada em concessionárias e arrendatários. Não vale construir SaaS GRC genérico.

**MVP (4–6 semanas):** um setor primeiro: **portos/ANTAQ** (contratos densos e norma em revisão) ou **ANP** (obrigações repetitivas, multa clara). Entregas: cadastro de 30–50 obrigações de um contrato real, calendário com alertas, monitor de DOU e um bloco novo no documento de 8 blocos, «Obrigações, prazos e como a diretoria pune casos parecidos».

**Como vender:**
1. Oferecer a quem já é cliente: «traga 3 obrigações ou processos que tiram seu sono».
2. **Piloto pago de 1–2 semanas:** mapear as 3 obrigações (fonte, prazo, evidência, sanção), mostrar 2–3 precedentes da diretoria por obrigação e o prazo mediano do processo correspondente; entregar o PDF e o calendário.
3. Reunião de resultado, seguida de proposta de **contrato anual** (implantação + mensalidade), com a ampliação para o contrato inteiro e as licenças.
4. Prova de valor: o número de prazos e de riscos encontrados que o cliente não tinha mapeado.

**Próximo passo interno:** definir o esquema `obrigacoes.json`, montar a biblioteca-modelo do SIMP/ANP (só dado público) como demonstração e testar a extração com um contrato de arrendamento **público** do site da ANTAQ.
