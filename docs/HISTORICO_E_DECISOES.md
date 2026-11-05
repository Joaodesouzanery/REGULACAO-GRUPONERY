# Histórico e decisões (substitui a memória da conversa)

## Objetivo e pedidos permanentes do dono
- Piloto ANTT (canal @canalANTT); depois outras agências. Perfis analíticos por diretor e tema, com evidência e link no minuto.
- Incluir TODOS os tipos de vídeo: diretoria (ordinárias e extraordinárias), audiências, participativas, workshops, Caminho dos Romeiros. Análises até 2019 no máximo.
- Sem chave de API da Anthropic: a análise é feita por Claude e subagentes.
- Tudo no GitHub, organizado por agência/ano/tipo/diretor (`agencias/antt/`); sempre avisar o que não tem transcrição (`sem_transcricao.md`).
- Monitorar reuniões novas (Mac + tarefa semanal na nuvem).
- Mandatos: nomeação, início e fim estimado, vacância (média por agência).
- Conferência por amostra das análises antigas.

## Decisões técnicas
- Votos: relator, acompanha, revisor_acompanha, revisor_diverge, vista, vencido, nao_captado, outro.
- Taxonomia de temas por regex em `pipeline/05_indexar.py`. Trechos em janelas de 30 s com FTS5.
- Marcelo Fonseca só conta como diretor votante a partir de 2026-08 (antes era superintendente). Em 2025, Alessandro Baumgarten e Marcelo Fonseca eram superintendentes.
- Duplicatas PT/EN e reuniões repetidas ficam em `data/analise/_duplicadas/`; datas corrigidas em `data/datas_manuais.json`.
- Eventos: pré-filtro (`07_preparar_eventos.py`) + subagentes; a data usada é a falada no encerramento quando difere do título (anotado em `limites_da_analise`). A maioria das audiências não tem fala de diretor: falam superintendentes, gerentes e ouvidores.
- Mandatos de 5 anos; substitutos até 180 dias; estatística de vacância em `pipeline/vacancias.py` (ANTT: 9 eventos, média 211 d, mediana 191 d).

## Qualidade
Amostra cega (108 itens, 2019–2024, semente 20261103): concordância ≈ 93% (relator 93,5%, resultado 92,6%, voto por diretor 93,5%). Mede consistência, não verdade absoluta. Não cobre 2025–2026 nem eventos.

## Erros já corrigidos (não repetir)
Duplicatas somando votos; datas erradas pelo título; Marcelo Fonseca contado em 2021; comparação relator × acompanha com regex errada; limite de uso dos subagentes (HTTP 429): retomar o mesmo agente com SendMessage depois do reset.

## Pendências conhecidas
Ver «Pendências» em `docs/CONTINUAR.md` (eventos de 2023 e anteriores, posses oficiais 2019–2022, nomes incertos como «Menezes», 4 reuniões de diretoria sem texto utilizável, outras agências).
