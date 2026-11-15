---
name: demo-prospect
description: Gera o demo de prospecção (4 páginas, só dado público) para uma empresa-alvo com pipeline/demo_empresa.py e a mensagem de LinkedIn que o acompanha. Use quando pedir «demo para a empresa X», «material para prospectar Y» ou antes de abordar um lead.
---
- `python3 pipeline/demo_empresa.py <ag> "<nome da empresa>" "<alias1|alias2>"` (aliases = regex de grafias, siglas e SPEs; a legenda automática erra nomes).
- Conteúdo fixo: 4 páginas — capa da empresa; decisões públicas que a citam (reunião, item, link `&t=`); diretoria com **1 diretor aberto** (o mais ligado aos itens) e os demais **desfocados**; página de previsão **oculta** (só o título e «disponível no relatório completo»).
- Regras: só dado público (nada de `clientes/`); marca d'água **DEMO** em todas as páginas; rodapé «válido por 30 dias a partir de <data>»; bloco de cobertura no fim; aviso de legenda automática.
- Conferir: os itens citados são mesmo da empresa (falso positivo do alias)? n ≥ 3 itens, senão avisar que o demo fica fraco e sugerir outra agência ou empresa.
- Mensagem de LinkedIn: chamar o agente `redator-demo` (gancho a partir do demo, até 600 caracteres, sem prometer previsão, sem citar cliente).
- Pronto quando: PDF < 1 MB, 4 páginas, revisado pelo `revisor-visual`, mensagem pronta, e passou na `conformidade-entrega`. O PDF fica fora do git.
