# Transparência e facilidade de acompanhar as agências — 16/11/2026

Notas 0–2 por critério (0 = não existe/não funciona; 1 = parcial; 2 = completo e fácil), com evidência em `data/<ag>/transparencia.json`. Gerado por `python3 pipeline/transparencia.py`.

| Agência | Reuniões transmitidas | Legenda disponível | Pauta antecipada | Atas e votos escritos | Calendário anual | Composição e currículos | Sigilo e reuniões sem vídeo | Facilidade de acesso | Total | Vídeos de diretoria 2018+ | % com legenda | Calendário na base | Pautas baixadas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ANTT | 2 | 2 | 1 | 1 | 0 | 1 | 1 | 1 | 9/16 | 289 | 99% | não | 0 |
| ANM | 2 | 1 | 1 | 2 | 0 | 2 | 1 | 1 | 10/16 | 121 | 96% | sim | 0 |
| ANTAQ | 1 | 2 | 1 | 1 | 2 | 2 | 0 | 1 | 10/16 | 117 | 96% | sim | 2 |
| ANEEL | 2 | 2 | 1 | 2 | 2 | 2 | 1 | 1 | 13/16 | 763 | 97% | sim | 0 |
| ANP | — | — | — | — | — | — | — | — | —/16 | — | — | — | — |

## Ranking

1. ANEEL (13)
2. ANTAQ (10)
3. ANM (10)
4. ANTT (9)
5. ANP (sem avaliação)

## Evidências

### ANTT
- **Reuniões transmitidas** (2): 289 vídeos de reunião de diretoria no canal @canalANTT entre 2019 e 2026 (45/45/43/33/30/31/36/26 por ano). Desde 2020 as pautas dizem que a reunião é transmitida ao vivo no YouTube. Não cruzei com o calendário nem com as atas, então reuniões que não foram ao canal podem estar faltando na contagem. — /home/user/REGULACAO-GRUPONERY/COBERTURA.md; https://www.gov.br/antt/pt-br/assuntos/noticias/documentos/pauta-871-reuniao-de-diretoria-1.pdf
- **Legenda disponível** (2): 284 dos 289 vídeos de diretoria têm transcrição útil (cerca de 98%). Os 5 restantes têm legenda desativada ou só ruído (2019, 2021, 2022, 2023, 2026). A legenda é automática. — /home/user/REGULACAO-GRUPONERY/sem_transcricao.md; /home/user/REGULACAO-GRUPONERY/COBERTURA.md
- **Pauta antecipada** (1): A ANTT publica a pauta em PDF, com data, hora, matérias por diretor e número de processo SEI (ex.: 1.040ª reunião, de 27/08/2026). Não medi a antecedência e não achei pautas na base local (data/pautas não existe). — https://www.gov.br/antt/pt-br/assuntos/noticias/documentos/pauta-872-reuniao-de-diretoria.pdf; https://agenciainfra.com/blog/wp-content/uploads/2026/08/PAUTA-DA-1.040a-REUNIAO-DE-DIRETORIA-PUBLICA-DE-27.08.2026.pdf
- **Atas e votos escritos** (1): A pauta abre com a aprovação da ata da reunião anterior, então a ata existe. Não encontrei na busca o repositório oficial de atas nem o prazo de publicação. Os votos da base vêm do vídeo, não de documento escrito. — https://www.gov.br/antt/pt-br/assuntos/noticias/documentos/pauta-da-868-reuniao-de-diretoria-1.pdf
- **Calendário anual** (0): Não encontrado (não é o mesmo que não existir). A busca não trouxe calendário anual oficial e data/calendario.json não existe na base. As reuniões são anunciadas uma a uma em notícias 'Acompanhe a Nª ReDir'. — https://www.gov.br/antt/pt-br/assuntos/acompanhe-a-971a-reuniao-de-diretoria-da-antt-redir
- **Composição e currículos** (1): A base tem mandatos com Senado, DOU e fim legal (data/mandatos.json) e minibios (data/dirigentes). Não conferi nesta rodada a página oficial da ANTT com a diretoria, os substitutos e os currículos. — /home/user/REGULACAO-GRUPONERY/data/mandatos.json
- **Sigilo e reuniões sem vídeo** (1): 43 dos 2382 itens analisados (1,8%) têm resultado sigiloso no banco. Não medi as reuniões virtuais ou internas sem transmissão. — /home/user/REGULACAO-GRUPONERY/data/regulacao.db (tabela itens)
- **Facilidade de acesso** (1): O portal gov.br tem uma seção Reuniões de Diretoria e notícias por reunião, mas as pautas são PDFs soltos com URLs irregulares (ex.: 'copy_of_Pauta882...'). Não achei dados abertos estruturados. O YouTube bloqueia IPs de nuvem na coleta de legendas. — https://www.gov.br/antt/pt-br/assuntos/ultimas-noticias/copy_of_Pauta882ReuniaodeDiretoria1.pdf
- Observações: Soma 9/16. Base local de 2026-11-14. Faltam: calendario.json e pautas/ na base; o cruzamento de vídeos com a numeração das reuniões; a antecedência da pauta; o prazo de publicação das atas; a página oficial de composição. 'Calendário' e 'atas' estão como não encontrados, não como inexistentes.

### ANM
- **Reuniões transmitidas** (2): 121 vídeos de diretoria em data/anm/videos.jsonl (2019:7, 2020:22, 2021:17, 2022:16, 2023:12, 2024:19, 2025:14, 2026:10, 4 sem data) para 122 atas em atas/indice_atas.json e 130 reuniões no banco; cobertura quase completa — data/anm/videos.jsonl; data/anm/atas/indice_atas.json; canal YouTube da ANM
- **Legenda disponível** (1): 27 vídeos sem legenda (data/anm/sem_legenda.jsonl) de 238 listados (~11%); 150 transcrições existentes — data/anm/sem_legenda.jsonl; data/anm/transcricoes/
- **Pauta antecipada** (1): Pauta oficial em PDF por reunião (ex.: 87ª ROP de 29/07/2026); antecedência da publicação não medida — https://www.gov.br/anm/pt-br/composicao/diretoria-colegiada/reunioes-da-diretoria-colegiada/pautas-da-rop/pauta-da-87a-rop.pdf
- **Atas e votos escritos** (2): 122 atas em PDF (a partir de 06/09/2019) com presentes, relator, processo e resultado por item; prazo de publicação não medido — https://www.gov.br/anm/pt-br/composicao/diretoria-colegiada/reunioes-da-diretoria-colegiada/atas-da-rop/
- **Calendário anual** (0): Calendário oficial não encontrado; o registro da base diz «não há calendário oficial publicado». Não confirmado como inexistente — data/anm/calendario.json
- **Composição e currículos** (2): Página de composição da diretoria colegiada no gov.br; base com minibios, fotos e mandatos de diretores atuais e anteriores. Página oficial não reconferida na web nesta rodada — https://www.gov.br/anm/pt-br/composicao/diretoria-colegiada; data/anm/dirigentes/; data/anm/mandatos.json
- **Sigilo e reuniões sem vídeo** (1): Nenhum dos 3619 itens do banco tem resultado sigiloso; mas há cerca de 7–8 reuniões com ata ou registro no banco sem vídeo correspondente, e as ROPs recentes são por videoconferência (Teams) — data/anm/regulacao.db; data/anm/calendario.json
- **Facilidade de acesso** (1): URLs estáveis no gov.br e PDFs por reunião; sem dados abertos estruturados de votos e sem busca por item; YouTube bloqueia IPs de nuvem — gov.br/anm (atas e pautas da ROP)
- Observações: Avaliação feita com a base local; nenhuma página foi consultada na web nesta rodada. Dados ainda não verificados: antecedência das pautas, prazo das atas e existência de um calendário oficial (marcado como não encontrado, não como inexistente). A contagem de vídeos de diretoria depende da classificação em videos.jsonl, com 62 vídeos 'outro' sem data.

### ANTAQ
- **Reuniões transmitidas** (1): data/antaq/videos.jsonl: 547 vídeos (324 com data, de 2011 a 2026; 21 a 37 por ano). As RODs telepresenciais são transmitidas no YouTube. As RODs virtuais via SEI (Resolução ANTAQ 66) não têm vídeo: são 7 das 13 reuniões do calendário do 2º semestre de 2026 (calendario.json). — data/antaq/videos.jsonl; data/antaq/calendario.json; https://youtube.com/c/CanalANTAQ
- **Legenda disponível** (2): 289 transcrições na base contra 44 vídeos sem legenda (sem_legenda.jsonl), cerca de 87% dos vídeos baixados. — data/antaq/transcricoes/; data/antaq/sem_legenda.jsonl
- **Pauta antecipada** (1): A pauta é publicada em PDF (lista processos por relator, nº SEI, interessados e assunto) na página do calendário. Os nomes dos arquivos não seguem padrão (ex.: PautadaROD616_vs4.pdf). A pauta da ROD 625 (10/12/2026) ainda está 'a confirmar'. Antecedência em dias não medida (não encontrado). — data/antaq/pautas/625.json; data/antaq/pesquisa_atas.md; https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes
- **Atas e votos escritos** (1): As atas (PDF assinado no SEI) trazem os acórdãos na íntegra, o relator, quem pediu vista e quem ficou vencido (ex.: ROD 597, Flávia Takafashi vencida). A fundamentação dos votos não vem na ata: fica no SEI e no vídeo. As virtuais têm página de resultados com links ao SEI. O acervo antigo está no Sophia, que estava bloqueado na pesquisa. Prazo de publicação não medido. — https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes/AtaROD615.pdf; .../resultado-das-reunioes-virtuais-da-diretoria-1; data/antaq/pesquisa_atas.md
- **Calendário anual** (2): Calendário semestral aprovado por acórdão (Acórdão 351/2026), com data e formato (virtual/telepresencial) de cada ROD de 613 a 625. Cumprimento não verificado. — https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/calendario-atas-e-pautas-das-reunioes/Calendrio2semestre2026.pdf
- **Composição e currículos** (2): Há página da diretoria atual e de ex-diretores. Os substitutos são definidos por decreto (DOU 31/01/2025). A base tem 17 registros de mandatos e as minibios dos dirigentes. — https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/diretoria-colegiada; data/antaq/mandatos.json; data/antaq/bios.json
- **Sigilo e reuniões sem vídeo** (0): Sigilo formal baixo: 7 de 5.190 itens com resultado sigiloso no banco (0,13%). Porém a maioria das RODs (7 das 13 no 2º semestre de 2026) é virtual via SEI, sem transmissão nem debate público; só ficam o resultado escrito e os votos no SEI. — data/antaq/regulacao.db (consulta via pipeline/ag.sh); data/antaq/calendario.json
- **Facilidade de acesso** (1): Os PDFs têm nomes irregulares e o caminho indexado pelo Google, sem o subdiretório, devolve NotFound. Há links antigos quebrados na página de distribuição de processos. O acervo Sophia não abriu a partir da nuvem. Há XLS semanal de distribuição de processos. Portal de dados abertos não verificado. — data/antaq/pesquisa_atas.md; https://www.gov.br/antaq/pt-br/acesso-a-informacao/institucional/reunioes-deliberativas/distribuicao-de-processos
- Observações: Avaliação baseada na base local e em data/antaq/pesquisa_atas.md (pesquisa de 09/11/2026); não fiz nova busca na web. Há 223 vídeos sem data no videos.jsonl, então a % de reuniões de diretoria com vídeo por ano é aproximada. Antecedência da pauta, prazo de publicação das atas, cumprimento do calendário e dados abertos ficaram como 'não medido/não encontrado', não 'não existe'. O bloqueio do Sophia foi do proxy da sessão e pode não afetar um usuário comum.

### ANEEL
- **Reuniões transmitidas** (2): videos.jsonl: 1.110 vídeos de diretoria (2012–2026); 58–103/ano desde 2016 (2024: 103; 2025: 97; 2026 parcial: 55). Exceção: CPDO virtual, sem vídeo. — data/aneel/videos.jsonl; https://www.youtube.com/@aneel
- **Legenda disponível** (2): 930 transcrições; só 44 vídeos sem legenda automática (sem_legenda.jsonl). — data/aneel/transcricoes; data/aneel/sem_legenda.jsonl
- **Pauta antecipada** (1): Pautas publicadas antes das reuniões públicas, mas a base não tem pautas coletadas (sem pasta pautas/; campo pauta nulo no calendario.json); antecedência não medida (não encontrado na base, não inexistente). — https://www.gov.br/aneel/pt-br/reunioes-publicas
- **Atas e votos escritos** (2): Atas e votos dos relatores publicados pela ANEEL; prazo de publicação não medido. — https://www.gov.br/aneel/pt-br/reunioes-publicas; https://biblioteca.aneel.gov.br
- **Calendário anual** (2): Calendário oficial fixado por portaria (Portaria ANEEL nº 7.014, de 3/11/2025); 23 datas na base (RPO e CPDO). Cumprimento não verificado. — data/aneel/calendario.json; https://www.gov.br/aneel/pt-br/reunioes-publicas/calendario; https://www2.aneel.gov.br/cedoc/prt20257014.pdf
- **Composição e currículos** (2): Página oficial da diretoria; base com fichas de dirigentes (foto+bio), mandatos e vacâncias. — https://www.gov.br/aneel/pt-br/composicao; data/aneel/dirigentes; data/aneel/mandatos.json
- **Sigilo e reuniões sem vídeo** (1): 0 de 107 itens analisados com resultado sigiloso; porém os circuitos deliberativos (CPDO) são virtuais e sem transmissão (transmitida=null no calendário). — data/aneel/regulacao.db (tabela itens); data/aneel/calendario.json
- **Facilidade de acesso** (1): Canal e portal com busca, mas documentos divididos entre gov.br e www2.aneel.gov.br/cedoc; 6.600+ vídeos 'outro' no canal dificultam achar as reuniões. — data/aneel/videos.jsonl; https://www.gov.br/aneel
- Observações: Soma 13/16. Não há COMPLETUDE.md nem pasta pautas/ em data/aneel. Base analisada pequena (107 itens). Notas de pauta, atas e composição vêm de conhecimento das páginas oficiais, sem verificação web nesta execução; prazos de publicação não medidos. 36 vídeos de diretoria sem data.

