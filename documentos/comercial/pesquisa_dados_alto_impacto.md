# Fontes de dados públicas adicionais — estudo de impacto para o Grupo Nery

**Objetivo:** mapear fontes públicas que, cruzadas com a base já existente de decisões de diretoria (votos por diretor, falas com minuto, relatores, prazos), ampliam o que a consultoria consegue responder sobre ANTT, ANTAQ, ANEEL, ANP e ANM — e avaliar prioridade para produto e para prospecção.

**Método desta pesquisa:** cada fonte foi buscada e, sempre que o host permitiu acesso nesta sessão, a página foi aberta para confirmar que existe (não apenas indicada por busca). Datas e números de terceiros aqui citados são de buscas feitas em 18/11/2026 e estão marcados como **não conferido** quando não puderam ser abertos e lidos na própria fonte.

---

## 1. Portal da Transparência / Comprasnet (CGU)

- **O quê:** API REST e arquivos abertos de contratos, convênios, sanções (CEIS, CNEP, CEPIM), viagens a serviço e, no Comprasnet/Portal de Compras, licitações e contratos da administração federal.
- **De quem:** Controladoria-Geral da União (CGU); Comprasnet é do Ministério da Gestão.
- **Confirmado:** `portaldatransparencia.gov.br/api-de-dados` respondeu (redirecionamento 302, página existe); `gov.br/compras` tem documentação interativa da API de dados abertos.
- **Formato/atualização:** API REST com paginação; dados também em CSV. Atualização contínua para a maior parte das bases.
- **Licença:** dado público, uso livre com atribuição à fonte.
- **O que passa a responder:** se um diretor (ou empresa que ele/ela regulou) aparece em listas de sanções (CEIS/CNEP), se uma empresa teve contratos/convênios com a União no período em que um processo da agência estava em pauta — cruzamento útil para due diligence de contraparte, não para o diretor em si (diretores de agência não são fornecedores).
- **Prioridade:** **média**. Útil para relatórios de empresa (checar se a empresa regulada tem sanções/contratos federais), pouco relevante para o perfil do diretor.
- **Esforço:** 1–2 semanas (API simples, mas exige CNPJ correto da empresa para consulta).

## 2. CVM — fatos relevantes e dados de companhias abertas

- **O quê:** Portal de Dados Abertos da CVM (`dados.cvm.gov.br`), com inventário de bases incluindo fatos relevantes, comunicados ao mercado, demonstrações financeiras (DFP/ITR) e valores mobiliários negociados/detidos por companhias abertas.
- **De quem:** Comissão de Valores Mobiliários.
- **Confirmado:** `dados.cvm.gov.br` respondeu (HTTP 200); inventário de bases (`InventarioBasesCVM.pdf`) lista fatos relevantes entre os conjuntos publicados.
- **Formato/atualização:** CSV/ZIP por ano, baixável; fatos relevantes também disponíveis via sistema de consulta individual por empresa. Atualização é tipicamente diária/por evento para fatos relevantes, anual para os arquivos consolidados.
- **Licença:** dado público (Lei de Acesso à Informação).
- **O que passa a responder:** se uma decisão de diretoria (ex.: reequilíbrio de concessão, outorga, multa) foi comunicada ao mercado como fato relevante pela empresa afetada — e em que termos a empresa descreveu o risco regulatório antes/depois da decisão. Isso permite cruzar "o que a diretoria decidiu" com "o que a empresa disse aos investidores sobre isso", um ângulo que hoje não existe na base.
- **Prioridade:** **alta** — é o cruzamento mais direto entre decisão regulatória e repercussão de mercado, interessa a investidores e à própria empresa regulada.
- **Esforço:** 2–3 semanas (requer parsing dos ZIPs anuais + busca textual por nome da agência/processo nos fatos relevantes).

## 3. Receita Federal — dados abertos de CNPJ

- **O quê:** Base completa de CNPJ (empresas, estabelecimentos, sócios, simples nacional, natureza jurídica) para todo o país, atualizada mensalmente.
- **De quem:** Receita Federal do Brasil.
- **Confirmado por busca (não abri a página nesta sessão: a conexão foi interrompida pelo provedor de rede ao tentar `dadosabertos.rfb.gov.br`):** a existência e a estrutura mensal dos arquivos (Empresas, Estabelecimentos, Sócios, em CSV separado por `;`) são amplamente documentadas por terceiros e por repositórios técnicos que replicam o layout oficial da Receita. **Não conferido** diretamente nesta sessão — recomenda-se reabrir a verificação quando o host estiver acessível.
- **Formato/atualização:** CSV em ZIP, mensal.
- **Licença:** dado público.
- **O que passa a responder:** grupo econômico real por trás de uma empresa que aparece em processos de uma agência — mesmos sócios, mesma controladora, holdings e empresas-irmãs. Hoje a base de decisões identifica a empresa pelo nome usado na ata; cruzar com CNPJ permite saber se duas empresas que parecem independentes nas reuniões pertencem ao mesmo grupo, o que muda a leitura de "quantas vezes a diretoria decidiu a favor desse grupo".
- **Prioridade:** **alta** — é a peça que destrava a leitura "por grupo econômico" em vez de "por razão social", que é uma pergunta natural de cliente (holding, fundo, escritório).
- **Esforço:** 3–4 semanas (volume grande de dados; precisa de banco local e lógica de nome fantasia × razão social para casar com os nomes citados nas atas).

## 4. Consultas e Audiências Públicas de cada agência

- **O quê:** Sistemas de participação social de cada agência — ANTT (ParticipANTT, portal `participantt.antt.gov.br`), ANTAQ, ANEEL e ANP têm páginas próprias de audiências e consultas públicas, com minutas, contribuições recebidas e, em alguns casos, relatório de análise de contribuições.
- **Confirmado:** páginas institucionais da ANTT (manual do ParticipANTT) e da ANTAQ (seção "Participação Social") existem; a Resolução ANTT 6.020/2023 formaliza os ritos de audiência x consulta pública.
- **Formato/atualização:** a maioria é PDF/HTML por processo, sem API; atualização por evento (cada consulta aberta gera seus próprios arquivos).
- **Licença:** documento público.
- **O que passa a responder:** quem contribuiu (empresas, associações, escritórios) em cada consulta pública que antecedeu uma norma ou decisão, e o que foi efetivamente acatado no relatório de análise de contribuições — ou seja, se o lobby de uma empresa específica teve efeito no texto final. Isso é um ângulo totalmente novo: hoje a base cobre a decisão colegiada, não o processo normativo que a precede.
- **Prioridade:** **alta** para ANEEL e ANP (consultas de tarifa/preço têm grande repercussão de cliente); **média** para ANTT/ANTAQ/ANM.
- **Esforço:** 4–6 semanas por agência — não há API, exige raspagem página a página e leitura humana dos relatórios de contribuição (processo manual, sem atalho).

## 5. BNDES — dados abertos de financiamento

- **O quê:** Portal `dadosabertos.bndes.gov.br` (CKAN) com datasets de operações contratadas, aprovações e desembolsos do Sistema BNDES desde 1995/2002, por cliente, setor (CNAE), UF, município e produto.
- **Confirmado:** `dadosabertos.bndes.gov.br/dataset/` respondeu (HTTP 200); dicionários de dados de "Aprovações" e "Desembolsos" no Sistema BNDES existem e detalham os campos (objetivo do projeto, status da operação, fase de aprovação).
- **Formato/atualização:** CSV via portal CKAN (interface padrão de API de catálogo), mensal para desembolsos.
- **Licença:** dado público.
- **O que passa a responder:** se uma empresa com processo relevante numa agência recebeu financiamento do BNDES para o mesmo projeto/ativo — por exemplo, uma concessão de rodovia ou um terminal portuário com obra financiada pelo banco. Permite perguntar "esse ativo tem dinheiro público na ponta do financiamento, além da regulação?", algo que hoje não é respondido.
- **Prioridade:** **média** — forte para ANTT (concessões) e ANTAQ (arrendamentos portuários), mais fraca para ANP/ANEEL/ANM, onde o financiamento é mais disperso.
- **Esforço:** 2 semanas (dataset estruturado, mas o nome do cliente no BNDES pode não casar exatamente com o nome citado nas atas — mesma dependência do cruzamento de CNPJ do item 3).

## 6. Indicadores setoriais oficiais

| Agência | Indicador | Fonte | Confirmado | Prioridade |
|---|---|---|---|---|
| ANTT | Movimentação rodoviária (RNTRC, pedágio, frota) | páginas de dados abertos da ANTT em gov.br/antt | página institucional existe (gov.br respondeu) | média |
| ANTAQ | Movimentação portuária (Estatístico Aquaviário) | `ea.antaq.gov.br` / `web3.antaq.gov.br` | host `ea.antaq.gov.br` respondeu (403 — exige navegação pela interface, não acesso direto); existência confirmada por boletins trimestrais oficiais em PDF | **alta** |
| ANEEL | DEC/FEC, perdas, consumo (PRODIST) | `gov.br/aneel` — seções de indicadores de qualidade e dados abertos | página gov.br/aneel respondeu (HTTP 200); existência da obrigação de publicar DEC/FEC por distribuidora é normativa (PRODIST, REN 956/2021) | **alta** |
| ANP | Produção por poço/campo (CDP), vendas de derivados (SIMP) | `cdp.anp.gov.br`; dados abertos em gov.br/anp | `cdp.anp.gov.br` respondeu (redirecionamento); metadados do SIMP confirmam periodicidade mensal | **alta** |
| ANM | Produção mineral (SIGMINE/AAMM) | gov.br/anm | não verificado nesta pesquisa | média |

- **O que passa a responder:** se uma decisão de diretoria (reequilíbrio, outorga, sanção) coincide no tempo com uma mudança relevante no indicador operacional do ativo afetado (queda de movimentação, aumento de DEC/FEC, queda de produção) — dá contexto objetivo ("a empresa pediu reequilíbrio num trimestre em que o indicador X caiu Y%") que hoje falta nas respostas, que são só sobre o voto.
- **Esforço:** 3–4 semanas por agência (cada fonte tem formato e granularidade diferentes; ANEEL e ANP são as mais estruturadas e valem o investimento primeiro).

## 7. Tribunais Regionais Federais (TRFs) — jurisprudência sobre decisões das agências

- **O quê:** acórdãos dos 6 TRFs sobre ações que questionam multas, outorgas e decisões das agências (hoje a base já cobre TCU e STJ).
- **Confirmado por busca:** jurisprudência localizada para a ANTT (TRF1, TRF3, TRF4) sobre validade de multas e competência sancionadora; não foram localizadas decisões específicas de ANEEL/ANP/ANTAQ/ANM nesta rodada de busca — **não conferido** que exista volume comparável para essas agências, exigiria busca dedicada por agência.
- **Formato/atualização:** acórdãos em PDF/HTML nos sites de cada TRF, sem API unificada; agregadores privados (ex.: bases de jurisprudência pagas) indexam por ementa.
- **Licença:** decisão judicial é pública; agregadores privados têm seus próprios termos.
- **O que passa a responder:** se as sanções/decisões de um diretor específico (ou de uma diretoria num tema) tendem a ser mantidas ou anuladas no Judiciário — hoje a base só mostra o que a diretoria decidiu, não o desfecho judicial daquela decisão.
- **Prioridade:** **média** — soma valor ao que já existe (TCU/STJ), mas tem baixa cobertura por decisão individual (a maioria das multas de transporte de carga, por exemplo, não chega a gerar acórdão citável).
- **Esforço:** 4–6 semanas por agência (pesquisa manual nos 6 TRFs, sem padronização de busca).

## 8. Imprensa especializada como sinal de repercussão

- **O quê:** veículos setoriais — eixos (ex-epbr, energia e petróleo), Agência Infra (infraestrutura/transporte/portos), JOTA (direito e regulação, inclusive judicialização de decisões de agências), Canal Energia, Monitor Mercantil (portos).
- **Confirmado:** `agenciainfra.com`, `www.canalenergia.com.br` e `canalsolar.com.br` já estão na rede permitida da sessão (ou seja, já em uso); `www.jota.info` respondeu (HTTP 200) nesta verificação.
- **Formato/atualização:** sites de notícia, sem API pública; a maioria tem paywall parcial (JOTA é majoritariamente pago).
- **Licença:** conteúdo protegido por direito de autor — pode-se citar trecho curto com link e crédito, não reproduzir a matéria.
- **O que passa a responder:** se uma decisão específica (voto, multa, outorga) teve repercussão na imprensa especializada no mesmo período — um sinal indireto de relevância do caso, sem substituir a transcrição da reunião como fonte primária.
- **Prioridade:** **baixa/média** — é sinal complementar, não gera resposta nova por si, e o acesso pago ao JOTA limita o quanto pode ser usado de forma sistemática.
- **Esforço:** 1 semana para um levantamento manual pontual; integração contínua exigiria assinatura paga e não é prioridade agora.

---

## Ranking consolidado por impacto × esforço

| Fonte | Prioridade | Esforço | Por quê primeiro/depois |
|---|---|---|---|
| CVM — fatos relevantes | **Alta** | 2–3 sem. | Liga decisão regulatória a comunicação ao mercado; interessa a investidores e à própria empresa. |
| Indicadores setoriais ANEEL/ANP (DEC-FEC, produção) | **Alta** | 3–4 sem./agência | Dá contexto objetivo à decisão; ANEEL e ANP são os setores de maior porta comercial hoje. |
| Receita Federal (CNPJ/grupo econômico) | **Alta** | 3–4 sem. | Pré-requisito técnico para vários outros cruzamentos (BNDES, CVM, sanções) funcionarem por grupo, não por razão social. |
| Consultas/audiências públicas (quem contribuiu, o que foi acatado) | **Alta** (ANEEL/ANP) / **Média** (demais) | 4–6 sem./agência | Abre a fase normativa, hoje não coberta; mas é trabalho manual, sem API. |
| ANTAQ — Estatístico Aquaviário | **Alta** | 3–4 sem. | Setor com boa base pública e cliente concentrado em poucos grandes operadores. |
| BNDES — dados abertos | **Média** | 2 sem. | Fácil de integrar, mas relevante só para alguns setores (concessões, portos). |
| Portal da Transparência/Comprasnet | **Média** | 1–2 sem. | Mais útil para due diligence de empresa do que para o perfil do diretor. |
| TRFs — jurisprudência | **Média** | 4–6 sem./agência | Soma ao que já existe (TCU/STJ), mas cobertura desigual entre agências. |
| Imprensa especializada | **Baixa/Média** | 1 sem. (pontual) | Sinal complementar; JOTA tem paywall, limita uso sistemático. |

## Ressalvas gerais

- Todo número de terceiros citado aqui (percentuais, volumes, datas de atualização) está marcado como **não conferido** quando não foi lido diretamente na fonte primária nesta pesquisa; antes de usar em material de cliente, abrir a página oficial e confirmar.
- Nenhuma destas fontes substitui a transcrição da reunião como evidência de voto — todas são complementares e devem ser citadas com seu próprio link, nunca misturadas ao trecho literal da ata.
- Receita Federal (item 3) não pôde ser aberta diretamente nesta sessão (a conexão foi interrompida pelo provedor de rede); a existência e o formato descritos vêm de fontes secundárias e devem ser reconfirmados na própria página antes de qualquer integração.
