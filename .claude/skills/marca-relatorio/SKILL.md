---
name: marca-relatorio
description: Regra de marca em TODO documento de cliente ou prospect (relatório, demo, radar, alerta, boletim) — perguntar ao usuário qual parceiro vai na capa (IRIS, Circle ou só Grupo Nery) ANTES de gerar; Grupo Nery sempre presente. Use antes de rodar qualquer gerador de PDF.
---
# Marca nos documentos
1. **Antes de gerar, pergunte ao usuário** (AskUserQuestion): «IRIS + Grupo Nery», «Circle + Grupo Nery» ou «só Grupo Nery». Não presuma pelo cliente anterior.
2. No código: `design.MARCA = "iris" | "circle" | "nery"` (capa, cabeçalho e encerramento usam a logo real). Geradores aceitam `--marca`.
3. Logos oficiais: `docs/marca/iris/logo_iris_branco.png` (fundo escuro) e `logo_iris_azul.png` (fundo claro); `docs/marca/circle/`; `docs/marca/grupo_nery/`. **Nunca desenhar logo em texto.** Logo nova: salvar o arquivo enviado pelo usuário nessa pasta.
4. Grupo Nery aparece sempre, menor que a marca parceira (exceto quando é só Grupo Nery).
