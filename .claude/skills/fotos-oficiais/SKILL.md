---
name: fotos-oficiais
description: Regras para imagens nos relatórios — retratos de diretores/superintendentes de gov.br, Flickr oficial, Agência Senado, Agência Brasil (nessa ordem), recorte quadrado 800×800 a partir da MAIOR versão oficial (mínimo 600), fonte registrada; sem foto oficial → iniciais. Fotos de setor só com licença livre (Openverse/Wikimedia) e crédito. Use ao baixar ou trocar qualquer imagem.
---
- Retratos: `docs/marca/diretores/<ag>/<slug>.jpg` (slug sem acento, minúsculo, hífen); `bios.json` → campo `foto` + URL em `fontes`. Nunca redes sociais nem bancos de imagem pagos/de terceiros para pessoas.
- Ordem de fontes para retratos (autorizada pelo dono em 15/11/2026): (1) gov.br/<ag> — composição, notícias e eventos, sempre no tamanho original (`++api++/pt-br/@search?SearchableText="Nome"&metadata_fields=image_scales` → `@@images/image-<largura>-...`, ou `<url>/@@images/image`); (2) Flickr oficial da agência ou do MME; (3) Agência Senado (sabatinas, alta resolução); (4) Agência Brasil/EBC; (5) imprensa setorial só em último caso. Mínimo 600 px na origem; rosto frontal, só a pessoa (recortar fotos de grupo sem pedaços de terceiros); 800×800, qualidade 85; conferir cada recorte visualmente.
- No `<slug>.json`: `foto`, `foto_fonte` (URL), `foto_licenca`, `foto_resolucao_original`, `foto_verificado_em` (+ `foto_nota` com o contexto da imagem). Gravar em `data/<ag>/dirigentes/<slug>.jpg` e `docs/marca/diretores/<ag>/<slug>.jpg`.
- Setor: agente `curador-fotos`; créditos em `docs/marca/setores/CREDITOS.md`; foco em `foco.json`; `preparar_fotos.py` gera recortes (capa 16:9, painel 2:5, cartão 4:5).
- Peso: relatórios < 1 MB quando possível (cada imagem embutida uma vez).
