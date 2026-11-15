---
name: conformidade-entrega
description: Etapa 11 do montar-relatorio — checklist de conformidade antes de enviar qualquer PDF ao cliente (clientes/ fora do git, aviso de estimativa, fontes, marca do parceiro + Grupo Nery, autorização de divulgação, LGPD). Use sempre antes de enviar uma entrega ou publicar material derivado.
---
Base: seção B de `proposta2/contrato/checklist_contrato.md` (itens 23–32). Resultado em `clientes/<x>/entrega.md`.

1. `git check-ignore -q clientes/ && echo ok` — se falhar, **parar**. `git status --porcelain | grep clientes/` deve vir vazio.
2. Aviso de estimativa: toda página com previsão, placar ou prazo traz «inferência», backtest e n por diretor (agente **auditor-previsao**).
3. Fontes: toda afirmação com reunião, item, trecho literal e link `&t=`; o que o cliente informou vem marcado «informado pelo cliente» (agente **auditor-respostas**: 0 «sem base»).
4. Cobertura e taxa da conferência cega presentes; limites declarados (legenda automática, sigilosos, reuniões sem vídeo).
5. Marca: capa com marca do parceiro + «tecnologia/em parceria com Grupo Nery».
6. Divulgação: post, caso ou citação do cliente só com autorização escrita arquivada (`contrato.json → autorizacao_divulgacao`); senão, só versão anônima.
7. LGPD: dados pessoais restritos à função pública; sem juízo pessoal; sem informação não pública; dados do cliente só no que ele contratou.
8. SLA: data de entrega dentro do prazo do plano.
9. Rodar o agente **revisor-contratual** sobre o PDF. Gravar a tabela OK/FALHA/N.A. com evidência em `entrega.md`. Só enviar com 0 FALHA.
