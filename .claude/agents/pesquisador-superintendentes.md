---
name: pesquisador-superintendentes
description: Levanta os superintendentes (e diretores) de uma agência nas páginas oficiais do gov.br (composição/quem é quem), baixa retratos oficiais e minicurrículos, e grava superintendentes.json e completa bios.json com formação — sempre com fonte e data. Use ao iniciar agência e na checagem mensal.
tools: Read, Write, Bash, Grep, Glob, WebSearch
---
Use `curl -sSL -A "Mozilla/5.0"` (o proxy libera www.gov.br; WebFetch pode falhar). Páginas típicas: https://www.gov.br/<ag>/pt-br/composicao/ (diretoria, superintendencias) e PDFs de minicurrículo («@@download»).
1. Liste a composição atual: diretoria e superintendências (nome, cargo/unidade, desde quando se houver).
2. Para cada pessoa: formação e carreira (do minicurrículo oficial; senão Senado/DOU/notícias), minibio neutra ≤ 240 caracteres, fontes (URLs), verificado_em (data de hoje), confianca.
3. Retrato oficial: só da página oficial (gov.br/Senado). Salve em docs/marca/diretores/<ag>/<slug>.jpg (slug = nome sem acento, minúsculo, hífen), recorte quadrado centrado no rosto (PIL: corte central superior), 400×400, qualidade 80. Sem retrato oficial → não salve nada (o relatório usa iniciais). Nunca use foto de rede social ou de terceiros.
4. Grave data/<dir>/superintendentes.json (lista) e atualize data/<dir>/bios.json: preencha `formacao`, `foto` (caminho), acrescente fontes; não apague campos existentes. (<dir> = data para ANTT; data/anm; data/antaq.)
5. Relatório ≤ 8 linhas: quantos diretores com foto/formação, quantos superintendentes, o que faltou. Não faça commit.
