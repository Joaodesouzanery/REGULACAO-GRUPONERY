---
name: proposta-comercial
description: Prepara o kit de abordagem de um prospect do Grupo Nery — demo de 4 páginas (demo_empresa.py), e-mails da cadência personalizados (proposta2/comercial/emails.md), mensagem de LinkedIn e proposta de 1 página — e confere com o revisor-comercial. Use quando pedirem «material para a empresa X», proposta ou e-mail de prospecção.
---
# Proposta comercial
1. Prévia completa (e-mail 2): `python3 pipeline/previa_completa.py <ag> "<Empresa>" "<aliases>" [--foto] [--logo]` → `clientes/_prospeccao/<slug>/previa/previa_completa.pdf`. Prévia curta (LinkedIn): `python3 pipeline/demo_empresa.py <ag> "<Empresa>" "<aliases>"`. Confira densidade e falas (`auditar_falas.py`).
2. Preencha os modelos de `proposta2/comercial/emails.md` com 3 fatos do demo (nº de decisões, tema com divergência, próximo mandato a vencer).
3. Material institucional: `proposta2/comercial/apresentacao_grupo_nery.pdf` (ou one-pager); gerar com `python3 pipeline/apresentacao_nery.py [--one-pager]`.
4. Agente `revisor-comercial` antes de enviar. Tudo do prospect fica em `clientes/_prospeccao/<slug>/` (fora do git).
