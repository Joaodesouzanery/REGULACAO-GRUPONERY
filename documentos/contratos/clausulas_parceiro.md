# Contrato de Licença de Entregas e Revenda (Grupo Nery × Parceiro Revendedor) — MODELO

> **MODELO PARA REVISÃO POR ADVOGADO.** Este texto não é aconselhamento jurídico. É uma minuta-base que precisa ser revisada e ajustada por um advogado habilitado antes de qualquer uso. Campos entre `{{ }}` são preenchidos a partir de `clientes/<x>/contrato.json` (skill `contratos`). Bases legais conferidas em 14/11/2026; o agente `pesquisador-juridico` as atualiza.

**LICENCIANTE:** {{licenciante.razao_social}} («GRUPO NERY»), CNPJ {{licenciante.cnpj}}.
**PARCEIRO:** {{parceiro.razao_social}} («PARCEIRO»), CNPJ {{parceiro.cnpj}}, representado por {{parceiro.representante}}.

## Cláusula 1 — Objeto
1.1. Licença **não exclusiva** (salvo a Cláusula 3.6), intransferível e onerosa para o PARCEIRO **revender e entregar a clientes finais as ENTREGAS** produzidas pelo GRUPO NERY: (A) relatório temático com quadro da diretoria; (B) relatório da empresa; (C) boletim mensal da agência; (D) alerta pré-pauta, casos semelhantes, raio-X de prazo e perguntas sob demanda, conforme o Anexo I (planos e preços).
1.2. **ENTREGAS** são os arquivos finais (PDF, e CSV/planilha quando previsto). **Não fazem parte do objeto** e ficam com o GRUPO NERY: o motor, código-fonte e objeto, scripts, prompts, skills e agentes, base de dados (transcrições, votos estruturados, índices), metodologia, critérios de classificação e de conferência, modelos de previsão e documentação interna (em conjunto, «MOTOR»).
1.3. É vedado ao PARCEIRO, direta ou indiretamente: (a) fazer engenharia reversa, descompilar ou tentar reconstruir o MOTOR ou a base a partir das ENTREGAS (por exemplo, por extração sistemática, raspagem ou agregação de várias entregas para recompor a base); (b) sublicenciar o MOTOR; (c) usar as ENTREGAS para treinar ou alimentar sistemas concorrentes. Fundamento: Lei 9.609/1998, arts. 2º e 9º; Lei 9.610/1998, art. 7º, XIII, e arts. 29 e 87 (bases de dados).

## Cláusula 2 — Revenda white label
2.1. O PARCEIRO vende com a marca própria. Toda ENTREGA leva a marca do PARCEIRO e a menção «tecnologia Grupo Nery» ou «em parceria com Grupo Nery», em local visível (capa ou rodapé). O PARCEIRO não pode remover essa menção.
2.2. O PARCEIRO é o único responsável pela relação comercial com o cliente final e repassa a ele, no mínimo, os termos de `clausulas_cliente_final.md`.
2.3. **Preço mínimo de revenda:** o PARCEIRO não pode vender abaixo da tabela do Anexo I (preço de fundador ou tabela cheia, conforme o caso) sem autorização escrita do GRUPO NERY. *(Nota ao advogado: avaliar o preço mínimo de revenda à luz da Lei 12.529/2011, art. 36, §3º, IX; se necessário, trocar por preço sugerido e repasse mínimo fixo por cliente.)*

## Cláusula 3 — Divisão de receita, não concorrência e metas
3.1. A receita líquida de cada contrato com cliente final é dividida **50% GRUPO NERY / 50% PARCEIRO**. Receita líquida = valor faturado menos os tributos incidentes sobre o faturamento, conforme o Anexo II.
3.2. **Não concorrência:** durante a vigência e por {{nao_concorrencia_meses|12}} meses depois, o PARCEIRO não desenvolverá, contratará nem revenderá produto substancialmente igual (perfis de votos de diretores de agências reguladoras a partir de reuniões públicas) concorrente das ENTREGAS, no território do Brasil. *(Nota ao advogado: limite razoável de tempo, objeto e território.)*
3.3. **Não aliciamento:** pelo mesmo prazo, nenhuma das partes aliciará empregados ou colaboradores da outra, nem abordará diretamente os clientes finais trazidos pela outra para vender o mesmo serviço sem ela.
3.4. O GRUPO NERY pode atender clientes diretamente ou por outros parceiros, exceto nos casos de exclusividade (3.6) e nos clientes registrados pelo PARCEIRO (3.5).
3.5. **Registro de oportunidade:** cliente registrado por escrito pelo PARCEIRO fica reservado a ele por {{registro_dias|90}} dias.
3.6. **Exclusividade (opcional):** {{exclusividade.ativa}}. Se ativa, vale para {{exclusividade.escopo}} (setor/agência/território) e depende de meta mínima de {{exclusividade.meta_clientes}} clientes ativos ou R$ {{exclusividade.meta_receita}}/mês em até {{exclusividade.prazo_meses}} meses; se não atingida, a exclusividade cai automaticamente, sem multa.

## Cláusula 4 — Remuneração e faturamento
4.1. **Quem fatura:** {{faturamento.quem|o PARCEIRO}} emite a nota fiscal ao cliente final. A outra parte emite NF de serviço contra quem faturou pelo seu percentual.
4.2. **Repasse:** até {{repasse_dias|10}} dias corridos após o recebimento do cliente, com relatório de recebimentos. Sem recebimento do cliente, não há repasse, salvo culpa de quem faturou na cobrança.
4.3. **Reajuste:** anual pelo IPCA/IBGE, na data de aniversário (Lei 10.192/2001, art. 2º, §1º — periodicidade mínima anual).
4.4. **Inadimplência entre as partes:** multa de 2%, juros de 1% ao mês pro rata e correção pelo IPCA; atraso superior a 30 dias permite suspender as entregas do cliente correspondente após aviso de 5 dias úteis (CC, arts. 395, 406 e 476).
4.5. **Preço de fundador:** os {{fundador.qtd|2}} primeiros clientes finais têm o preço de fundador por 12 meses a contar da primeira entrega; depois passam à tabela cheia vigente, com aviso de 60 dias ao cliente.

## Cláusula 5 — Propriedade intelectual
5.1. O MOTOR é propriedade do GRUPO NERY, protegido pela Lei 9.609/1998 (software) e pela Lei 9.610/1998 (obras e bases de dados — art. 7º, XIII). Nenhum direito sobre ele é cedido.
5.2. As ENTREGAS são obras do GRUPO NERY licenciadas para uso interno do cliente final; os trechos literais de reuniões públicas e os documentos oficiais citados permanecem de domínio público ou de seus titulares (Lei 9.610/1998, art. 8º, IV, e art. 46, III — citação para fins de estudo/crítica).
5.3. Marcas: cada parte mantém a sua; o uso cruzado é limitado ao previsto na Cláusula 2.1.
5.4. Melhorias sugeridas pelo PARCEIRO e incorporadas ao MOTOR passam a integrar o MOTOR, sem remuneração adicional.

## Cláusula 6 — Fontes públicas e limites declarados
6.1. As ENTREGAS usam apenas fontes públicas: vídeos das reuniões nos canais oficiais das agências no YouTube, pautas, atas e calendários no gov.br, Diário Oficial da União e Senado Federal, além de informações que o próprio cliente fornecer (sempre identificadas como tal).
6.2. O PARCEIRO declara ciência dos limites, que repassará ao cliente: (a) a legenda do YouTube é automática e pode errar nomes, números e valores; (b) itens sigilosos e votos escritos completos (SEI) não estão cobertos; (c) reuniões virtuais ou deliberações sem vídeo público não estão cobertas; (d) o minuto de quem só «acompanha o relator» é aproximado; (e) a conferência por amostra cega mede **consistência**, não verdade absoluta. A taxa vigente (hoje cerca de 92–96% conforme agência e ano) é informada em cada ENTREGA.

## Cláusula 7 — Natureza das previsões e limitação de responsabilidade
7.1. Previsões de voto, placares, prazos e tendências são **estimativas estatísticas (inferência)** baseadas no histórico público. Não substituem intimação, publicação oficial, leitura dos autos nem orientação jurídica.
7.2. O GRUPO NERY não responde por decisões de negócio, jurídicas ou processuais tomadas pelo PARCEIRO ou pelo cliente com base nas ENTREGAS.
7.3. **Teto:** a responsabilidade total do GRUPO NERY, por qualquer causa, limita-se ao valor efetivamente recebido por ele do contrato em questão nos **12 meses** anteriores ao fato. Excluem-se lucros cessantes e danos indiretos. Não se aplica a dolo ou culpa grave (CC, arts. 402, 403 e 944; para B2B, princípio da autonomia — CC, art. 421-A).

## Cláusula 8 — Integridade e anticorrupção
8.1. As partes usarão **somente informação pública** e nunca buscarão, comprarão nem usarão informação não pública de agentes públicos, servidores ou autos sigilosos.
8.2. É vedado oferecer, prometer ou dar vantagem a agente público (Lei 12.846/2013, art. 5º) e induzir agente público a usar informação privilegiada ou a atuar em conflito de interesses (Lei 12.813/2013, arts. 5º e 6º).
8.3. As ENTREGAS não contêm juízo pessoal sobre diretores; padrões de voto são apresentados como contagens e inferências.
8.4. Violação desta cláusula é causa de rescisão imediata, sem multa para a parte inocente.

## Cláusula 9 — Proteção de dados (LGPD)
9.1. Aplica-se o `dpa_lgpd.md` (Anexo III), parte integrante deste contrato. Base: Lei 13.709/2018.

## Cláusula 10 — Confidencialidade
10.1. Informação confidencial: dados do cliente final, preços negociados, o MOTOR e a metodologia. Dever de sigilo durante a vigência e por **5 anos** após o término. Exceções: informação pública, já conhecida, recebida legitimamente de terceiros ou exigida por ordem legal (com aviso prévio, quando permitido).

## Cláusula 11 — Níveis de serviço (SLA)
11.1. Boletim mensal: até o **dia 5** do mês seguinte (dia útil seguinte se cair em fim de semana ou feriado).
11.2. Alerta pré-pauta: até **24 horas antes** da reunião, **quando a pauta for publicada** com antecedência suficiente pela agência; pauta publicada com menos de 48 h → melhor esforço.
11.3. Perguntas sob demanda: até {{perguntas_mes}} perguntas/mês conforme o plano, resposta em até {{prazo_resposta_dias_uteis|5}} dias úteis. Perguntas não usadas não acumulam.
11.4. Dependências: o SLA não se aplica quando a agência não publicar vídeo, pauta ou legenda, ou quando o YouTube bloquear a coleta; o GRUPO NERY avisa e entrega assim que possível.
11.5. Descumprimento reiterado (3 atrasos em 6 meses por culpa do GRUPO NERY) dá ao PARCEIRO desconto de 10% no mês seguinte ou rescisão sem multa.

## Cláusula 12 — Vigência, renovação e término
12.1. Vigência de **12 meses**, renovação automática por iguais períodos, salvo aviso escrito com **{{aviso_dias|60}} dias** (mínimo 30) de antecedência.
12.2. Rescisão antecipada imotivada: multa de {{multa_meses|3}} mensalidades médias ou o saldo, o que for menor (CC, arts. 412 e 413).
12.3. Rescisão motivada: descumprimento não sanado em 15 dias após notificação; Cláusula 8; recuperação judicial ou falência.
12.4. **Efeitos:** (a) contratos de clientes vigentes podem ser concluídos até o fim do ciclo pago, mantida a divisão; (b) o PARCEIRO e o cliente ficam com o histórico das ENTREGAS já pagas (PDF/CSV); (c) devolução ou eliminação de dados conforme o DPA; (d) sobrevivem as cláusulas 1.3, 3.2–3.3, 5, 7, 8, 10 e 13.

## Cláusula 13 — Divulgação e uso de marca
13.1. Nenhuma parte usará a marca, o nome ou o caso de um **cliente final** em divulgação (site, redes sociais, apresentações, propostas) **sem autorização prévia e escrita** do cliente, que define o que pode ser dito. Versões anônimas não podem permitir identificação.
13.2. Conteúdo confidencial (previsões específicas, estratégia, números do cliente) nunca é divulgado, mesmo com autorização genérica.

## Cláusula 14 — Lei, mediação e foro
14.1. Lei brasileira.
14.2. Antes de ação judicial, as partes tentarão **mediação** por até 60 dias (Lei 13.140/2015), em câmara escolhida de comum acordo.
14.3. Foro de {{foro|comarca da sede do GRUPO NERY}} (CPC, art. 63). *(Alternativa: arbitragem — Lei 9.307/1996.)*
14.4. Assinatura eletrônica válida (MP 2.200-2/2001; Lei 14.063/2020).

**Anexos:** I — Planos e preços (fundador × tabela cheia); II — Cálculo da receita líquida e repasse; III — DPA LGPD; IV — Termos do cliente final.
