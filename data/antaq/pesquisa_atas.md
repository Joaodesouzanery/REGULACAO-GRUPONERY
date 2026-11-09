# ANTAQ: onde estão as pautas, atas e deliberações da Diretoria Colegiada

Pesquisa de 09/11/2026. Fontes abertas com curl a partir da nuvem: gov.br/antaq, Senado e DOU. Ficaram bloqueados pelo proxy da sessão: sophia.antaq.gov.br, agenciainfra.com, atribuna.com.br e legismap.com.br.

## 1. Composição e regras
- Até dez/2022 a Diretoria tinha 3 membros (DG + 2 diretores). A partir de 14/12/2022 passou a ter 5 (DG + 4 diretores), pelo Decreto 11.284/2022, e os novos diretores tomaram posse em 14/12/2022.
- Os mandatos são de 5 anos, sem recondução (Lei 13.848/2019). Antes, pela Lei 10.233, eram de 4 anos, com fim fixo em 18 de fevereiro.
- Os substitutos saem de uma lista enviada pela agência e decretada pelo Presidente; a última é o decreto de 30/01/2025 (DOU 31/01/2025). Cada substituição vale por até 180 dias.
- Os mandatos estão em `data/antaq/mandatos.json` (17 registros: 12 mandatos titulares de 9 pessoas e 5 substitutos).

## 2. Onde está cada coisa
| O quê | URL |
|---|---|
| Página-mãe das Reuniões da Diretoria | https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas |
| Calendário, últimas pautas e últimas atas | https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes |
| Pautas e atas anteriores (acervo) | http://sophia.antaq.gov.br/terminal/Busca/legislacao (biblioteca Sophia; cada ata tem uma ficha `sophia.antaq.gov.br/Terminal/acervo/detalhe/<id>`, p.ex. 43052 = ata da ROD 620). **Bloqueado daqui**: precisa liberar o host ou baixar pelo Mac |
| Resultado das reuniões virtuais (voto do relator + posição de cada diretor) | https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes/resultado-das-reunioes-virtuais-da-diretoria-1 (traz links para a pesquisa pública do SEI: `sei.antaq.gov.br/sei/modulos/pesquisa/md_pesq_processo_exibir.php?...` com relatórios e votos) |
| Distribuição (sorteio) de processos por diretor | https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/distribuicao-de-processos (XLS semanal desde 2023; PDFs de 2020–2022, mas muitos links antigos dão NotFound) |
| Sustentação oral | .../reunioes-deliberativas/sustentacao-oral |
| Vídeo das ROD (YouTube) | https://youtube.com/c/CanalANTAQ e a playlist https://www.youtube.com/playlist?list=PLUx7SBS9VtlAfMS5T9FLHDhflAn-bF7C- |
| Diretoria atual / ex-diretores | .../institucional/diretoria-colegiada e .../diretoria-colegiada/ex-diretores |

**URLs dos PDFs.** As últimas pautas e atas ficam em `.../reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes/<Arquivo>.pdf`. O Google costuma indexar o caminho sem `calendario-atas-e-pautas-das-reunioes/`, e esse caminho devolve `{"error_type":"NotFound"}`: é preciso acrescentar o subdiretório. Os nomes dos arquivos não seguem padrão: `AtaROD615.pdf`, `copy_of_AtaROD613.pdf`, `copy_of_Ata506ROD.pdf`, `PautadaROD616_vs4.pdf`, `Pautade33RED.pdf`, `copy9_of_document.send.pdf`. Por isso não dá para gerar as URLs; é preciso raspar as páginas ou o Sophia.

## 3. Tipos de reunião e formato
- **ROD (Reunião Ordinária de Diretoria)**: numeração contínua. Exemplos: 506ª em 11/08/2021, 597ª em out/2025, 622ª em nov/2026. Pode ser:
  - **telepresencial/presencial**, transmitida no YouTube;
  - **virtual via SEI**, com cerca de 48–72 h para cada diretor votar eletronicamente. A Resolução ANTAQ nº 66 rege as virtuais, que existem desde 2020/2021.
- **RED (Reunião Extraordinária de Diretoria)**: numeração própria. A 33ª foi em 25/06/2025.
- **Pauta (PDF)**: lista os processos por relator, com nº SEI, interessados e assunto. A página de resultados das virtuais traz Tipo, Interessados, Contextualização e Resultado (Deliberado / Retirado de pauta).
- **Ata (PDF assinado no SEI)** traz:
  - abertura, com quem presidiu, diretores e substitutos presentes, Secretário-Geral e Procurador-Chefe;
  - processos retirados de pauta, por relator;
  - **pedidos de vista**, nominais: "objeto de pedido de vista formulado pelo Diretor X";
  - acórdãos aprovados, transcritos na íntegra.
- **Estrutura de cada acórdão:**
  1. Processo
  2. Interessados
  3. Relator
  4. Unidade técnica
  5. Acórdão ("VISTOS… que tratam de…", "ACORDAM os Diretores… em: 5.1…")
  6. Data e modalidade
  7. Quórum: **7.1 Diretores presentes (Presidente, Relator); 7.2 Diretor(a) com voto vencido: Nome**. Atas antigas usam a forma "Revisor" (ex.: "Vencido o 1º Revisor, Diretor Francisval Mendes").
- **Voto nominal: sim, em parte.** A ata nomeia relator, presidente, presentes, quem pediu vista e quem ficou **vencido**. Quando não aparece 7.2, a decisão foi unânime entre os presentes. A fundamentação de cada voto não vem na ata; está no SEI (relatório/voto) e no vídeo. Atas de 2021 também registram revisores e quem teve a proposta "vencedora".

## 4. Exemplos reais de ata (baixados e lidos)
1. **ROD 615, 03 a 05/08/2026 (virtual)**: https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes/AtaROD615.pdf
   - Presidida por Frederico Dias, com Lima Filho, Alber Vasconcelos, Caio Farias e a Diretora-Substituta Cristina Castro.
   - Acórdãos 440 a 475/2026.
   - Temas: referendo de Deliberação-DG, sobre-estadia de contêineres (denúncias Grancafe e Maersk), reajuste tarifário de Porto Velho, Sandbox, TAC, auto de infração.
2. **ROD 597, 20 a 22/10/2025 (virtual)**: .../calendario-atas-e-pautas-das-reunioes/AtaROD597.pdf
   - Composição completa: Frederico Dias, Flávia Takafashi, Lima Filho, Alber Vasconcelos e Caio Farias.
   - 39 acórdãos (nº 700+/2025).
   - Pedido de vista de Alber Vasconcelos em processo relatado por Flávia Takafashi.
   - **2 acórdãos com "Diretora com voto vencido: Flávia Takafashi"**, um deles sobre o contrato Vports–Peiú e a cobrança de tarifas portuárias.
3. **RED 33, 25/06/2025 (telepresencial)**: .../calendario-atas-e-pautas-das-reunioes/AtaRED33.pdf
   - Presidida pelo DG substituto Caio Farias.
   - Acórdão 443/2025, de relatoria de Alber Vasconcelos: concessão da Hidrovia do Rio Paraguai, com critério técnica e preço 70/30, prazo de 20 anos e vedação à LHG Mining (J&F) na 1ª etapa.
4. **ROD 506, 11/08/2021 (extra)**: .../calendario-atas-e-pautas-das-reunioes/copy_of_Ata506ROD.pdf
   - Presentes: Nery, Tokarski e Takafashi.
   - Registra os ex-diretores interinos Gabriela Costa e Joelson Miranda, pedidos de vista e o voto vencido de Francisval Mendes.

## 5. Taxonomia proposta de temas (a partir das atas 597, 615, RED 33 e das competências da ANTAQ)
1. **Arrendamentos e portos organizados**
   - licitação e estudos de arrendamento (EVTEA, CPLA)
   - contratos de transição e de uso temporário
   - cessão de áreas
   - transferência de titularidade e alteração de controle societário
   - reequilíbrio econômico-financeiro
   - contrato de exploração em porto concedido (ex.: Vports/Peiú)
2. **Concessões** de porto organizado e de hidrovias
   - modelagem, Fator Q e receita-teto
   - revisão contratual
3. **TUP e outras instalações privadas** (autorização, ETC, IP4)
   - autorização e autorização especial/emergencial
   - prorrogação de prazo de início das operações
   - procedimento extraordinário
   - acesso de terceiros (ex.: Itaguaí/minério)
4. **Tarifas portuárias**
   - reajuste e revisão tarifária das autoridades portuárias
   - cobrança de tarifas
5. **Serviços e preços em terminais / relação usuário–terminal**
   - THC2/SSE
   - sobre-estadia (demurrage) de contêineres
   - cobranças de armadores e agentes
   - denúncias com **medida cautelar**
6. **Navegação: outorgas e afretamento**
   - autorização de EBN (empresa brasileira de navegação): longo curso, cabotagem, apoio e interior
   - afretamento e tonelagem (BR do Mar)
   - travessias e passageiros
7. **Fiscalização e sanções**
   - julgamento de autos de infração e multas
   - processo administrativo sancionador
   - TAC: celebração e acompanhamento
   - interdição cautelar
8. **Recursos**
   - recurso de reconsideração
   - embargos de declaração
   - referendo de Deliberação-DG
9. **Normas e regulação**
   - edição e revisão de resoluções
   - Agenda Regulatória
   - audiência e consulta pública
   - tomada de subsídios
   - Sandbox regulatório
   - consultas regulatórias e interpretação de normas
10. **Meio ambiente e ESG**: resíduos, IDA, bunkering, adaptação climática
11. **Governança interna e TCU**
    - cumprimento de acórdãos do TCU
    - relatórios
    - calendário
    - designações
12. **Resolução de conflitos**: mediação e arbitragem regulatória

## 6. Lacunas e próximos passos
- O acervo completo de atas (2015 a 2024) está no **Sophia** (sophia.antaq.gov.br), que não abriu daqui. Os PDFs antigos no gov.br (ex.: `RelSorteio*.pdf`, `SEI_50300.018912_2021_64.pdf`) agora dão NotFound. Próximo passo: liberar `sophia.antaq.gov.br` ou baixar pelo Mac.
- Substitutos não confirmados:
  - quem ocupou as vagas em fev–jul/2016, fev–mai/2018, fev–out/2020 e set–dez/2022;
  - os períodos exatos de Gabriela Costa e Joelson Miranda (2020–2021).
- Para votos detalhados: SEI (pesquisa pública), pelos links da página de resultados das virtuais, e os vídeos das ROD telepresenciais no YouTube.
