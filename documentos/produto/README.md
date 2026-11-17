# Proposta 2 — «Radar Regulatório» (pasta só de documentos)

**Ideia.** O mesmo repositório gera uma família de entregas: relatórios, alertas, boletins, planilhas e, se fizer sentido, um painel privado. O cliente recebe as entregas, e a coleta, a análise e a base ficam com o operador. A lógica é **monitorar, analisar e antecipar**.

## Cabe tudo no repositório? Sim, com 3 regras
1. **Dados públicos, scripts e skills ficam no GitHub, que é privado.** São dezenas de MB por ano por agência.
2. **As bases e os PDFs pesados são gerados fora do git;** a base se reconstrói em cerca de 10 segundos.
3. **Dados de cliente (processos, CNPJ, intimações) nunca entram no repositório principal:** ficam em `clientes/` ou num repositório privado separado.

## Fontes
YouTube (Mac) · pautas e atas no gov.br · DOU (INLABS) · SEI só via o que o cliente informa ou o que for público sem burlar bloqueios (CAPTCHA nunca é contornado) · LAI para séries históricas.

## Documentos
- `catalogo_entregas.md` — o que se vende
- `modelo_comercial.md` — planos, boletim à parte, parceiro, contrato
- `operacao.md` — rotina e lembretes automáticos
- `roadmap.md` — ordem de construção
- `situacao_dados.md` — o que já temos de ANTT, ANTAQ e ANM
- `como_comecar.md` — os 8 blocos → entregas → primeiro passo de cada um

## O que já existe (≈ 60% da inteligência)
Quadro da diretoria e comparador, minibios/superintendentes, mandatos/vacâncias, 3 agências com votos e trechos, desfecho por empresa, previsão de placar com backtest, relatório por empresa, cobertura em toda resposta. **Falta:** coleta diária de pautas, alerta de processo, cálculo de prazos por tipo e casos semelhantes.
