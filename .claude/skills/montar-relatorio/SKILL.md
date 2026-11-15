---
name: montar-relatorio
description: Roteiro-mestre de qualquer relatório de cliente (empresa, temático, boletim) — uma etapa por vez, cada uma com sua skill/agente e critério de «pronto»; só avança quando a etapa anterior passou. Use ao começar qualquer relatório para cliente.
---
| # | Etapa | Skill / agente | Pronto quando |
|---|---|---|---|
| 0 | Briefing: `clientes/<x>/<pasta>/empresa.json` (nome, CNPJ, aliases, agências, `temas_consultoria`, `item_antecipado`, `contrato_foco`, `logo`) | agente general-purpose como pesquisador-empresa (CNPJ, grupo, contratos, com fonte) | CNPJ e aliases com fonte ou «a confirmar» |
| 1 | Cobertura | cobertura-em-toda-resposta | lacunas do período listadas |
| 2 | Reuniões novas | lote-mac · analista-reuniao / analista-evento | validar.py ok |
| 3 | Diretoria, superintendentes, mandatos, fotos | perfis-dirigentes, vacancia-agencia, fotos-oficiais · pesquisador-dirigentes / pesquisador-mandatos | `dirigentes.py faltas` vazio ou justificado |
| 4 | Mapeamento por assunto (como cada diretor vota) | `python3 pipeline/mapa_tema.py <ag> "<regex>"` — conferir 10 itens da lista contra falso positivo | ≥ 90% dos itens corretos |
| 5 | Casos semelhantes / outras iniciativas | mesma lista do mapa_tema (seção «decisões semelhantes») | ≥ 5 precedentes com link |
| 6 | Previsão de voto | previsao.py + mapa_tema (prior 97%, peso 10) | backtest e n por diretor no texto; rótulo «inferência» |
| 7 | Pauta e calendário (item retirado/vista, próximas reuniões) | calendário oficial no gov.br; transcrição da última reunião com minuto | data oficial com fonte; o que o cliente informou × o que o vídeo mostra, separados |
| 8 | Montagem | relatorio_empresa.py (+ secoes_consultoria.py) / relatorio_v2.py / boletim.py · relatorio-visual | < 1 MB; marca do parceiro + «em parceria com Grupo Nery» |
| 9 | Auditoria | auditoria · auditor-respostas | 0 afirmações «sem base» |
| 10 | Revisão visual | revisor-visual (screenshots) | 0 estouros |
| 11 | Conformidade | `clientes/` fora do git; aviso de estimativa; LGPD; fonte de toda informação do cliente marcada | checklist em clientes/<x>/entrega.md |
Regra: informação recebida do cliente («retirado para análise do DG») aparece como tal e é confrontada com o vídeo; nunca chamar de «privilegiada» o que é público.
