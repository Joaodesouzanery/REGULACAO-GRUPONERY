# Mapa do repositório (scripts, skills e agentes)

Gerado a partir das descrições de cada arquivo. Para o roteiro de trabalho, veja `docs/CONTINUAR.md`; para o que está completo, `COMPLETUDE.md`.

## Scripts (`pipeline/`)

| Script | O que faz |
|---|---|
| `00_init_db.py` | — |
| `01_coletar.py` | Lista os vídeos de um canal (abas /videos e /streams) -> data/videos.jsonl, com `tipo` e `prioridade`. Uso: 01_coletar.py @canalANTT [anos] (anos=0: s |
| `02_transcrever.py` | Baixa a legenda pt de cada vídeo de data/videos.jsonl -> data/transcricoes/{id}.json [{t, d, x}] (retomável). Ordem: youtube-transcript-api; fallback  |
| `03_preparar.py` | Prepara cada transcrição para leitura/análise: turnos de fala (separados por '>>'), marcadores de pauta e menções normalizadas a diretores. Saída: dat |
| `05_indexar.py` | Carrega data/analise/*.analise.json em data/regulacao.db (tabelas de schema2.sql) e normaliza diretores, temas e categorias de voto. |
| `07_preparar_eventos.py` | Prepara resumos de leitura (data/analise_eventos/<id>.md) de audiências/participativas/workshops/romeiros: abertura (15 min), janelas ±75 s em torno d |
| `agenda_comparativa.py` | Atalho: python3 pipeline/agenda_comparativa.py clientes/<x>/<pasta> (= pipeline/monitoramento.py <pasta> agenda) |
| `alerta_pauta.py` | Alerta pré-pauta (produto D): 1–2 páginas antes da próxima reunião, por cliente. Cruza a pauta publicada (pipeline/pautas.py) com os aliases/temas do  |
| `amostra.py` | Conferência por amostra. Uso: amostra.py sortear / comparar sortear: sorteia (semente fixa) 6 reuniões por ano (2019-2024) e 3 itens por reunião; grav |
| `ata_para_analise.py` | Cria análises a partir de atas oficiais para reuniões SEM vídeo analisado. Uso: bash pipeline/ag.sh anm python3 pipeline/ata_para_analise.py Gera data |
| `auditar.py` | Auditoria da base e dos relatórios entregues. Uso: python3 pipeline/auditar.py [pasta_relatorio ...] Base (ANTT e ANM): integridade referencial, links |
| `auditar_falas.py` | Auditoria automática das falas citadas num documento (skill auditoria-falas). Para cada «trecho literal» seguido de link do YouTube com &t=, confere s |
| `baixar_dou_mac.py` | Baixa do DOU (Seção 2, oficial, via INLABS da Imprensa Nacional) os atos que citam cada diretor — rodar NO MAC. INLABS = serviço oficial e gratuito de |
| `baixar_leis.py` | Baixa do Planalto o texto compilado das leis e converte em docs/leis/<id>.md. O Planalto bloqueia IPs de nuvem (redireciona para gov.br/planalto): ROD |
| `boletim.py` | Boletim mensal da agência (produto à parte): o que a diretoria decidiu no mês, quem divergiu, quem relatou, empresas citadas, diretoria (vagas, mandat |
| `boletim_cliente.py` | Boletim mensal DO CLIENTE (peça 2 do pacote), todo no padrão Grupo Nery (pipeline/design.py): capa · sumário · 01 Na próxima reunião (alerta pré-pauta |
| `checagem_mensal.py` | Checagem do dia 1 (rodar em outro chat todo mês): o que mudou ou precisa conferir na diretoria de cada agência. Uso: python3 pipeline/checagem_mensal. |
| `checar_integridade.py` | Checagem antes de commit (obrigatória; ver .claude/skills/cuidados-pipeline). Uso: python3 pipeline/checar_integridade.py [--atualizar] Falha (código  |
| `cobertura.py` | Gera COBERTURA.md: vídeos publicados x transcritos x analisados, por ano e tipo. Uso: python3 pipeline/cobertura.py |
| `cobertura_resposta.py` | Bloco «Cobertura desta resposta» — rodar antes de TODA resposta sobre diretor/assunto. Uso: python3 pipeline/cobertura_resposta.py <agencia> [diretor] |
| `completude.py` | Painel de COMPLETUDE de todas as agências (2018+): vídeos, diretoria, mandatos, agenda, prazos, comparativa, processos de clientes e qualidade. Gera C |
| `conferencia_eventos.py` | Conferência dos eventos (audiências/participativas/workshops). Uso: conferencia_eventos.py trechos -> confere AUTOMATICAMENTE se cada trecho literal d |
| `consulta.py` | Consulta a base: perfil por diretor/tema, busca de texto e lista de itens com citação (link do YouTube no minuto). Uso: consulta.py perfil "Alex Azeve |
| `cruzar_atas.py` | Cruza as análises (vídeos) com as atas oficiais. Uso: bash pipeline/ag.sh anm python3 pipeline/cruzar_atas.py Entrada: data/atas/indice_atas.json (tip |
| `demo_empresa.py` | DEMO de prospecção (4 páginas, só dado público): mostra o suficiente para a empresa querer o resto. Uso: python3 pipeline/demo_empresa.py <ag> "<Nome  |
| `desfecho.py` | Desfecho de um item para o interessado (empresa): favorável / desfavorável / parcial / neutro. Usa o texto do voto do RELATOR + resultado + resumo, po |
| `design.py` | Sistema de design único dos documentos (padrão Grupo Nery, nov/2026). Cores fixas: azul petróleo #003B4C + lilás #BCCFFF + cinzas. No máximo 2 cores p |
| `dirigentes.py` | Perfis de dirigentes (diretores e superintendentes): fonte canônica em data/<ag>/dirigentes/<slug>.json (+ <slug>.jpg). Uso: python3 pipeline/dirigent |
| `indexar_leis.py` | Indexa docs/leis/**/*.md em data/leis.db (tabela leis + FTS5 leis_fts), quebrando por artigo. Cabeçalho esperado no .md: linhas «# <nome>» e «URL: <ur |
| `iniciar_agencia.py` | Começa uma agência nova em 1 sessão: pasta, raiz virtual, config a partir do modelo, prompts de análise/evento. Uso: python3 pipeline/iniciar_agencia. |
| `mapa_tema.py` | Mapeamento de um assunto por diretor (usado em todo relatório de consultoria): como cada diretor em exercício votou em itens que casam com uma regex ( |
| `marca.py` | Marca comum dos PDFs: parceiro (padrão Circle) + «em parceria com Grupo Nery». Venda só por parceiro revendedor. Uso nos geradores: from marca import  |
| `monitor.py` | Monitor de empresas/temas por cliente (funcionalidade 10). Uso: python3 pipeline/monitor.py [--dias 7] [--cliente X] Config: data/monitor.json (fica n |
| `monitor_8blocos.py` | Documento «Monitoramento de processos: os 8 blocos» para 1–3 processos de um cliente (padrão Grupo Nery, página cheia). Blocos: 1 visão geral · 2 mape |
| `monitoramento.py` | Monitoramento de Processos: documentos 3 e 4 do pacote (mesmo visual do relatório em painel). raio_x → «Raio-X dos Processos» (blocos 1 Visão geral, 2 |
| `organizar.py` | — |
| `painel_dados.py` | Gera os JSONs do painel web (Painel ANTT · ANM) a partir dos bancos. Uso: python3 pipeline/painel_dados.py [pasta_saida] Depois: subir cada JSON como  |
| `pautas.py` | Pautas futuras e calendário (Proposta 2, bloco 4 · Agenda). Só fontes públicas; nada de contornar bloqueio. Uso: python3 pipeline/pautas.py <ag> [--pr |
| `pdf_leve.py` | Deixa os PDFs leves para folhear: sem transparência/blur (camadas que o leitor recompõe a cada página), fontes locais (Inter instalada), véus embutido |
| `pendencias.py` | O que está pendente hoje na operação (usado pelos lembretes). Uso: python3 pipeline/pendencias.py |
| `planilha_cliente.py` | Planilha do cliente (xlsx): todas as decisões que citam a empresa (2018+) com voto de cada diretor, relator, desfecho e link. Uso: python3 pipeline/pl |
| `planilha_votos.py` | Planilha Excel de votos por diretor (ANTT), a partir de data/regulacao.db (rode 05_indexar.py antes). Uso: python3 pipeline/planilha_votos.py [saida.x |
| `prazos.py` | Inteligência de prazo (bloco 3) — processos que passaram por MAIS DE UMA sessão (vista, retirada, retorno): tempo entre a 1ª aparição de um processo n |
| `preparar_fotos.py` | Gera os recortes fixos das fotos de setor para os relatórios (sempre as mesmas imagens, sem corte feio). Uso: python3 pipeline/preparar_fotos.py Entra |
| `previsao.py` | Previsão de votação por diretor (passado × futuro) — usada no relatório por empresa. Ideia simples e auditável: para cada diretor do colegiado atual,  |
| `raio_x.py` | Atalho: python3 pipeline/raio_x.py clientes/<x>/<pasta> (= pipeline/monitoramento.py <pasta> raio_x) |
| `relatorio.py` | Relatório da consultoria (PDF, identidade Grupo Nery) a partir de uma pasta de semana do cliente. Uso: python3 pipeline/relatorio.py clientes/<cliente |
| `relatorio_agencia.py` | Relatório de apresentação de uma agência (PDF Grupo Nery), montado da base. Uso: python3 pipeline/relatorio_agencia.py antt/anm Gera agencias/<ag>/apr |
| `relatorio_diretoria.py` | PDF «Diretoria» de uma agência: quadro atual (foto, formação, minibio, mandato) + comparador (cada página = 1 pergunta com TODOS os diretores lado a l |
| `relatorio_empresa.py` | Relatório por EMPRESA (até 3 agências) — formato do rascunho de 11/2026 (identidade Circle, 16:9). Uso: python3 pipeline/relatorio_empresa.py clientes |
| `relatorio_nery.py` | Relatório da EMPRESA no padrão Grupo Nery (azul + lilás; brochura com divisores de seção e páginas técnicas brancas). Mesmo conteúdo do relatorio_pain |
| `relatorio_painel.py` | Relatório da EMPRESA em formato PAINEL (produto B, design 2026-11): capa com a foto do cliente (sem corte do assunto), painel-resumo (processos · cale |
| `relatorio_v2.py` | Relatório «Circle» (v2): apresentação 16:9, uma ideia por página. Uso: python3 pipeline/relatorio_v2.py <pasta> --titulo "..." [--subtitulo "..."] [-- |
| `secoes_consultoria.py` | Seções de consultoria do relatório (lidas de empresa.json), usadas por relatorio_empresa.py: - temas_consultoria: [{"titulo", "regex", "agencia"?, "de |
| `similares.py` | Casos semelhantes (Proposta 2, bloco 7): os N itens da base mais parecidos com um texto (assunto de pauta, resumo de processo), por busca textual pond |
| `split.py` | — |
| `transparencia.py` | Quadro comparativo de transparência e facilidade das agências (skill transparencia-agencias). Lê data/<ag>/transparencia.json (notas do agente auditor |
| `vacancias.py` | Estatísticas de vacância de cadeira titular a partir de data/vacancias.json. Uso: python3 pipeline/vacancias.py [agencia] Gera agencias/<agencia>/mand |
| `validar.py` | Valida data/analise/*.analise.json: JSON válido e campos mínimos. Uso: validar.py |
| `validar_evento.py` | Valida data/analise_eventos/*.evento.json. Uso: python3 pipeline/validar_evento.py |
| `ag.sh` | Roda qualquer comando do pipeline para uma agência. A ANTT (piloto) usa a raiz (data/); as demais usam data/<sigla>/ através de uma «raiz virtual» dat |
| `baixar_tudo.sh` | Baixa TODAS as transcrições pendentes, sozinho: roda em lotes, envia ao GitHub a cada lote e dorme quando o YouTube limita (429). Uso: caffeinate -i b |
| `coletar_todas.sh` | COMANDO ÚNICO DO MAC: coleta ANTT, ANM e ANTAQ em sequência (só baixa o que falta) e mede o tempo de cada uma. Uso: cd ~/REGULACAO-GRUPONERY && git pu |
| `coletar_tudo_e_enviar.sh` | COLETA TOTAL (rodar no Mac): inventaria TODO o canal (sem corte de ano; videos, streams, shorts e playlists), baixa todas as transcrições que faltam e |
| `instalar_agendamento_mac.sh` | Instala um agendamento semanal (segunda-feira 09:00) no Mac usando launchd. Desinstalar: launchctl unload ~/Library/LaunchAgents/br.antt.monitor.plist |
| `monitorar.sh` | Monitor semanal (Mac): descobre vídeos novos no canal, baixa as transcrições e envia ao GitHub. Uso manual: bash pipeline/monitorar.sh Agendado: bash  |
| `pacote_mensal.sh` | Pacote mensal do cliente (skill pacote-mensal): 4 PDFs + checagens + cópia para entrega/. Uso: bash pipeline/pacote_mensal.sh clientes/<x>/<pasta> AAA |
| `whisper_mac.sh` | TRANSCRIÇÃO POR ÁUDIO (Whisper) das reuniões SEM legenda utilizável — rodar NO MAC (o YouTube bloqueia download na nuvem). Só rode com aprovação do re |

## Skills (`.claude/skills/`)

| Skill | Quando usar |
|---|---|
| **agenda-comparativa** | Gera o documento 4 (agenda e comparativa — blocos 4, 6 e 7) com pipeline/agenda_comparativa.py: próximas pautas, precedentes e contradições da diretoria nos temas do cliente. Use quando pedir «agenda  |
| **agenda-pauta** | Coleta e mostra pautas e calendário oficial das próximas reuniões de diretoria (gov.br) com pipeline/pautas.py. Use quando pedir «próximas reuniões», «pauta da ANTAQ», «quando o item X entra em pauta» |
| **alerta-pre-pauta** | Gera o alerta pré-pauta (produto D) — itens de interesse do cliente na pauta publicada, relator, como cada diretor votou em casos parecidos e previsão rotulada como inferência — com pipeline/alerta_pa |
| **analise-lote** | Analisa em lote as reuniões de diretoria que já têm texto mas ainda não têm .analise.json (qualquer agência; prioridade ANEEL) — fila, workflow de analistas em paralelo, validação, indexação e conferê |
| **atualizar-mandatos** | Importa uma tabela de composição de diretorias (PDF/planilha de terceiros, como o «IRIS Diretorias e mandatos», página da agência ou DOU), compara com data/<ag>/mandatos.json e data/mandatos_agencias. |
| **auditoria** | Auditoria completa da base e dos relatórios — integridade, links no minuto, trechos literais, conferência cega, e afirmação por afirmação das respostas entregues. Use quando o usuário pedir «conferênc |
| **auditoria-falas** | Confere automaticamente cada trecho literal com link no minuto de um documento (HTML do relatório, boletim, raio-X, agenda, demo) contra a transcrição — existe? o minuto bate (±2 min)? Use antes de to |
| **base-legal** | Busca e cita a base legal (leis das agências, Lei 13.848, Lei 9.784, LINDB, LGPD, LAI, conflito de interesses, regimentos internos) com pipeline/consulta.py lei. Use quando a pergunta envolver regra d |
| **boletim-mensal** | Gera o boletim mensal de uma agência (produto premium à parte) — mês em números, decisões por tema, divergências/vistas, quem relatou, empresas em pauta, diretoria (vagas, mandatos), eventos, o que es |
| **calendario-agencias** | Cadastra e mantém o calendário oficial de reuniões de diretoria e as pautas publicadas de TODAS as agências (ANTT, ANM, ANTAQ, ANEEL, ANP) em data/<ag>/calendario.json e data/<ag>/pautas/. Use no dia  |
| **casos-semelhantes** | Lista precedentes (decisões semelhantes) para um item ou processo, com voto de cada diretor, resultado e link no minuto, usando pipeline/similares.py. Use quando pedir «casos parecidos», «precedentes» |
| **checagem-mensal** | Checagem do dia 1 de cada mês — diretoria e superintendentes de cada agência mudaram? (nomeações, reconduções, renúncias, substitutos, vagas). Atualiza mandatos/vacâncias/bios/superintendentes e regen |
| **cobertura-em-toda-resposta** | OBRIGATÓRIA em toda resposta sobre diretor, agência, empresa ou assunto — confere o que a base cobre (reuniões no canal × com texto × analisadas, anos faltando, vídeos sem legenda/Whisper, datas de up |
| **comparar-diretores** | Perguntas que comparam diretores («quem diverge mais», «quem relata concessões», «como cada um vota em X») — resposta sempre com TODOS os diretores em exercício lado a lado (mesmos indicadores), e o P |
| **completude** | Painel de completude de TODAS as agências (ANTT, ANM, ANTAQ, ANEEL, ANP) — vídeos no canal × com texto × analisados, itens e votos, diretoria (foto ≥600, formação, minibio), superintendentes, mandatos |
| **conformidade-entrega** | Etapa 11 do montar-relatorio — checklist de conformidade antes de enviar qualquer PDF ao cliente (clientes/ fora do git, aviso de estimativa, fontes, marca do parceiro + Grupo Nery, autorização de div |
| **consulta-mensal-cliente** | Roteiro da conversa mensal (30 min) com o cliente que gera as perguntas do boletim do mês e atualiza clientes/<x>/<pasta>/processos.json. Use antes de cada ciclo mensal ou quando pedir «preparar a con |
| **contratos** | Gera a minuta de contrato (parceiro revendedor, termos do cliente final e DPA LGPD) a partir de clientes/<x>/contrato.json e dos modelos em proposta2/contrato/; confere com o agente revisor-contratual |
| **controle-diretoria** | Monta e mantém o controle da diretoria por cadeira (como o painel da ANTT) para cada agência — data/<ag>/cadeiras.json com cadeira, ocupantes, nº do mandato, titular/substituto, decreto, posse, saída, |
| **cuidados-pipeline** | Checklist obrigatório antes de qualquer commit/push neste repositório (regulação/diretores). Use sempre que rodar organizar.py, 05_indexar.py, análises por subagente, conferências, ou ao mexer em scri |
| **dados-do-cliente** | Como receber, usar, proteger e apagar dados de processos que o cliente informa (e-mail/planilha → clientes/<x>/<pasta>/processos.json com fonte e sigiloso; raio-X; eliminação no término). Use ao receb |
| **demo-prospect** | Gera o demo de prospecção (4 páginas, só dado público) para uma empresa-alvo com pipeline/demo_empresa.py e a mensagem de LinkedIn que o acompanha. Use quando pedir «demo para a empresa X», «material  |
| **fotos-oficiais** | Regras para imagens nos relatórios — retratos de diretores/superintendentes de gov.br, Flickr oficial, Agência Senado, Agência Brasil (nessa ordem), recorte quadrado 800×800 a partir da MAIOR versão o |
| **lacunas-agencias** | Fecha as lacunas recorrentes de todas as agências — calendário/pautas, fotos e minibios de superintendentes, mandatos ainda não confirmados no DOU e conferência cega pendente (ANEEL) — usando os agent |
| **lote-mac** | O que fazer quando o Mac do usuário envia um lote novo ao GitHub (legendas da coleta, transcrições Whisper, DOU). Use quando o usuário disser «dei push no Mac», «rodei a coleta», «pode analisar o Whis |
| **mapa-assunto** | Mapeia como cada diretor vota num assunto (ex.: reequilíbrio de arrendamento, passivo ambiental) — relatorias, acompanha, diverge, vista, vencido — com pipeline/mapa_tema.py e conferência de falso pos |
| **monitoramento-8-blocos** | Gera o documento «Monitoramento de processos — os 8 blocos» (visão geral, mapeamento, prazo, agenda, agência, busca, comparativa, visão do cliente) para 1–3 processos de um cliente com pipeline/monito |
| **montar-relatorio** | Roteiro-mestre de qualquer relatório de cliente (empresa, temático, boletim) — uma etapa por vez, cada uma com sua skill/agente e critério de «pronto»; só avança quando a etapa anterior passou. Use ao |
| **nova-agencia** | Checklist para iniciar (ou retomar) uma nova agência reguladora no projeto — raiz virtual, config, inventário do canal, coleta no Mac, análise por subagentes, conferência, atas, mandatos, vacância, pa |
| **nova-agencia-energia** | Particularidades para iniciar ANEEL ou ANP — vocabulário técnico (RTP/RTA, bandeiras, MMGD, RAP, CDE, CCEE/PLD, leilões), formatos de reunião (RPO na ANEEL, RD na ANP), filtro de título e checklist. U |
| **nova-agencia-rapida** | Começa uma agência nova em uma sessão (ANEEL, ANAC, ANP, ANATEL, ARTESP…): estrutura, config, prompts, inventário do canal, mandatos/minibios/superintendentes e comando do Mac. Use quando o usuário di |
| **pacote-mensal** | Gera o pacote mensal completo de um cliente (1 relatório da empresa, 2 boletim, 3 raio-X, 4 agenda comparativa + planilha) com todas as checagens (densidade, falas, auditor, guardião) e copia para ent |
| **pagina-cheia** | Regra de densidade e escrita de TODOS os documentos de cliente (relatório da empresa, boletim, raio-X, agenda comparativa, demo) — nenhuma página técnica com espaço sobrando; o espaço livre vira evidê |
| **perfis-dirigentes** | Perfis de diretores e superintendentes (foto oficial, formação, minibio, mandato) guardados no repositório em data/<ag>/dirigentes/ e prontos para qualquer relatório; atualiza quando alguém entra ou s |
| **post-setor** | Cria carrossel (até 10 cards) para Instagram/LinkedIn do Grupo Nery em parceria com a Circle sobre um setor ou agência, só com números agregados e públicos — sem cliente, sem explicar como os dados sã |
| **previsao-voto** | Previsão de voto e placar para um item futuro com pipeline/previsao.py + mapa_tema.py, sempre com backtest, n por diretor e rótulo «inferência». Use quando pedir «como deve votar», «placar provável» o |
| **proposta-comercial** | Prepara o kit de abordagem de um prospect do Grupo Nery — demo de 4 páginas (demo_empresa.py), e-mails da cadência personalizados (proposta2/comercial/emails.md), mensagem de LinkedIn e proposta de 1  |
| **prospeccao** | Monta e atualiza a lista de possíveis clientes do Grupo Nery (empresas reguladas, escritórios, associações, investidores) em proposta2/comercial/prospects.csv/.xlsx, com motivo de interesse tirado da  |
| **qualidade-maxima** | Regime de qualidade reforçado para ANEEL e ANP (prioridade comercial, porta grande de mercado) — conferência cega de 30 itens por lote, auditor em toda entrega, fotos oficiais em alta, revisor-energia |
| **raio-x-processos** | Gera o documento 3 (raio-X dos processos do cliente — blocos 1, 2, 3 e 8) com pipeline/raio_x.py a partir de clientes/<x>/<pasta>/processos.json e prazos.py. Use quando pedir «raio-X dos processos», « |
| **relatorio-cliente** | Gera o relatório da consultoria para um cliente a partir das perguntas da semana (pacote de N perguntas sobre diretores/agências/temas). Use quando o usuário disser «perguntas do cliente X», «relatóri |
| **relatorio-empresa** | Relatório por EMPRESA cliente (até 3 agências: ANTT, ANM, ANTAQ) no formato capa da empresa → processos e calendário → diretoria (minibio, mandato) → decisões setoriais → previsão (placar e % com back |
| **relatorio-visual** | Regras do layout dos relatórios em PDF (identidade Circle, 16:9) — 1 página por pergunta, fotos fixas por setor, peso < 1 MB, conferência por screenshot. Use ao gerar ou mudar relatórios para cliente  |
| **resposta-com-evidencia** | Formato obrigatório (ficha fixa) para responder perguntas sobre diretores de agências — perfil, tema, empresa, divergências, falas, mandatos. Use sempre que o usuário perguntar algo como «o diretor X  |
| **retomar-workflow** | Registra e retoma lotes longos de análise (workflows de analistas, ex.: ANEEL) sem refazer o que já terminou — runId, lista de reuniões e script ficam em docs/lotes.md. Use quando o usuário pedir paus |
| **transparencia-agencias** | Avalia e compara a TRANSPARÊNCIA e a FACILIDADE de acompanhar cada agência reguladora (vídeos das reuniões, legenda, pautas e atas publicadas, calendário, votos por escrito, composição e currículos, s |
| **triagem-eventos** | Classifica eventos (audiências, workshops, participativas) por prioridade antes de analisar — alta (audiência/consulta pública, leilão, tarifa, resolução), média, baixa (encerramento de P&D, internaci |
| **vacancia-agencia** | Mantém sempre atualizado o tempo de vacância de diretoria (cadeira titular vaga) de cada agência reguladora — média, mediana, máximo, vagas em aberto e % de dias-cadeira vagos — e o comparativo entre  |

## Agentes (`.claude/agents/`)

| Agente | Função |
|---|---|
| **analista-evento** | Analisa UM evento público (audiência pública, reunião participativa, workshop) a partir da transcrição e grava o .evento.json validado — falas de diretores, temas, pedidos dos participantes, com minut |
| **analista-prazos** | Calcula prazos de tramitação com pipeline/prazos.py — mediana e faixa por tipo de processo — e compara um processo do cliente com ≥ 20 semelhantes. Use no bloco 3 do raio-x-processos ou quando pergunt |
| **analista-reuniao** | Analisa UMA reunião de diretoria (ou uma parte dela) a partir do .md preparado e grava o .analise.json validado. Use para lotes novos (legendas do Mac, Whisper, nova agência) — um subagente por reuniã |
| **analista-tema** | Escolhe a regex de um assunto (ex.: reequilíbrio de arrendamento, passivo ambiental), roda pipeline/mapa_tema.py e confere 10 itens contra falso positivo até precisão ≥ 90%. Use na etapa 4 do montar-r |
| **auditor-previsao** | Confere qualquer previsão de voto/placar em relatório — backtest refeito, n por diretor, regex/mapa de tema e rótulo «inferência». Use antes de entregar relatório com previsão (skill previsao-voto, et |
| **auditor-respostas** | Audita um relatório de cliente já escrito — confere cada afirmação (número, tendência, evidência citada) contra a base com SQL próprio e marca confirmada / imprecisa / sem base / inferência. Use antes |
| **auditor-transparencia** | Avalia a transparência e a facilidade de acompanhar UMA agência reguladora pelos critérios da skill transparencia-agencias (transmissão, legenda, pauta, atas, calendário, composição, sigilo, facilidad |
| **conferente-cego** | Conferência cega por amostra — relê itens sorteados direto da transcrição, SEM ver a base nem as análises, e grava respostas para pipeline/amostra.py comparar. Use em rodadas de qualidade (nova agênci |
| **curador-fotos** | Busca, avalia e propõe fotos genéricas de setor (Openverse/Wikimedia, licença livre) para os relatórios — 2 opções por setor no padrão editorial numa folha de contato, sem marcas, pessoas em destaque  |
| **detector-contradicao** | Encontra possíveis contradições da diretoria — mesmo tema com desfecho oposto em menos de 24 meses — e compara as justificativas lado a lado, rotulando como inferência. Use no bloco 7 (agenda-comparat |
| **guardiao-dados-cliente** | Antes de cada entrega ou commit, confere que dados de cliente não vazam — nada de clientes/ no git, materiais públicos (proposta2/marketing, demos) sem processos/CNPJs/estratégia de cliente, e process |
| **pesquisador-calendario** | Encontra o calendário oficial de reuniões de diretoria e as pautas publicadas de uma agência reguladora (gov.br), com data, número, formato e URL de fonte, e devolve no formato de data/<ag>/calendario |
| **pesquisador-dirigentes** | Levanta os superintendentes (e diretores) de uma agência nas páginas oficiais do gov.br (composição/quem é quem), baixa retratos oficiais e minicurrículos, e grava o perfil canônico em data/<ag>/dirig |
| **pesquisador-empresa** | Levanta dados públicos de uma empresa cliente — CNPJ, razão social, grupo econômico, aliases, contratos com a agência, terminais/concessões — sempre com fonte, e grava clientes/<x>/<pasta>/empresa.jso |
| **pesquisador-juridico** | Atualiza as bases legais citadas nos modelos de contrato (LGPD, resoluções da ANPD, Lei 9.609/9.610, 12.846, 12.813, termos do YouTube) com fonte oficial e data. Use a cada 6 meses ou quando a ANPD pu |
| **pesquisador-mandatos** | Pesquisa mandatos de diretores de uma agência (nome completo, aprovação no Senado, nomeação/posse no DOU, fim legal, renúncia, substitutos) com fontes, no formato de data/[<sigla>/]mandatos.json. Use  |
| **pesquisador-prospects** | Levanta empresas-alvo por setor/agência para o Grupo Nery e seus contatos institucionais públicos (site, fale-conosco, RI, LinkedIn da empresa), com fonte, e o motivo de interesse a partir da base de  |
| **pesquisador-tcu** | Levanta acórdãos do TCU sobre uma agência reguladora e um tema (fiscalização de outorgas, tarifas, leilões, concessões), com nº/ano, relator, data, síntese e URL oficial. Use para enriquecer relatório |
| **redator-demo** | Escreve o gancho e a mensagem de LinkedIn para uma empresa-alvo a partir do demo gerado (demo-prospect), só com dado público e sem nenhum dado de cliente. Use depois de gerar o demo. |
| **revisor-comercial** | Revisa material comercial e de marketing do Grupo Nery (apresentação, one-pager, e-mails, posts, planilha de prospects) — não pode citar ferramenta, repositório, método de coleta («YouTube», «legenda» |
| **revisor-contratual** | Confere uma minuta de contrato (parceiro, cliente final, DPA) ou uma entrega (PDF/MD) contra proposta2/contrato/checklist_contrato.md, item por item, com evidência. Use antes de enviar minuta ou entre |
| **revisor-energia** | Confere termos técnicos de tarifa, leilão, transmissão, petróleo e gás (RTP/RTA, bandeiras, MMGD, RAP, CDE, CCEE/PLD, oferta permanente, partilha) em entregas da ANEEL e da ANP, apontando uso errado o |
| **revisor-visual** | Revisa visualmente um relatório em PDF/HTML gerado por pipeline/relatorio_v2.py — abre os screenshots de cada página e aponta corte feio de foto, texto estourando, cartões vazios, números incoerentes  |
