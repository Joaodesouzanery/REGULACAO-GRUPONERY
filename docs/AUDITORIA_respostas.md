# Auditoria independente das «Respostas curtas» (ANTT e ANM, 2026)

Data: 2026-11-09. Escopo: a linha «**1. Resposta curta:**» de `clientes/exemplo/2026-antt-10/respostas/01–10.md` e `clientes/exemplo/2026-anm/respostas/01–10.md`.
Método: cada resposta foi quebrada em afirmações verificáveis, e cada afirmação foi conferida com SQL próprio, em modo somente leitura, contra `data/regulacao.db` (ANTT) e `data/anm/regulacao.db` (ANM), no estado atual dos arquivos. O banco **não** foi reindexado, para auditar exatamente a base usada. Não usei os números do resto dos arquivos de resposta.

Convenções:
- **Relatorias**: `votos.eh_relator=1`.
- **% acompanha**: (`acompanha` + `revisor_acompanha`) ÷ votos em que o diretor não era relator.
- **Diverge**: `vencido` + `revisor_diverge`. **Vista**: categoria `vista`.
- **Desfecho**: lido no texto de `itens.resultado` junto com o voto do relator (ver nota B).

Vereditos:
- **CONFIRMADA**: a base sustenta a afirmação.
- **IMPRECISA**: o valor correto vai indicado.
- **SEM BASE**: nenhum dado sustenta a afirmação.
- **INFERÊNCIA**: afirmação qualitativa; digo se os dados a sustentam.

## Resumo

| Veredito | ANTT | ANM | Total |
|---|---|---|---|
| CONFIRMADA (inclui 6 «n=1»: confirmadas, mas apoiadas em um único caso) | 52 | 48 | **100** |
| IMPRECISA (3 graves: desfechos de CONCER, Vale e sustentação oral) | 6 | 12 | **18** |
| SEM BASE | 1 | 0 | **1** |
| INFERÊNCIA (sustentada / parcial / fraca) | 7 (4 / 1 / 2) | 6 (2 / 2 / 2) | **13** |
| **Total de afirmações** | 66 | 66 | **132** |

**As cinco correções mais importantes**
1. **Desfechos «favorável/desfavorável» à empresa estão errados de forma sistemática.** Os casos são ANTT 07 (CONCER), 08 (Rumo) e 10 (sustentação oral) e ANM 07 (Vale). Todos vêm da regra automática `FAV` de `pipeline/consulta.py`, que conta qualquer «aprovado por unanimidade» como favorável à empresa. Mas «aprovado» quer dizer apenas que o voto do relator foi aprovado, e nos recursos esse voto costuma negar o pedido.
   - CONCER: a resposta diz 90 favoráveis e 71 desfavoráveis. A base dá **cerca de 146 desfavoráveis** (recurso negado ou multa mantida), 9 parciais e quase nenhum favorável integral.
   - Vale: a resposta diz 41 favoráveis e 17 desfavoráveis. A base dá **cerca de 30 desfavoráveis, 23 favoráveis ou aprovações**, 16 sem mérito e 2 parciais. O resultado se inverte.
   - Sustentação oral: a comparação «38% contra 74%» não se sustenta. Os 74% contam normas e editais como «favoráveis». Comparando só recursos, os resultados ficam iguais: provimento em 15% com sustentação e em 17% sem ela.
2. **ANTT 05 (Davi Barreto).** A resposta diz que as vistas se «concentram em revisões tarifárias e reequilíbrio». Na base, só **1 das 15** vistas é de reequilíbrio (RD 909). A maior parte trata de regulação normativa e institucional e de ônibus. O argumento citado sobre «menor preço, contas de compensação» vem do edital do semiurbano Timon–Teresina (RD 912, item 1.2), não de uma revisão tarifária.
3. **ANM 06 e 10 (Luís Paniago).** A resposta diz que ele ficou «vencido 3 vezes em disponibilidade». Na base há **1 voto vencido** (RD 71, item 1.3.1) e **2 votos-vista divergentes** (83ª ROP, itens 2.7.1 e 2.7.2). Os 4 vencidos dele aconteceram todos na mesma reunião (RD 71).
4. **ANM 01 (Mauro Sousa).**
   - A resposta diz que as divergências se concentram em «recursos, disponibilidade e unidades de conservação». Contando vencidos e divergentes, a ordem é outra: recursos 75, **licenciamento/registro 33**, pesquisa 11, lavra 11, judicial 9, UC 8, disponibilidade 7.
   - Os argumentos «perda de objeto pela UC» e «autonomia frente ao Ministério Público» aparecem em **uma única justificativa** (RD 89, item 1.3.1). Não são «recorrentes».
   - O único argumento de fato recorrente é a inadmissibilidade de reconsideração contra decisão de última instância.
5. **ANM 10 e ANM 02/04 (rankings e contagens).**
   - «Disponibilidade é o tema mais disputado» é falso. A taxa de unanimidade em disponibilidade é de 80%, mais alta que em minerais críticos (57%), servidão (70%), judicial/liminar (72%), licenciamento (77%) e UC (78%).
   - Tasso Mendonça tem **325 relatorias em outorgas, com 264 unânimes**. A resposta diz 317 e 259.
   - Roger Cabral não é «o grande relator de recursos». Tasso Mendonça tem mais relatorias no tema: 302 contra 264.

Outros pontos que merecem atenção:
- Várias afirmações de «padrão» se apoiam em **um único voto** e deveriam vir com «em um caso»:
  - «não antecipa voto» e «diligências análogas» (ANTT 03);
  - «baixar processos em diligência» (ANM 05);
  - «terceira via» (ANM 02);
  - «prorrogou guias» (ANM 03).
- Em barragens (ANM 08) o número de votos é **441** no microtema ou **397** no tema, e não 332.

### Notas de método
- **A.** Microtema e tema dão números diferentes:
  - ANTT 06 e 09 usam microtemas (`onibus_cassacao`, `conc_free_flow`).
  - No tema amplo `pedagio_freeflow` (161 itens) há 2 vencidos, 1 voto-vista divergente e 9 vistas, e quem mais relata é Davi Barreto (29). Isso acontece porque o tema amplo inclui revisões tarifárias de pedágio.
- **B.** Como classifiquei os desfechos:
  - Script próprio sobre `resultado` + voto do relator:
    - «desprov/não provido/nega/indefer/mantida/não conhec» = desfavorável;
    - «parcial/reduz» = parcial;
    - «sigiloso/retirado/vista/sobrestado» = sem mérito;
    - os demais «aprova/autoriza/defere/dá provimento» = favorável ou aprovação.
  - A classificação também é aproximada, mas lê o voto do relator, que a regra `FAV` ignora.
- **C.** «Sustentação oral» foi identificada por busca textual em assunto, resumo e resultado, com o mesmo critério de `consulta.py sustentacoes`. É um piso: só aparecem os casos em que o resumo menciona a sustentação.

---

## ANTT (`data/regulacao.db`)

| P | Afirmação | Veredito | Valor na base / consulta |
|---|---|---|---|
| 01 Lucas Asfor · ônibus | É relator em 30% dos seus votos sobre ônibus | CONFIRMADA | 65/214 = 30,4% (tema `onibus`) |
| 01 | 65 relatorias, 64 unânimes | CONFIRMADA | 65 relatorias; 64 com `unanime=1` |
| 01 | Linha de «fiscalização firme contra reincidência» | INFERÊNCIA – sustentada | Justificativas como relator: «infração grave e reincidente» (RD 955, 2.3.1), «reiteração; risco à incolumidade» (RD 1031, 1.2.1), «gravidade, reiteração» (RD 967, 1.3.1) |
| 01 | Cassações por circuito aberto, mercados não autorizados e documentos inidôneos | CONFIRMADA | RD 955, 2.3.1 (circuito aberto); RD 1020, 1.3.3 (seccionamentos/mercados não autorizados); RD 957, 2.4.1 (BP-e inidôneos) |
| 01 | Ressalva: efeito suspensivo para empresa em recuperação judicial | CONFIRMADA (n=1) | RD 955, 2.3.3: efeito suspensivo concedido por risco de dano à empresa em RJ. Contraexemplo: na RD 996, 1.4.3, ele negou efeito suspensivo a empresa em RJ |
| 01 | Diverge pouco (2 votos-vista) | CONFIRMADA | `revisor_diverge`=2 (RD 1015, 1.2.3; RD 1020, 1.3.10). Há ainda 1 pedido de vista (RD 1025, 1.2.3) e 1 vista coletiva |
| 01 | «Sempre com argumento jurídico» | INFERÊNCIA – sustentada (n=2) | As duas justificativas são jurídicas |
| 01 | Citação «formalidades são meios, não fins» | CONFIRMADA | `votos.justificativa`, RD 1015 (29/08/2025), item 1.2.3 |
| 01 | Legalidade das janelas de abertura de mercado (art. 47-B) | CONFIRMADA | RD 1020, 1.3.10: «art. 47-B §2º… janelas organizam a abertura gradual» |
| 02 Felipe Queiroz · concessões | Um dos dois maiores relatores de concessões rodoviárias | CONFIRMADA | Empatado com Guilherme Sampaio (120 cada); Lucas Asfor tem 110 |
| 02 | 120 relatorias, 119 unânimes | CONFIRMADA | 120 / 119 |
| 02 | Não tem voto vencido nem voto-vista divergente no tema | CONFIRMADA | 0 `vencido`, 0 `revisor_diverge` no tema. O único voto-vista divergente dele (RD 1044, 1.1.3) é de ônibus |
| 02 | «Quase não diverge» | INFERÊNCIA – sustentada | Acompanha em 96,5% (279/289); os 9 votos «outro» são concordâncias com comentário |
| 02 | Valoriza revisões quinquenais ágeis | CONFIRMADA | RD 1011, 1.2.1 («mantendo agilidade na gestão contratual»); RD 1032, 1.3.1 |
| 02 | Geração de emprego em regiões sem tradição de concessões | CONFIRMADA | RD 1026, 1.3.1 |
| 02 | Comunicação com a sociedade (plano de 100 dias) | CONFIRMADA | RD 1028, 1.1.1 |
| 02 | Pediu vista uma vez no tema, num extrapauta, «por cautela» | CONFIRMADA | RD 1021, extrapauta-1: «cautela por ser extrapauta». Considerando todos os temas, foram 4 vistas |
| 03 Guilherme Sampaio · reequilíbrio | Como diretor e depois diretor-geral | CONFIRMADA | `mandatos`: diretor desde 2021; DG desde 29/08/2025 |
| 03 | 34 relatorias, 32 unânimes | CONFIRMADA | 34 / 32 |
| 03 | Acompanhou o relator em 98% dos demais votos | CONFIRMADA | 138/140 = 98,6% |
| 03 | Padrão de cautela processual | INFERÊNCIA – fraca | Só 2 votos sustentam a ideia (RD 971, 1.3.3; RD 972, 1.4.3). Não basta para falar em «padrão» |
| 03 | Não antecipa voto em casos sensíveis | CONFIRMADA (n=1) | RD 971, 1.3.3: «não antecipa o voto». A generalização não tem base |
| 03 | Pede diligências análogas para casos parecidos (ex.: Malha Oeste) | CONFIRMADA (n=1) | RD 972, 1.4.3: «pede diligência análoga no caso da Malha Oeste» |
| 03 | Não há voto vencido dele no tema | CONFIRMADA | 0 vencido, 0 divergente, 0 vista no tema |
| 04 Alex Azevedo | Pouco mais de um ano, 191 votos | CONFIRMADA | 191 votos, de 02/09/2025 a 22/10/2026 |
| 04 | Relata 34 | CONFIRMADA | 34 |
| 04 | Acompanha a maioria (96%) | CONFIRMADA | 152/157 = 96,8% |
| 04 | Diretor recente com mais posições próprias | CONFIRMADA | Entre os que entraram em 2025–26: Alex tem 5 votos fora do padrão (2 vencidos, 1 vista, 2 «outro»), Severino Medeiros 4 «outro», os demais 0 |
| 04 | Ficou vencido 2 vezes | CONFIRMADA | RD 1025, 1.3.3; RD 1044, 1.1.3 |
| 04 | Citação «o que não está escrito no acordo não pode ser imposto depois» (consensualidade com o TCU) | CONFIRMADA | Justificativa na RD 1025, 1.3.3. O assunto é a vedação a signatárias de solução consensual no TCU |
| 04 | Pediu vista após sustentação oral | CONFIRMADA | RD 1033, 1.5.1: «diante dos argumentos do advogado…» |
| 04 | Perfil jurídico-contratual | INFERÊNCIA – fraca | Só 5 votos fora do padrão; a própria resposta reconhece a amostra pequena |
| 05 Davi Barreto | É quem mais pediu vista na ANTT | CONFIRMADA | 15 vistas; os seguintes têm 5 (Weber Ciloni, Lucas Asfor, Alexandre Porto) |
| 05 | 15 vezes em 1.010 votos | CONFIRMADA | 15 / 1.010 |
| 05 | 2019–2023 | CONFIRMADA | Votos de 09/07/2019 a 16/02/2023 |
| 05 | Vistas concentradas em revisões tarifárias e reequilíbrio | **IMPRECISA** | Só 1 das 15 é de reequilíbrio (RD 909, 2.2.1). Temas das vistas (sobrepostos): regulação normativa 7, institucional 6, ônibus 6 |
| 05 | Dúvidas sobre critério de menor preço, contas de compensação e memórias de cálculo | **IMPRECISA** (contexto) | A justificativa existe, mas é da RD 912, item 1.2: edital do serviço semiurbano Timon–Teresina, não revisão tarifária nem reequilíbrio |
| 05 | Voto-vista divergente na RD 912 redefiniu o cálculo da remuneração | CONFIRMADA | RD 912, 1.1: «aprovado por maioria conforme o voto-vista de Davi Barreto» |
| 05 | Decisão judicial não impedia os mecanismos de equilíbrio | CONFIRMADA | Mesma justificativa da RD 912, 1.1 |
| 06 Cassação · ônibus | Decidida quase sempre por unanimidade | CONFIRMADA | 130/133 itens unânimes; os 3 restantes não têm registro (sessão reservada ou legenda truncada) |
| 06 | Nenhum voto divergente ou vencido no microtema | CONFIRMADA | Em 596 votos: 0 vencido, 0 divergente, 0 vista |
| 06 | Relatores: G. Sampaio 28, L. Asfor 27, F. Queiroz 25, L. Lourenço 25 | CONFIRMADA | Pela coluna `itens.relator`, Lucas Asfor tem 28 |
| 06 | Padrão é manter a cassação em reincidência e circuito aberto | INFERÊNCIA – sustentada | Dezenas de resultados com «cassação mantida» e justificativas com «reiteração» |
| 06 | Exceções em efeito suspensivo para empresas em recuperação judicial | **IMPRECISA** | Há um único caso (RD 955, 2.3.3). Na RD 996, 1.4.3, empresa em RJ teve o efeito suspensivo negado. A regra é «sem efeito suspensivo» (mais de 20 itens) |
| 06 | Exceções em conversões de pena em multa | CONFIRMADA | RD 970, 1.3.1; RD 998, 1.1.1 e 1.2.3; RD 951, 2.3.1; RD 993, 1.2.1; RD 966, 1.1.5; RD 1034, 1.2.1 |
| 07 CONCER | Juiz de Fora–Rio, grupo Triunfo | CONFIRMADA | `entidades.grupo` = Triunfo |
| 07 | Empresa com mais itens: 170 | CONFIRMADA | 170 itens distintos; a seguinte é Autopista Fernão Dias, com 25 |
| 07 | De 2019 a 2025 | CONFIRMADA | 07/05/2019 a 11/09/2025 |
| 07 | Quase todos são recursos contra multas por inexecução | CONFIRMADA | `recurso_reconsideracao` 162; `conc_multa_inexecucao` 140 |
| 07 | Desfecho favorável em 90, desfavorável em 71 | **IMPRECISA (grave)** | A regra `FAV` conta «aprovado por unanimidade» (53 itens) como favorável. Lendo resultado + voto do relator: **≈146 desfavoráveis** (recurso negado/multa mantida), 9 parciais (multa reduzida/cancelada), 9 sem mérito (sigiloso/retirado/vista), 6 indeterminados |
| 07 | Quem mais relata: F. Queiroz 46, L. Asfor 45, L. Lourenço 40 | CONFIRMADA | 46 / 45 / 40 |
| 07 | Nenhum diretor divergiu do relator | CONFIRMADA | 0 vencido/divergente; houve 1 pedido de vista (Lucas Asfor) |
| 08 Grupo Rumo | Seis concessionárias (Malhas Central, Norte, Oeste, Paulista, Sul e a holding) | CONFIRMADA | 6 entidades com grupo Rumo |
| 08 | Soma 59 itens | CONFIRMADA | 59 itens distintos |
| 08 | Recursos, prorrogação e devolução, termos aditivos, liminares | CONFIRMADA | Microtemas: recurso 19, prorrogação/devolução 14, termo aditivo 14, liminar 9 |
| 08 | Favorável em 34, desfavorável em 12 | **IMPRECISA** | Pela leitura resultado + voto: ≈30 aprovações/deferimentos, ≈15 desfavoráveis, 12 sem mérito (retirado/sigiloso/vista), 2 parciais. Mesmo viés da regra `FAV` |
| 08 | Relatores: D. Barreto 10, M. Vinaud 9, A. Porto 6 | CONFIRMADA | 10 / 9 / 6 |
| 09 Free flow | Tema de consenso: nenhum voto divergente ou vencido | CONFIRMADA (microtema) | `conc_free_flow`: 42 itens, todos unânimes, 0 divergência. No tema amplo `pedagio_freeflow` há 2 vencidos, 1 voto-vista divergente e 9 vistas (ver nota A) |
| 09 | Relatores: F. Queiroz 13, L. Asfor 11, L. Lourenço 8 | CONFIRMADA (microtema) | No tema amplo, Davi Barreto lidera com 29 |
| 09 | Temas: praças trocadas por pórticos em aditivos, evasão e cobrança, sandbox | CONFIRMADA | Nos 42 itens: pórtico/praça 23, aditivo 16, cobrança 21, evasão 7, sandbox 11 |
| 10 Sustentação oral | 96 itens com sustentação oral | CONFIRMADA | 96 pela busca textual (é um piso; ver nota C) |
| 10 | Favorável em 38% com sustentação contra 74% na média | **IMPRECISA (grave)** | Os 74% contam toda aprovação de norma ou edital como «favorável à empresa». Leitura resultado + voto: com sustentação, 21% favorável/aprovação e 38% desfavorável. Só recursos: com sustentação (47) 15% providos e 55% negados; sem sustentação (491) 17% providos e 65% negados |
| 10 | «Muda» o resultado | SEM BASE | Não há diferença de desfecho favorável nos recursos. A diferença real está no rito (próximas linhas) |
| 10 | Mais itens retirados de pauta (17%) | CONFIRMADA | 17/96 = 18%; base geral 6% |
| 10 | Mais itens com pedido de vista (10%) | CONFIRMADA | 10/96 = 10%; base geral 4% |
| 10 | Aparece sobretudo em processos difíceis, como sanções e cassações | INFERÊNCIA – parcial | 47/96 são recursos e 32/96 são de `fiscalizacao_sancoes`, mas só 6 de cassação de ônibus. Também aparecem liminares (29) e normas (22) |

## ANM (`data/anm/regulacao.db`)

| P | Afirmação | Veredito | Valor na base / consulta |
|---|---|---|---|
| 01 Mauro Sousa | É, de longe, o diretor que mais diverge | CONFIRMADA | 62 vencidos; os seguintes têm até 4 |
| 01 | 62 votos vencidos | CONFIRMADA | 62 |
| 01 | 16 votos-vista divergentes | CONFIRMADA | 16 |
| 01 | 71 pedidos de vista | CONFIRMADA | 71 (o segundo é Tasso Mendonça, com 53) |
| 01 | Em 1.881 votos | CONFIRMADA | 1.881 |
| 01 | Acompanha o relator em 85% | CONFIRMADA | 1.340/1.570 = 85,4% |
| 01 | Colegas entre 91% e 97% | **IMPRECISA** | Colegas contemporâneos: de 90,9% (Caio Seabra) a 98,6% (Júlio Rodrigues) e 98,4% (Fábio Borges). Tomás Filho (2019–21) tem 87% |
| 01 | Divergências concentradas em recursos, disponibilidade de áreas e UC | **IMPRECISA** | Vencido + divergente por microtema: recurso 75, **licenciamento/registro 33**, pesquisa 11, lavra 11, judicial 9, UC 8, disponibilidade 7 |
| 01 | Argumento recorrente: reconsideração inadmissível contra decisão de última instância | CONFIRMADA | 62ª ROP, 2.7.1–6; RD 68, 5.5.1 e 5.7.1; RD 89, 1.2.1; RD 46, 3.1.1; RD 74, 3.7.1 (cerca de 11 votos) |
| 01 | Argumento recorrente: perda de objeto quando surge UC | **IMPRECISA** | Aparece uma vez (RD 89, 1.3.1). Não é recorrente |
| 01 | Argumento recorrente: autonomia frente ao Ministério Público | **IMPRECISA** | Uma vez explícito (RD 89, 1.3.1), mais uma cautela com recomendações do MPF (RD 71, 2.2.1) |
| 01 | Em vários casos a divergência foi só declarada | CONFIRMADA | 20 dos 78 votos vencidos/divergentes não têm justificativa |
| 02 Tasso Mendonça · outorgas | É o maior relator de outorgas | CONFIRMADA | 325, contra 240 de Roger Cabral |
| 02 | 317 relatorias, 259 unânimes | **IMPRECISA** | 325 relatorias, 264 unânimes (`eh_relator`). Pela coluna `itens.relator`: 344 / 270 |
| 02 | Quem mais votou no período | CONFIRMADA | 2.895 votos |
| 02 | Pede vista com frequência (38 no tema) | CONFIRMADA | 38 |
| 02 | Pede vista para uniformizar casos parecidos | INFERÊNCIA – parcial | Cerca de 6 das 38 justificativas falam em homogeneidade, precedente ou «processos em linha parecida». Muitas não têm justificativa ou citam só «dúvida» |
| 02 | «Terceira via» na 79ª RO, vencida | CONFIRMADA | 79ª ROP, 2.2.1: voto-vista «terceira via», vencido |
| 02 | Tende a soluções intermediárias em disputas de títulos | INFERÊNCIA – fraca | Apoiada em um único caso |
| 02 | Pesa operação em curso, CFEM recolhida e empregos | CONFIRMADA (n=1) | RD 78, 1.2.1: «operação em pleno vapor, recolhe CFEM, gera empregos» |
| 03 Caio Seabra · CFEM | Relata 28% dos votos sobre CFEM (69 relatorias) | CONFIRMADA | 69/244 = 28,3% |
| 03 | Voto-vista derrubou a decisão ad referendum do DG sobre CFEM de municípios afetados (26ª REP, 4 a 1) | CONFIRMADA | 26ª Extraordinária, item 1: «voto-vista de Caio Seabra vencedor (4 a 1)» |
| 03 | CFEM como participação no resultado; conceito ampliado de município afetado é ilegal | CONFIRMADA | Mesma justificativa da 26ª Extraordinária |
| 03 | Prorrogou guias por isonomia com quem pediu antes da Res. 37/2020 | CONFIRMADA (n=1) | RD 71, 4.3.1. O plural «guias» exagera |
| 04 Roger Cabral · recursos | É «o grande relator de recursos» | **IMPRECISA** | É o segundo: Tasso Mendonça tem 302 relatorias e Roger 264 |
| 04 | 264 relatorias no tema, 231 unânimes | CONFIRMADA | 264 / 231 |
| 04 | Acompanha o relator em 97% dos demais votos | CONFIRMADA | 1.018/1.049 = 97,0% |
| 04 | Perfil de alinhamento com a área técnica | INFERÊNCIA – parcial | A base mede alinhamento com o relator, não com a área técnica. 55 das 162 justificativas dele como relator citam parecer, PFE ou área técnica |
| 04 | Raramente pede vista (3) | CONFIRMADA | 3 no tema (4 no total) |
| 04 | Motivos da vista: não prejudicar o regulado pela demora da ANM; comparar precedentes | CONFIRMADA | RD 73, 5.14.1–2; RD 76, 1.2.1 |
| 04 | Ficou vencido só 2 vezes | CONFIRMADA | 2 no tema (3 no total) |
| 05 José Fernando Gomes | Desde set/2025, 478 votos | CONFIRMADA | Primeiro voto em 29/09/2025; 478 votos |
| 05 | Relata 75 itens | CONFIRMADA | 75 |
| 05 | Acompanha o relator em 93% | CONFIRMADA | 377/403 = 93,5% |
| 05 | Já ficou vencido 3 vezes | CONFIRMADA | 3, e há ainda 1 voto-vista divergente não mencionado (80ª ROP, 4.3.1–2) |
| 05 | Pediu vista 4 vezes | CONFIRMADA | 4 |
| 05 | Propõe baixar processos em diligência à Procuradoria para «evitar deliberação questionável» | CONFIRMADA (n=1) | RD 86, 1.3.1. O plural «processos» exagera |
| 05 | Perfil inicial cauteloso e procedimental | INFERÊNCIA – fraca | Só uma diligência. Suas divergências são de mérito (renúncia, auto de infração, prazo da guia). Como relator, invoca segurança jurídica e confiança legítima |
| 06 Luís Paniago | Substituto desde fev/2025 | CONFIRMADA | Primeiro voto em 25/02/2025 |
| 06 | 547 votos, 126 relatorias, 118 unânimes | CONFIRMADA | 547 / 126 / 118 |
| 06 | Acompanha o relator em 91% | CONFIRMADA | 386/421 = 91,7% |
| 06 | 3 votos-vista divergentes, 4 vencidos | CONFIRMADA | 3 / 4. Os 4 vencidos são todos da RD 71 |
| 06 | Ficou vencido 3 vezes em disponibilidade de áreas | **IMPRECISA** | 1 vencido (RD 71, 1.3.1) + 2 votos-vista divergentes (83ª ROP, 2.7.1 e 2.7.2) |
| 06 | Grafia incerta na legenda (Paniago/Panhago) | CONFIRMADA | Trechos: «paniago» 199, «panhago» 59 |
| 07 Grupo Vale | Vale, MBR, Ferrous, Salobo, Vale Manganês e outras | CONFIRMADA | 7 entidades no grupo |
| 07 | 72 itens | CONFIRMADA | 72 itens distintos |
| 07 | Sobretudo recursos, multas, CFEM, lavra e cessões | CONFIRMADA | Microtemas: recurso 50, multa 21, CFEM 20, lavra 15, cessão 11 |
| 07 | Favorável em 41, desfavorável em 17 | **IMPRECISA (grave)** | Leitura resultado + voto: **≈30 desfavoráveis**, ≈23 favoráveis/aprovações, 16 sem mérito (vista/sobrestado/retirado), 2 parciais. O resultado se inverte |
| 07 | Quem mais relata: Tasso Mendonça 16, Guilherme Gomes 11 | CONFIRMADA | 16 / 11 |
| 07 | Casos ligados a UC e ao PAE (multa por lavra fora do PAE) | CONFIRMADA | 10 itens de UC; recurso contra multa por lavra em desacordo com o PAE |
| 08 Barragens | Chegam sobretudo como normas (Res. 95/2022 e sua substituta) e multas | CONFIRMADA | A Res. 95/2022 foi alterada (RD 48, RD 64) e revista (33ª REP/2025); a Res. 220/2025 aparece na RD 87. Em número de itens, porém, predominam recursos e multas (62 e 53) sobre normas (37) |
| 08 | Relatoria: Tasso 15, Roger 9, Mauro 8 | CONFIRMADA (microtema) | Ronaldo Lima também tem 9. No tema `barragens_seguranca`: Tasso 16, Mauro 11, Ronaldo 9, Fábio Borges 9 |
| 08 | 1 voto divergente e 3 vistas | CONFIRMADA | 1 voto-vista divergente (RD 66, 1.5.1) e 3 vistas |
| 08 | Em 332 votos | **IMPRECISA** | 441 votos no microtema (99 itens) ou 397 no tema (89 itens) |
| 08 | É tema de consenso | INFERÊNCIA – sustentada | 93,9% de unanimidade; menor taxa de divergência + vista de todos os microtemas (0,9%) |
| 09 UC e terras indígenas | Aí está a maior divergência do diretor-geral | CONFIRMADA (em taxa) | 22% dos votos são vencido, divergente ou vista: a maior taxa entre microtemas com n≥10. Em número absoluto, recursos lideram (75) |
| 09 | Mauro diverge ou fica vencido 8 vezes e pede vista 11, em 86 votos | CONFIRMADA | 5 vencidos + 3 votos-vista divergentes; 11 vistas; 86 votos |
| 09 | Os colegas quase não divergem | CONFIRMADA | 0 vencido/divergente entre os outros diretores; 4 vistas no total |
| 09 | Disputa: se a criação da UC tira o objeto e quanto a ANM segue o MP | **IMPRECISA** | Só uma justificativa trata disso (RD 89, 1.3.1). As demais falam em UCs criadas sem consultar a ANM, esterilização sem indenização, convivência mineração × UC como questão normativa e segurança jurídica. Várias não têm fundamento registrado |
| 10 Disponibilidade e leilões | É o tema mais disputado | **IMPRECISA** | Unanimidade de 80,4%, maior que em minerais críticos (56,9%), servidão (70%), judicial (72%), licenciamento (76,9%) e UC (77,7%). Divergência + vista: 4,4%, contra 10,9% em minerais críticos |
| 10 | Mauro diverge 7 e pede vista 7 | CONFIRMADA | 5 vencidos + 2 votos-vista divergentes; 7 vistas |
| 10 | Luís Paniago fica vencido 3 | **IMPRECISA** | 1 vencido + 2 votos-vista divergentes |
| 10 | Tasso pede vista 7 | CONFIRMADA | 7 |
| 10 | Relatores: Tasso 28, Caio 23, Victor Bicca 22, Roger 21 | CONFIRMADA | Por `eh_relator`. Pela coluna `itens.relator`: Tasso 30, Caio 30, Roger 22, Victor Bicca 22 |
| 10 | Victor Bicca nos primeiros editais | CONFIRMADA | Votou de 2019 a 2022 |
| 10 | Debate sobre inabilitações, documentos exigidos e prioridade entre requerentes | INFERÊNCIA – sustentada | Nos 32 votos fora do padrão: prioridade/pontuação/empate 10, documentos/exigências 8, inabilitação 5 |

---

### Consultas usadas
Os scripts ficaram no scratchpad da sessão, fora do repositório: `q.py`, `st.py` e `cls.py`, todos com conexão `mode=ro`. As consultas principais foram:
- **Perfil de um diretor:** `select v.categoria, v.eh_relator, i.unanime from votos v join itens i … where v.diretor=? [and v.item_id in (select item_id from item_temas where tema=?)]`.
- **Microtemas:** a mesma consulta com `item_microtema`.
- **Rankings:** `select diretor, count(*) … where eh_relator=1 group by 1` e `select diretor, count(*) … where categoria='vista' group by 1`.
- **Empresas e grupos:** `item_entidade` + `entidades.grupo`, com `count(distinct item_id)`; desfecho pelo script de leitura descrito na nota B.
- **Citações:** busca `LIKE` em `votos.justificativa`, `votos.voto`, `votos.trecho`, `itens.assunto/resumo/resultado`, `trechos.texto` e `falas_diretores`. Todas as citações entre aspas das respostas foram encontradas em `votos.justificativa`. Nenhuma foi encontrada na legenda literal (`trechos`), porque são paráfrases da análise, não falas transcritas.

Limites:
- A base vem de legendas automáticas.
- A conferência cega mede consistência da análise (≈94–95% nos votos da ANTT), não verdade absoluta.
- Itens sigilosos ficam fora.
- Esta auditoria mede **fidelidade à base**, não a correção da base.
