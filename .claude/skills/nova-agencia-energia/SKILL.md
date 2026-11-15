---
name: nova-agencia-energia
description: Particularidades para iniciar ANEEL ou ANP — vocabulário técnico (RTP/RTA, bandeiras, MMGD, RAP, CDE, CCEE/PLD, leilões), formatos de reunião (RPO na ANEEL, RD na ANP), filtro de título e checklist. Use junto com nova-agencia-rapida quando a agência for de energia.
---
## Formatos
- **ANEEL**: Reunião Pública Ordinária (**RPO**) semanal, extraordinárias e sessões de **sorteio** (não analisar sorteio como deliberação). Sem playlist: filtrar o canal pelo título `Reuni[ãa]o P[úu]blica (Ordin|Extraordin)`. Reuniões longas (3–8 h) com sustentação oral.
- **ANP**: Reunião de Diretoria Colegiada (**RD**, numerada, ~nº 1193 em out/2026) — playlist «Reuniões de Diretoria»; o termo interno pode aparecer como **ROD** (ordinária) — aceitar `RD|ROD|Reuni[ãa]o de Diretoria`.
- Ver `proposta2/novas_agencias.md` (canais, playlists, composição a confirmar).

## Vocabulário (para prompts, temas e `revisor-energia`)
- **RTP** revisão tarifária periódica; **RTA** reajuste tarifário anual; **RTE** revisão extraordinária.
- **Bandeiras tarifárias** (verde/amarela/vermelha 1 e 2, escassez hídrica).
- **MMGD** micro e minigeração distribuída (Lei 14.300/2022).
- **RAP** receita anual permitida (transmissão); **CDE** Conta de Desenvolvimento Energético; **CCEE** câmara de comercialização; **PLD** preço de liquidação das diferenças; **MRE/GSF** risco hidrológico.
- Leilões: A-x de energia nova/existente, LRCAP (reserva de capacidade), transmissão (deságio sobre RAP). ANP: rodadas de licitação, **oferta permanente**, partilha, conteúdo local, UTGN, revenda de combustíveis, autorização de agentes.
- Caducidade, intervenção, termo de intimação e auto de infração aparecem em ambas.

## Checklist (além da nova-agencia-rapida)
1. Temas iniciais em config: tarifa, bandeira, MMGD, transmissão/RAP, leilão, caducidade, fiscalização, CDE (ANEEL); exploração, leilão, combustíveis, gás, fiscalização (ANP).
2. Prompt de análise com o glossário acima e aviso: valores (R$, %) da legenda **sempre** conferir em voto escrito/ata.
3. Piloto 2025–26 antes de todo o período.
4. Mandatos com `pesquisador-mandatos` (composição em `novas_agencias.md` está «a confirmar»).
5. Aplicar a skill `qualidade-maxima` (ANEEL/ANP são prioridade comercial).
