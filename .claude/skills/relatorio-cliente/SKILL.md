---
name: relatorio-cliente
description: Gera o relatório da consultoria para um cliente a partir das perguntas da semana (pacote de N perguntas sobre diretores/agências/temas). Use quando o usuário disser «perguntas do cliente X», «relatório da semana», «dossiê pré-pauta» ou colar perguntas de cliente.
---
# Relatório para cliente (consultoria)

1. Salve as perguntas em `clientes/<cliente>/<AAAA-semNN>/perguntas.md`, uma por linha: `- texto [diretor: Nome] [tema: onibus] [setor: rodovias]` (temas: `consulta.py temas`; setor = nome da imagem em `docs/marca/setores/`). `clientes/` NÃO vai para o GitHub.
2. Para cada pergunta, gere a ficha (`consulta.py ficha`, skill `resposta-com-evidencia`) em `respostas/NN.md` e **reescreva a «Resposta curta»** com o padrão de mérito lido nas evidências (o texto automático é só rascunho). Revise trechos e links.
3. `python3 pipeline/relatorio.py clientes/<cliente>/<AAAA-semNN> --titulo "..." [--agencia anm]` → `relatorio.pdf` (identidade Grupo Nery: capa, Conteúdo I/II/III, KPIs, gráfico, tabela de evidências com trecho literal e link no minuto, contra-exemplos, metodologia). Confira as páginas por screenshot antes de entregar.
4. Entregue o PDF ao usuário (ele é quem envia ao cliente). Registre no `clientes/<cliente>/historico.md` o que foi entregue.
5. Nunca invente: sem dado → diga que não temos e por quê (cobertura em `COBERTURA.md`).
