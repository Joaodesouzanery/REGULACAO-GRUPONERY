---
name: relatorio-visual
description: Regras do layout dos relatórios em PDF (identidade Circle, 16:9) — 1 página por pergunta, fotos fixas por setor, peso < 1 MB, conferência por screenshot. Use ao gerar ou mudar relatórios para cliente ou apresentações de agência.
---
# Relatório visual (Circle v3)

Gerar: `python3 pipeline/relatorio_v2.py <pasta> --titulo "…" --subtitulo "…" --agencia <sigla> [--sem-marca] [--anexo]`.

- **Estrutura**: capa (foto do setor da agência + cartão translúcido) · sumário em 1 página (grade 5×2) · **1 página por pergunta** (faixa de foto à esquerda; pergunta, resposta curta ≤ 400 caracteres, 3 números, mini-gráfico ≤ 5 barras, 2 evidências com «assistir no minuto») · «Como ler» · anexo opcional. 10 perguntas ≈ 13 páginas.
- **Fotos**: sempre as mesmas por setor, genéricas, licença livre (créditos em `docs/marca/setores/CREDITOS.md`). Recortes prontos em `docs/marca/setores/recortes/` gerados por `pipeline/preparar_fotos.py` a partir de `foco.json` (ponto focal, área a evitar — ex.: carimbo de data —, cor do setor). Nunca use a foto original direto: o recorte já tem a proporção exata (16:9 capa/sumário, 2:5 faixa), então não há corte feio.
- **Cor por setor** (`foco.json`): rodovias âmbar, ônibus azul-petróleo, ferrovias vermelho, mineração terracota, portos/navegação azul-marinho. Base Circle: preto #0B0B0B, branco, dourado #C99A06.
- **Setor nova**: baixar foto horizontal ≥ 1600 px, sem pessoas em destaque, sem marca d'água/data; adicionar a `foco.json` e `CREDITOS.md`; rodar `preparar_fotos.py`; olhar o recorte.
- **Conferir sempre**: nº de páginas, tamanho (< 1 MB), screenshots (capa, sumário, 2 perguntas de setores diferentes) e checagem de overflow. Números do KPI vêm do texto/base — cuidado com regex («favorável» casa dentro de «desfavorável»: use `(?<!des)`).
- Antes de entregar: subagente `auditor-respostas`.
