# Conhecimento do dono: como se aprofundar em regulação (ANTT, ANTAQ, ANM, ANEEL, ANP)

Objetivo: o dono precisa entender o que a base mostra (votos, vistas, relatorias) e defender cada entrega diante de diretor jurídico ou regulatório do cliente. Este roteiro junta leitura essencial, fontes novas para a base, formação, leitura semanal, revisão por advogado e um plano de 90 dias.

## 1. Leitura essencial (leis)
| Norma | Por que importa para o produto | Onde ler |
|---|---|---|
| Lei 13.848/2019 (Lei Geral das Agências) | decisão colegiada, reuniões públicas e gravadas (art. 8º), AIR (art. 6º), agenda regulatória (art. 21), consulta pública (art. 9º), mandatos e vacância, interinos (arts. 10 e 11 da Lei 9.986/2000, na redação dela) | https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2019/lei/l13848.htm |
| Lei 9.784/1999 (processo administrativo federal) | motivação (art. 50), recurso e reconsideração (arts. 56–65), prazos (arts. 24, 49, 59): é a base de `prazos.py` | https://www.planalto.gov.br/ccivil_03/leis/l9784.htm |
| LINDB (Decreto-Lei 4.657/1942), arts. 20–30 | consequências práticas da decisão (art. 20), regime de transição (art. 23), compromisso (art. 26), segurança jurídica e orientações gerais (art. 30): argumentos recorrentes em votos | https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm |
| Lei 9.427/1996 (ANEEL) | competências, diretoria, regime das decisões no setor elétrico | https://www.planalto.gov.br/ccivil_03/leis/l9427cons.htm |
| Lei 9.478/1997 (Lei do Petróleo / ANP) | competências da ANP, CNPE, outorgas e leilões | https://www.planalto.gov.br/ccivil_03/leis/l9478.htm |
| Lei 10.233/2001 (ANTT, ANTAQ, DNIT) | competências, diretoria, outorgas de transporte | https://www.planalto.gov.br/ccivil_03/leis/leis_2001/l10233.htm |
| Lei 12.815/2013 (portos) | arrendamento, TUP, reequilíbrio: tema central da ANTAQ | https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12815.htm |
| Lei 13.575/2017 (ANM) | criação da ANM, diretoria, competências minerárias | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2017/lei/l13575.htm |

**Regimentos internos (ler por agência, só os capítulos de deliberação):** quórum e votação (ordem de voto, voto de desempate do diretor-geral), **pedido de vista** (prazo e devolução), **sustentação oral** (inscrição e tempo), **sorteio/distribuição de relatoria**, deliberação por circuito ou eletrônica (sem vídeo, ponto cego da base) e sigilo. Procure no gov.br de cada agência por «Regimento Interno» (ANTT: Resolução do regimento vigente; ANEEL: Norma de Organização e Regimento Interno; ANP, ANTAQ, ANM: idem). Anote em `data/<ag>/config` as regras que mudam a leitura dos dados (ex.: prazo de vista, quem vota primeiro).

## 2. Fontes que enriquecem a base (ordem de retorno)
1. **Atas** das reuniões (gov.br): conferem resultado e relator; já há `cruzar_atas.py` e `ata_para_analise.py`.
2. **Votos escritos** (PDF por processo, comuns na ANEEL): dão a justificativa completa que a legenda corta.
3. **Acórdãos do TCU** sobre a agência (pesquisa de jurisprudência do TCU): mostram controle externo e temas sensíveis; agente `pesquisador-tcu`.
4. **AIR** (análises de impacto regulatório) e **consultas/audiências públicas**: antecipam a pauta e a posição técnica.
5. **Agenda regulatória** anual/bienal (art. 21 da Lei 13.848): o que deve ir a voto.
6. **DOU** (INLABS, no Mac): nomeações, deliberações, resoluções; fecha mandatos e prazos.
7. **Decisões judiciais** (TRF1, STJ) que suspendem ou anulam deliberações: risco do precedente.
Regra: tudo só de fonte pública, sem contornar CAPTCHA; dado de cliente fica em `clientes/`.

## 3. Formação (conferido por busca em 15/11/2026; confirmar turma, preço e datas no site)
- **FGV Direito SP (FGV LAW)**: pós lato sensu em Direito Administrativo (programa 2026) e curso de Direito e Relações Governamentais; não achei um curso com o nome «direito regulatório e infraestrutura» em 2026. https://direitosp.fgv.br/sites/default/files/cursos/arq-prog/2025-08/programa-2026-pos-graduacao-em-direito-administrativo.pdf · https://direitosp.fgv.br/sites/default/files/cursos/arq-prog/2025-10/programa-2026.1-direito-e-relacoes-governamentais-fgv-law_0.pdf
- **FGV Direito Rio**: Pós-graduação em Direito do Estado e da Regulação (divulgada em várias turmas). https://www.migalhas.com.br/agenda/157876/pos-graduacao-em-direito-do-estado-e-da-regulacao
- **IDP (Brasília)**: linha de regulação, grupo de pesquisa Better Regulation (infraestrutura) e disciplina «Temas em Regulação de Infraestrutura» no mestrado em Administração Pública. https://en.idp.edu.br/regulacao · https://wpcdn.idp.edu.br/idpsiteportal/2025/10/Edital_Better_Regulation_IDP_01-2025__2_.pdf · https://wpcdn.idp.edu.br/idpwpmestradoadm/sites/5/2020/07/Temas_em_Regulação_de_Infraestrutura_-_Plano_de_Ensino_v4.pdf
- **Insper**: LL.M.s de Direito (contratos; mercados financeiro e de capitais); não encontrei LL.M. específico de infraestrutura; conferir oferta. https://www.insper.edu.br/pt/cursos/pos-graduacao/direito/direito-dos-contratos
- **PUC-SP** (alternativa direta ao tema): Especialização em Direito e Infraestrutura. https://www.pucsp.br/pos-graduacao/especializacao-mba/direito-e-infraestrutura
- **Energia**: o **FGV CERI** (Centro de Estudos em Regulação e Infraestrutura) é centro de pesquisa, não oferece curso regular que eu tenha encontrado; use publicações e eventos dele (https://ceri.fgv.br/index.php/en/sobre). Para curso: **MBA no Setor Elétrico** (FGV Educação Executiva) https://educacao-executiva.fgv.br/produto/mba-no-setor-eletrico-01tV200000Je87EIAR e **MBA em Óleo, Gás e Transição Energética** https://educacao-executiva.fgv.br/produto/mba-em-oleo-gas-e-transicao-energetica-01tV200000JoRjeIAF
- Gratuito e curto: cursos de AIR da **ENAP** (ex.: modelagem de AIR) https://repositorio.enap.gov.br/bitstream/1/3453/1/Programa%20-%20Curso%20Modelagem%20AIR.pdf

Sugestão: um curso de extensão curto agora (ENAP + publicações CERI) e uma pós (FGV Rio, IDP ou PUC-SP) só se o volume de ANEEL/ANP justificar.

## 4. Leitura semanal (1 h por semana, sexta)
- **Agência iNFRA** (transportes, portos, energia; bastidores de diretoria) — https://www.agenciainfra.com
- **MegaWhat** (setor elétrico, ANEEL) — https://megawhat.energy
- **Canal Energia** (ANEEL, leilões, tarifas) — https://www.canalenergia.com.br
- **Portos e Navios** (ANTAQ, arrendamentos) — https://www.portosenavios.com.br
- **Brasil Energia** (petróleo, gás, energia) — https://brasilenergia.com.br
- **epbr** (ANP, gás, transição) — https://epbr.com.br
Rotina: anotar em 3 linhas cada notícia sobre diretor, vaga, pauta ou empresa-alvo; se citar diretor, conferir a fala na base (`consulta.py busca`) e usar como gancho de demo.

## 5. Advogado regulatório como revisor
- Papel: revisar amostra de cada entrega (terminologia, leitura jurídica da decisão, riscos de afirmação), não produzir conteúdo.
- Formato: 2 a 4 h por mês, pagamento por hora ou participação por cliente indicado; NDA e cláusula de conflito de interesse (não atuar contra cliente do produto com base nos relatórios).
- Entrada no fluxo: depois do `auditor-respostas` e antes da `conformidade-entrega`; em ANEEL/ANP, junto com o `revisor-energia`.
- Perfil: ex-procurador de agência ou advogado de escritório de infraestrutura/energia; idealmente um para transportes e outro para energia.

## 6. Plano de 90 dias
| Semanas | Foco | Pronto quando |
|---|---|---|
| 1–2 | Lei 13.848 inteira, Lei 9.784 (motivação, recursos, prazos), LINDB 20–30 | resumo de 1 página de cada no caderno do dono |
| 3–4 | Regimentos da ANTT e ANTAQ (votação, vista, sustentação, sorteio); Leis 10.233 e 12.815 | consigo explicar por que um item teve vista e o prazo de devolução |
| 5–6 | Lei 9.427 e regimento da ANEEL; vocabulário de energia (skill `nova-agencia-energia`) | leio uma pauta de RPO e classifico os itens por tema |
| 7–8 | Lei 9.478, regimento da ANP; Lei 13.575 (ANM) | idem para RD da ANP |
| 9–10 | Fontes novas: 10 acórdãos TCU (`pesquisador-tcu`), 1 AIR, agenda regulatória de 2 agências | 1 seção nova num relatório usando essas fontes |
| 11–12 | Fechar parceria com advogado revisor; inscrever-se em 1 curso | revisor revisou 1 entrega real |
| 13 | Revisão: o que mudou nos produtos | `catalogo_entregas.md` atualizado |
Leitura semanal (seção 4) corre em paralelo durante os 90 dias.
