# Proposta 2 — «Radar Regulatório» (avaliação; nada implementado ainda)

**Ideia:** o mesmo repositório (motor) gera uma família de entregas para clientes e parceiros — relatórios, alertas, boletins, planilhas e, se fizer sentido, um painel privado. O cliente recebe as entregas; o motor (coleta, análise, base, conferência) fica com o operador. Monitorar → Analisar → Antecipar.

## Cabe tudo no repositório? Sim, com 3 regras
1. **Público e motor no GitHub:** transcrições, análises, votos, quem é quem, pautas, DOU, scripts, skills (dezenas de MB/ano por agência).
2. **Gerados fora do git:** bases SQLite (reconstruídas em ~10 s) e PDFs pesados (só em marcos).
3. **Dados de cliente nunca no repositório público:** processos monitorados, CNPJs, intimações e entregas ficam em `clientes/` (já fora do git) ou num repositório privado `clientes-privado` que só lê o motor.

## Fontes
YouTube (Mac) · pautas e atas no gov.br · DOU (INLABS) · SEI só via o que o cliente informa ou o que for público sem burlar bloqueios (CAPTCHA nunca é contornado) · LAI para séries históricas.

## Documentos
- `catalogo_entregas.md` — o que se vende
- `modelo_comercial.md` — planos, boletim à parte, parceiro, contrato
- `operacao.md` — rotina e lembretes automáticos
- `roadmap.md` — ordem de construção

## O que já existe (≈ 60% da inteligência)
Quadro da diretoria e comparador, minibios/superintendentes, mandatos/vacâncias, 3 agências com votos e trechos, desfecho por empresa, previsão de placar com backtest, relatório por empresa, cobertura em toda resposta. **Falta:** coleta diária de pautas, alerta de processo, cálculo de prazos por tipo e casos semelhantes.
