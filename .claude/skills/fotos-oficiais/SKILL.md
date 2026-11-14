---
name: fotos-oficiais
description: Regras para imagens nos relatórios — retratos de diretores/superintendentes só de páginas oficiais (gov.br, Senado), recorte quadrado 800×800 a partir da MAIOR versão oficial (mínimo 600), fonte registrada; sem foto oficial → iniciais. Fotos de setor só com licença livre (Openverse/Wikimedia) e crédito. Use ao baixar ou trocar qualquer imagem.
---
- Retratos: `docs/marca/diretores/<ag>/<slug>.jpg` (slug sem acento, minúsculo, hífen); `bios.json` → campo `foto` + URL em `fontes`. Nunca redes sociais, notícias ou bancos de imagem para pessoas.
- Setor: agente `curador-fotos`; créditos em `docs/marca/setores/CREDITOS.md`; foco em `foco.json`; `preparar_fotos.py` gera recortes (capa 16:9, painel 2:5, cartão 4:5).
- Peso: relatórios < 1 MB quando possível (cada imagem embutida uma vez).
