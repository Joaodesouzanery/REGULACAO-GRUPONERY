# Checklist contratual (usado pelos agentes `revisor-contratual` e skill `conformidade-entrega`)

> **MODELO PARA REVISÃO POR ADVOGADO.** Não é aconselhamento jurídico. Cada item é verificado e marcado OK / FALHA / N.A. com evidência (arquivo e linha).

## A. Minuta (contrato parceiro ou cliente)
1. Topo diz «modelo para revisão por advogado».
2. Objeto = licença das ENTREGAS; MOTOR (código, base, metodologia, prompts) excluído.
3. Proibição de engenharia reversa e de reconstrução da base (Lei 9.609/1998; Lei 9.610/1998, art. 7º, XIII).
4. White label com «tecnologia Grupo Nery» obrigatória e não removível.
5. Divisão 50/50 sobre receita líquida; quem fatura, prazo de repasse e NF definidos.
6. Preço mínimo de revenda = tabela do Anexo I; nota antitruste ao advogado presente.
7. Preço de fundador limitado a 2 clientes e 12 meses; transição para tabela cheia com aviso.
8. Reajuste anual pelo IPCA; multa, juros e suspensão por inadimplência.
9. Não concorrência e não aliciamento com prazo, objeto e território; exclusividade opcional ligada a metas.
10. PI: MOTOR do Grupo Nery; trechos públicos não apropriados.
11. Fontes públicas e limites (legenda automática, sigilosos, reuniões sem vídeo, taxa de conferência).
12. Previsões = estimativas; não substituem intimação ou publicação oficial nem orientação jurídica.
13. Teto de responsabilidade = 12 meses pagos; exclusão de dolo e culpa grave da limitação.
14. Integridade: só fonte pública; Lei 12.846/2013 e Lei 12.813/2013 citadas.
15. LGPD: DPA anexo; papéis definidos; bases do art. 7º, §§3º-4º e IX.
16. Incidente: operador → controlador em 24 h; ANPD em 3 dias úteis (Res. CD/ANPD 15/2024).
17. Confidencialidade de 5 anos após o término.
18. SLA: boletim até o dia 5; alerta pré-pauta 24 h antes (se pauta publicada); perguntas/mês.
19. Vigência de 12 meses, renovação, aviso de 30–60 dias, multa ≤ saldo, efeitos do término.
20. Uso de marca/caso do cliente só com autorização escrita.
21. Lei brasileira, mediação prévia, foro.
22. Nenhum campo `{{ }}` sem preencher; valores batem com `contrato.json` e com `proposta2/modelo_comercial.md`.

## B. Cada entrega (PDF) antes de enviar
23. Arquivo gerado de `clientes/<x>/`, que está fora do git (`git check-ignore clientes/`).
24. Aviso de estimativa nas páginas de previsão, placar ou prazo, com rótulo «inferência», backtest e n por diretor.
25. Toda afirmação tem fonte: reunião, item, trecho literal, link `&t=`; informação do cliente marcada «informado pelo cliente».
26. Bloco de cobertura e taxa de conferência por amostra cega presentes.
27. Limites declarados (legenda automática, sigilosos, reuniões sem vídeo).
28. Marca do parceiro + «tecnologia/em parceria com Grupo Nery».
29. Nenhum juízo pessoal sobre diretor; nenhuma informação não pública.
30. Dados pessoais restritos à função pública; dados do cliente só no que ele contratou.
31. Entrega dentro do SLA do plano (data registrada em `clientes/<x>/entrega.md`).
32. Material de divulgação derivado: autorização escrita do cliente arquivada, ou versão anônima sem elementos identificáveis.
