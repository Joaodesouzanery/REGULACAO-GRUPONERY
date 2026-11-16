---
name: pagina-cheia
description: Regra de densidade e escrita de TODOS os documentos de cliente (relatório da empresa, boletim, raio-X, agenda comparativa, demo) — nenhuma página técnica com espaço sobrando; o espaço livre vira evidência (falas literais com link no minuto, votos, precedentes); travessão só onde precisa. Use ao gerar, revisar ou mudar qualquer PDF de cliente.
---

# Página cheia (densidade e escrita)

## Regra
- Página técnica (fundo branco) não pode ter mais de **1,4 pol vazias** no pé, nem conteúdo passando do pé.
- `design.documento()` mede isso sozinho (`design.densidade()`) e imprime `AVISO densidade` ou `AVISO estouro` com o número da página. Os scripts que não usam `documento()` (`monitoramento.py`, `demo_empresa.py`) chamam `dz.densidade(<html>)` no fim.
- Só entregue sem nenhum aviso. `densidade(html, estrito=True)` faz a geração falhar.

## Como preencher (nesta ordem; nunca com enfeite)
1. **Falas literais com minuto**: trecho da legenda do voto (relator primeiro), com `▶ minuto`. Use o helper de cada script: `falas()` em monitoramento/demo, `falas_itens()` no boletim, `decs_html()` no relatório. Elimine trechos repetidos.
2. **Votos por diretor**: `matriz()` do relatório (sessão × diretor), com link da sessão.
3. **Precedentes**: `similares.similares()` (casos parecidos com desfecho e justificativa).
4. **Contexto da base**: números da base, quem relatou, empresas em pauta.

## Como cortar (quando estoura)
- Reduza o nº de linhas da tabela de falas, ou divida a tabela em páginas iguais (nunca uma página com 2 linhas).
- Não corte texto no meio da palavra (`[:95]`); prefira dividir a página.

## Escrita (não parecer IA)
- **Travessão «—» só onde precisa** (célula vazia de tabela). No texto use vírgula, dois-pontos, ponto ou parênteses.
- Sem frases genéricas; cada afirmação com reunião, item, trecho e link.
- Rótulos de desfecho: «a favor da empresa», «em parte», «sem efeito direto», «contra a empresa», «sem decisão ainda», com a definição em nota.

## Conferência
- `pdftotext <pdf> - | grep -c "—"`: o resultado deve ser baixo (só tabelas e textos da legenda).
- Screenshots de todas as páginas, conferidos pelo agente `revisor-visual`.
