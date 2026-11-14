# Novas agências: ANEEL, ANP, ANAC, ANA (avaliação de 14/11/2026)

Método: páginas públicas do YouTube (abas *playlists*, *streams* e *videos*, lidas com curl daqui em 14/11/2026), buscas na web e o gov.br. O gov.br respondeu 401 na página de composição da ANEEL e 429 na da ANAC (limite de requisições), e não tentei contornar. Por isso a composição das diretorias saiu de imprensa especializada e documentos oficiais e **precisa ser confirmada pelo agente `pesquisador-mandatos`** (DOU/Senado). As contagens de reuniões são **estimativas** até rodarmos o inventário (`01_coletar.py ... 0`).

## Quadro comparativo

| | ANEEL | ANP | ANAC | ANA |
|---|---|---|---|---|
| Canal | @aneel | @ANPgovbr | @OficialANAC | youtube.com/anagovbr |
| Formato | Reunião Pública Ordinária (RPO) semanal (terças), mais extraordinárias e sorteios públicos de processos | Reunião de Diretoria Colegiada (RD) numerada (nº 1193 em 29/10/2026), quinzenal, mais extraordinárias | Reunião Deliberativa presencial (~7 a 12 por ano, numeradas por ano) + **Deliberativa Eletrônica** semanal (sem vídeo) | Reunião Deliberativa Ordinária (RDO) numerada (956ª em 28/07/2026), quase semanal |
| Playlist de reuniões | sem playlist própria; RPOs ficam na aba *Ao vivo* (`/streams`). Sorteios: `PL83dxI5zonT57parQ4wTTPBqWykH5ECJi`; «CDPO 2026»: `PL83dxI5zonT4cg06i_OTJ6PO_9Hqj-N_y` (41 vídeos) | «Reuniões de Diretoria» `PLvGUUvSxkN9WLZpSBz_bnvTzpnuTj1oVr` (242 vídeos) | «Reuniões da Diretoria Colegiada» `PLCncnMm7iOKx3SHwLOHyVn21aXD-iZV8d` (850 vídeos) | sem playlist; RDOs na aba *Ao vivo* (`/streams`) |
| Transmitidas desde 2018 (estimativa) | ~330 a 380 RPOs + ~60 extraordinárias | ~240 (é a própria playlist) | ~90 a 130 deliberativas presenciais; os 850 vídeos da playlist incluem outros formatos, a conferir | poucas: vídeo de RDO só aparece com segurança em 2026 (~15 a 25) |
| Duração típica | longa (3 a 8 h, sustentações orais) | 1 a 3 h | 1 a 3 h | 0,5 a 1,5 h |
| Pauta, atas e calendário no gov.br | sim (calendário das reuniões públicas, pautas, atas e votos) | sim (pautas, atas e calendário por ano) | sim (pautas e atas, presenciais e eletrônicas) | sim (calendário, despachos de resultado e votos) |
| Mercado | **muito alto** | **alto** | médio-alto | médio (saneamento em alta) |
| Esforço (h de análise + conferência) | 150 a 220 h (todo o período); piloto 2025–26 ≈ 50 h | 50 a 70 h | 40 a 70 h | 15 a 25 h (base pequena) |
| Ordem recomendada | **1 (piloto 2025–26)** | **2** | **3** | **4** |

A estimativa de horas usa a régua da ANTT/ANTAQ: cerca de 0,25 a 0,5 h por reunião curta (subagente `analista-reuniao` + validação) e 0,5 a 1 h por reunião longa, mais cerca de 10 h fixas por agência (config, mandatos, dirigentes, amostra cega, organizar, relatório).

---

## 1. ANEEL (energia elétrica)

**(1) Como se reúne.** A diretoria colegiada (diretor-geral + 4 diretores) faz **Reuniões Públicas Ordinárias** semanais, transmitidas ao vivo no YouTube, com sustentação oral. Há também reuniões extraordinárias e **sessões públicas de sorteio/distribuição de processos**. Em 14/11/2026, a aba *Ao vivo* do canal mostrava da «19ª» à «24ª Reunião Pública Ordinária da Diretoria da ANEEL de 2026», além de «12ª Sessão Pública Extraordinária de Sorteio de 2026». O canal transmite RPOs pelo menos desde 2016–2017. Não existe playlist só de reuniões: a coleta tem de usar o canal inteiro e filtrar pelo título com o regex `Reuni[ãa]o P[úu]blica (Ordin|Extraordin)`.
- Playlists que interessam: «Sessões Públicas de Distribuição de Processos» `PL83dxI5zonT57parQ4wTTPBqWykH5ECJi`, «CDPO 2026 da Diretoria da ANEEL» `PL83dxI5zonT4cg06i_OTJ6PO_9Hqj-N_y` (41 vídeos, conteúdo a conferir) e «Sorteios Públicos de Credenciamento» `PL83dxI5zonT5QBKRu9kKekKFMglz2t4QI`.

**(2) Volume.** Historicamente são de 40 a 48 RPOs por ano (em 2026, a 24ª aparece em novembro, o que indica um ritmo menor). De 2018 a 2026, a estimativa é de **~330 a 380 ordinárias** mais extraordinárias. Todas trazem legenda automática.

**(3) Pauta, atas, calendário.** Calendário das Reuniões Públicas (menu «Calendário de Atividades» do gov.br/aneel); pautas e votos em PDF por processo (ex.: voto do diretor Gentil Nogueira na 21ª RPO/2026). A página de composição respondeu 401 a requisições automáticas.
- https://www.gov.br/aneel/pt-br (Calendário de Atividades → Calendário das Reuniões Públicas)

**(4) Composição (a confirmar no DOU).**
- Sandoval de Araújo Feitosa Neto, diretor-geral (mandato até 13/08/2027; a diretora Agnes Costa é a substituta designada).
- Agnes Maria de Aragão da Costa, diretora.
- Gentil Nogueira de Sá Júnior, diretor (posse em set/2025).
- Willamy Moreira Frota, diretor (posse em set/2025).
- Vaga de **Fernando Mosna**, cujo mandato terminou em ago/2026 (despedida na RPO de 11/08/2026). Ocupante ou substituto a confirmar; a imprensa citou Ludimila Silva para a vaga.
- Fontes: [despedida de Mosna](https://cenarioenergia.com.br/2026/08/06/aneel-analisa-recurso-da-enel-sp-contra-processo-de-caducidade-em-sessao-que-marca-despedida-de-fernando-mosna/), [posse de Gentil e Willamy](https://cenarioenergia.com.br/2025/09/16/novos-diretores-da-aneel-e-anm-tomam-posse-com-missao-de-modernizar-e-fortalecer-agencias/), [substituição do diretor-geral](https://tagdlaw.com.br/?p=16568), [vaga de Mosna](https://canalsolar.com.br/ludimila-silva-vaga-mosna-diretoria-aneel/), [voto 21ª RPO/2026](https://cenarioenergia.com.br/wp-content/uploads/2026/06/Aneel-48500.007946-2026-30.pdf).

**(5) Mercado e temas quentes.** É o maior mercado regulado em número de clientes potenciais: ~100 distribuidoras (Enel, Equatorial, Neoenergia, CPFL, Energisa, Light), transmissoras, geradoras, comercializadoras, associações (Abradee, Absolar, Abeeólica, Abrace), grandes consumidores, bancos e escritórios. Temas quentes: caducidade e renovação de concessões de distribuição (Enel SP), curtailment de eólicas e solares, leilões de armazenamento (baterias), geração distribuída e subsídios (CDE), bandeiras e revisões tarifárias, abertura do mercado livre, bônus de Itaipu.

**(6) Esforço.** Alto por volume e duração (sessões de 4 a 8 h). A recomendação é um **piloto 2025–2026 (~70 RPOs, ~50 h)** e depois retroceder ano a ano. Também é preciso separar sorteios e sessões de distribuição, que não são deliberação. **Ordem: 1ª**, pelo valor comercial, começando pelo piloto.

---

## 2. ANP (petróleo, gás natural e biocombustíveis)

**(1) Como se reúne.** A diretoria colegiada tem diretor-geral + 4 diretores e faz **reuniões deliberativas quinzenais** numeradas (RD nº 1188 em 07/08/2026, nº 1193 em 29/10/2026), além de extraordinárias (Extraordinária nº 70 em 30/06/2026). Desde set/2024, por corte orçamentário, a ANP **deixou de transmitir ao vivo**: publica a gravação no YouTube em até 24 h, e a eixos retransmite ao vivo por conta própria. Para o projeto, o vídeo gravado basta.
- Playlist «Reuniões de Diretoria» **`PLvGUUvSxkN9WLZpSBz_bnvTzpnuTj1oVr`** (242 vídeos; inclui extraordinárias desde pelo menos 2022, como a nº 64 de 09/11/2022).

**(2) Volume.** Pela numeração, foram ~130 ordinárias de 2018 a 2026 (de ~1060 até 1193) mais ~20 extraordinárias. Como a playlist tem 242 vídeos, ela provavelmente vai além (2017 ou antes) ou inclui retomadas. Estimativa: **~150 a 240 vídeos aproveitáveis**.

**(3) Pauta, atas, calendário.** Sim, é a mais organizada das quatro: pautas, atas e calendário por ano em PDF.
- https://www.gov.br/anp/pt-br/composicao/diretoria-colegiada/reunioes-da-diretoria-colegiada/pautas-atas-e-calendario-de-reunioes-da-diretoria-colegiada (ex.: [ata 1182](https://www.gov.br/anp/pt-br/composicao/diretoria-colegiada/reunioes-da-diretoria-colegiada/pautas-atas-e-calendario-de-reunioes-da-diretoria-colegiada/2026/arquivos-rd-2026/ata-1182.pdf), [pauta 1186](https://www.gov.br/anp/pt-br/composicao/diretoria-colegiada/reunioes-da-diretoria-colegiada/pautas-atas-e-calendario-de-reunioes-da-diretoria-colegiada/2026/arquivos-rd-2026/pauta-1186.pdf))

**(4) Composição (a confirmar).**
- Artur Watt Neto, diretor-geral (posse em set/2025).
- Pietro Mendes, diretor (posse em set/2025).
- Symone Araújo, diretora.
- Júlio Nishida, diretor **substituto** (desde out/2026, na vaga de Daniel Maia).
- Amanda Gondim, diretora **substituta** (convocada em nov/2026, na vaga de Fernando Moura).
- Em abr/2026 houve um placar dividido (3×2) na reforma do regimento interno, com Pietro e Symone contra. É um bom caso para o perfil.
- Fontes: [Nishida interino](https://cenarioenergia.com.br/2026/10/08/julio-nishida-assume-diretoria-da-anp-interinamente-a-partir-da-proxima-semana/), [Gondim](https://www.novacana.com/noticias/com-o-fim-do-mandato-de-fernando-moura-amanda-gondim-assume-diretoria-da-anp), [regimento 3×2](https://cenarioenergia.com.br/2026/04/24/reforma-interna-da-anp-reduz-transparencia-administrativa-e-eleva-alerta-sobre-risco-regulatorio/), [fim da transmissão ao vivo](https://eixos.com.br/noticias/anp-interrompe-transmissao-de-reunioes-devido-a-cortes-orcamentarios/), [RD 1191 (eixos)](https://eixos.com.br/petroleo-e-gas/reuniao-de-diretoria-da-anp-no-1-191/).

**(5) Mercado e temas quentes.** Petroleiras (Petrobras, Shell, Equinor, Prio, independentes), distribuidoras de combustíveis (Vibra, Raízen, Ipiranga) e revendas, gás natural (transportadoras, comercializadoras, Nova Lei do Gás), usinas de etanol e biodiesel, associações (IBP, Abegás, Abicom, Unica). Temas quentes: Combustível do Futuro e mandatos de mistura (etanol/biodiesel), fiscalização e multas, CBIOs/RenovaBio, acesso a gasodutos e terminais, rodadas e oferta permanente, regimento interno e transparência, decommissioning.

**(6) Esforço.** Médio: reuniões curtas e atas boas para conferir. São **50 a 70 h**. **Ordem: 2ª.** Pode até ir em 1º se o objetivo for ter rápido uma agência «completa» de 2018 a 2026.

---

## 3. ANAC (aviação civil)

**(1) Como se reúne.** A diretoria tem diretor-presidente + 4 diretores, com dois ritos:
- **Reunião Deliberativa presencial**, transmitida no YouTube e numerada por ano. Em 2026, a 7ª foi em 06/10/2026 e a 3ª em 04/02/2026.
- **Reunião Deliberativa Eletrônica**, semanal (de 12 h de um dia a 23h59 do dia seguinte), com ~30 a 40 por ano e **sem vídeo**: só pauta e ata.

Playlist «Reuniões da Diretoria Colegiada» **`PLCncnMm7iOKx3SHwLOHyVn21aXD-iZV8d`** (850 vídeos, com reuniões de 2022, 2023 e 2025 identificadas). O total alto sugere que cada item ou sustentação vira um vídeo, ou que a playlist cobre anos antigos. Isso precisa ser conferido no inventário.

**(2) Volume.** De 2018 a 2026 a estimativa é de **~90 a 130 deliberativas presenciais**. As eletrônicas (~300) só podem ser cobertas por ata em texto, sem vídeo e sem trecho com minuto.

**(3) Pauta, atas, calendário.** Sim, para os dois ritos:
- https://www.gov.br/anac/pt-br/acesso-a-informacao/institucional/reunioes-da-diretoria/reunioes-deliberativas (ex.: [ata 8ª/2025](https://www.gov.br/anac/pt-br/acesso-a-informacao/institucional/reunioes-da-diretoria/reunioes-deliberativas/2025/arquivos-8a-redir-del/ata-8a-redir-deliberativa-de-22-de-maio-de-2025.pdf))
- https://www.gov.br/anac/pt-br/acesso-a-informacao/institucional/reunioes-da-diretoria/reunioes-deliberativas-eletronicas

**(4) Composição (a confirmar; houve trocas em 2026).**
- Tiago Chagas Faierstein, diretor-presidente.
- Antonio Mathias Nogueira Moreira, diretor.
- Rui Chagas Mesquita, diretor.
- Luiz Ricardo de Souza Nascimento, diretor: o mandato teria terminado em 19/03/2026, a confirmar.
- Mariana Altoé, diretora substituta (convocada em fev/2026 após a renúncia de Tiago Sousa Pereira).
- Fontes: [Plano de Diretrizes 2026](https://www.gov.br/anac/pt-br/acesso-a-informacao/acoes-e-programas/governanca/arquivos-e-imagens/PLANODEDIRETRIZESPARA2026v.1final.pdf), [Agência iNFRA, fev/2026](https://agenciainfra.com/blog/?p=36535), [calendário de jan/2026](https://agenciainfra.com/blog/agencias-reguladoras-retomam-reunioes-deliberativas-a-partir-desta-semana/).

**(5) Mercado e temas quentes.** Companhias aéreas (LATAM, Gol, Azul; Gol e Azul em reestruturação), concessionárias de aeroportos (Aena, CCR/Motiva, Fraport, Zurich, Inframerica), táxi aéreo, eVTOL (Eve), MRO, associações (Abear, ABR). Temas quentes: revisão dos direitos do passageiro (Res. 400, judicialização), repactuação e relicitação de concessões (procedimento competitivo), slots em Congonhas e Santos Dumont, regulação de eVTOL e drones, tarifas aeroportuárias.

**(6) Esforço.** Médio: poucas reuniões com vídeo, mas parte da decisão acontece nas eletrônicas, cobertas só por ata. São **40 a 70 h**. **Ordem: 3ª.**

---

## 4. ANA (águas e saneamento básico)

**(1) Como se reúne.** A diretoria colegiada (diretor-presidente + 4 diretores) faz **Reuniões Deliberativas Ordinárias** numeradas e quase semanais: 952ª em 31/03/2026, 956ª em 28/07/2026, 957ª em 11/08/2026, 960ª em ago/2026. O resultado sai em «Despacho Resultado DIREC». Na aba *Ao vivo* do canal aparecem «956th/957th Ordinary Deliberative Meeting of the Collegiate Board» (2026, títulos em tradução automática). **Não há playlist de reuniões.** Não ficou claro desde quando o vídeo existe: a hipótese é 2025 ou 2026. As playlists do canal são de cursos, PISF e audiências.

**(2) Volume.** Pequeno: **~15 a 25 vídeos** de RDO até agora (a confirmar no inventário). Antes disso, só despachos e votos em texto.

**(3) Pauta, atas, calendário.** Sim:
- https://www.gov.br/ana/pt-br/acesso-a-informacao/institucional/reuniao-deliberativa/calendario-das-reunioes-deliberativas
- Despachos e votos no SEI e em participacao-social.ana.gov.br (ex.: [Despacho DIREC 305](https://participacao-social.ana.gov.br/api/files/SEI_0222332_Despacho_Resultado_DIREC_305-1785521493702.pdf))

**(4) Composição (a confirmar; há muita interinidade).**
- Cristiane Battiston, diretora e **diretora-presidente interina** desde 16/07/2026.
- Larissa Rego, diretora (posse em 01/10/2025).
- Leonardo Silva, diretor (posse em 01/10/2025).
- Ana Paula Fioreze, diretora **substituta** (desde jul/2026, vaga de Ana Carolina Argolo).
- Vaga da ex-presidente Veronica Sánchez (mandato encerrado em 16/01/2026), sem titular confirmado.
- Fontes: [posse de 3 diretores](https://agenciainfra.com/blog/ana-da-posse-a-tres-novos-diretores-com-cinco-anos-de-mandato/), [Battiston interina](https://cenarioenergia.com.br/2026/07/16/cristiane-battiston-assume-presidencia-interina-da-ana/), [Fioreze](https://agenciainfra.com/blog/?p=43836), [fim do mandato de Sánchez](https://agenciainfra.com/blog/?p=34904), [956ª RDO](https://www.gov.br/ana/pt-br/assuntos/noticias-e-eventos/noticias-periodo-eleitoral-2026/diretoria-colegiada-da-ana-aprova-proposta-de-agenda-regulatoria-2027-2028-e-revisao-tarifaria).

**(5) Mercado e temas quentes.** Concessionárias privadas de saneamento (Aegea, Iguá, BRK, Sabesp privatizada, GS Inima), estatais estaduais, agências infranacionais, irrigantes e hidrelétricas (outorga), mineradoras (segurança de barragens). Temas quentes: Normas de Referência do saneamento (NR 5, 8, 12) e comprovação de adoção, regulação tarifária de água e esgoto, Agenda Regulatória 2027–2028, PISF (Transposição do São Francisco), segurança de barragens, crises hídricas.

**(6) Esforço.** Baixo, porque a base é pequena: **15 a 25 h**. O valor analítico será limitado até haver mais reuniões gravadas, e a vacância é muito alta, o que é interessante para a skill `vacancia-agencia`. **Ordem: 4ª.** Pode ser feita em paralelo por ser barata, desde que o cliente-alvo seja saneamento.

---

## Comandos para começar

Testar daqui (sem criar nada; o `--simular` só mostra o que seria criado):

```bash
python3 pipeline/iniciar_agencia.py aneel @aneel "Agência Nacional de Energia Elétrica" --simular
python3 pipeline/iniciar_agencia.py anp @ANPgovbr "Agência Nacional do Petróleo, Gás Natural e Biocombustíveis" --simular
python3 pipeline/iniciar_agencia.py anac @OficialANAC "Agência Nacional de Aviação Civil" --simular
python3 pipeline/iniciar_agencia.py ana @anagovbr "Agência Nacional de Águas e Saneamento Básico" --simular
```

No Mac (o YouTube bloqueia a nuvem para legendas):

```bash
# ANEEL: sem playlist de reuniões → canal inteiro (filtrar "Reunião Pública" depois)
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh aneel @aneel
# ANP: playlist de reuniões de diretoria
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh anp PLvGUUvSxkN9WLZpSBz_bnvTzpnuTj1oVr
# ANAC: playlist de reuniões da diretoria colegiada
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh anac PLCncnMm7iOKx3SHwLOHyVn21aXD-iZV8d
# ANA: sem playlist → canal inteiro (filtrar "Reunião Deliberativa")
caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh ana @anagovbr
```

Antes de rodar no Mac:
- Confira que o canal da ANA responde como `@anagovbr`. A URL informada é `youtube.com/anagovbr`. Se o handle não existir, use `https://www.youtube.com/anagovbr`.
- Rode o inventário daqui (`bash pipeline/ag.sh <sigla> python3 pipeline/01_coletar.py <canal> 0`) para substituir as estimativas acima por contagens reais.
- Para ANEEL e ANA, inclua no `config_agencia.json` um filtro de título de reunião de diretoria, para não baixar milhares de vídeos institucionais.
