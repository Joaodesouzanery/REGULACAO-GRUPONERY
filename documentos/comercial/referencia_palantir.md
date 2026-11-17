# Referência: Palantir × «inteligência de decisão regulatória»

*Pesquisa web de 17/11/2026. Cada fato traz a URL. Material da Palantir é marketing do fornecedor; blogs de terceiros sobre preços não estão verificados.*

## Resumo (5 linhas)
1. A Palantir **não tem produto público** que monitore como diretorias de agências decidem (votos por diretor, falas, mandatos, precedentes). O que ela vende é uma plataforma genérica (Foundry/AIP + Ontologia) que o cliente configura.
2. Do lado do **governo**, ela atende os próprios reguladores e órgãos (FDA, CDC/HHS, IRS, NHS, FCA britânica) para analisar dados internos. Não faz análise das decisões deles para quem é regulado.
3. Em **setores regulados** (bancos/AML, energia, nuclear), o uso é de *compliance operacional*: monitorar transações, acompanhar marcos de licenciamento e manter gêmeos digitais. Isso não é previsão de comportamento decisório.
4. O caso mais próximo é o **«nuclear operating system»** com a The Nuclear Company (~US$ 100 mi em 5 anos), que inclui *regulatory compliance tracking* e marcos regulatórios em tempo real. Mesmo assim, olha para o processo do regulado, não para quem decide.
5. Para o nosso posicionamento valem a **linguagem** (ontologia, rastreabilidade, decisão) e o **modelo de venda** (bootcamp curto com dados reais do cliente → contrato maior). Não vale o lock-in nem a opacidade de preço.

## (1) Produtos e Ontologia
- **Foundry**: plataforma de integração e análise de dados, usada no governo e no setor comercial (HHS: [FedScoop](https://fedscoop.com/hhs-palantir-platform-bpa/)).
- **Gotham**: linha de defesa e inteligência. Não aparece nos casos regulatórios levantados.
- **AIP**: camada de IA sobre Foundry/Ontologia. A venda começa por *bootcamps* de cerca de 5 dias, com engenheiros da Palantir montando casos de uso sobre os dados do cliente ([Redress Compliance](https://redresscompliance.com/palantir-aip-foundry-guide.html)).
- **Apollo**: implantação contínua do software em vários ambientes. Não entra nos casos aqui; é infraestrutura.
- **Ontologia**: modelo de objetos de negócio (entidades, relações e ações) sobre os dados brutos. Analistas apontam que ela «incorpora a lógica do negócio» e torna a migração cara, porque teria de ser refeita do zero ([Redress Compliance](https://redresscompliance.com/palantir-aip-foundry-guide.html); [Redress, negociação](https://www.redresscompliance.com/palantir-aip-foundry-negotiation.html)).

## (2)–(4) Casos

| Caso | Cliente | O que faz | Semelhança com o nosso serviço | Fonte |
|---|---|---|---|---|
| Revisão de medicamentos | FDA (CDER, Oncology Center) | Análise de dados para revisar medicamentos e produtos regulados (2020) | Baixa: ajuda o **regulador** a decidir; não analisa decisões para terceiros | [TechCrunch](https://techcrunch.com/?p=2084328) |
| DCIPHER / vigilância | CDC | Vigilância epidemiológica desde 2010, em ambiente Foundry | Baixa: integração de dados públicos de saúde | [ExecutiveBiz](https://www.executivebiz.com/articles/palantir-to-continue-support-for-cdcs-disease-surveillance-response-efforts) |
| BPA HHS | HHS (NIH, CDC, FDA) | Contrato-quadro de 5 anos, US$ 90 mi | Referência de preço e escala | [FedScoop](https://fedscoop.com/hhs-palantir-platform-bpa/) |
| Federated Data Platform | NHS England | Plataforma de dados do NHS, até £ 330 mi em 7 anos; polêmica de privacidade | Baixa no conteúdo; alta como alerta de reputação | [Digital Health](https://digitalhealth.net/2023/11/nhs-england-awards-330m-federated-data-platform-contract-to-palantir) |
| Lead and Case Analytics | IRS | Análise de crimes financeiros desde 2018; mais de US$ 130 mi pagos | Baixa: fiscalização | [The Intercept](https://theintercept.com/2026/04/24/palantir-irs-contract-data/) |
| Piloto no regulador financeiro | FCA (Reino Unido) | Foundry sobre o *data lake* do regulador; 3 meses a £ 30 mil/semana | Média: mostra o modelo **piloto pago por semana** | [TLT](https://www.tlt.com/insights-and-events/insight/fca-turns-to-ai-to-fight-fraud-what-the-palantir-contract-means-for-financial-regulation) |
| Anti Financial Crime | Société Générale e «mais de uma dúzia» de grandes bancos | AML/KYC: triagem, investigação, monitoramento de transações | Média: compliance com rastreabilidade de evidência para o regulador | [Retail Banker Intl.](https://www.retailbankerinternational.com/news/societe-generale-palantir-tech-financial-crime/); [Palantir AML/KYC](https://www.palantir.com/assets/xrfr7uokpv1b/4ggUhYEasIX2p0mOaAW1zV/03978f27a9477f78e150241c6884efdb/Foundry_AML_KYC.pdf) |
| Nuclear operating system | The Nuclear Company | Gêmeo digital, acompanhamento de compliance regulatório, marcos regulatórios em tempo real; ~US$ 100 mi em 5 anos | **A mais alta encontrada**: acompanha prazos e marcos do processo regulatório do regulado | [StreetInsider](https://www.streetinsider.com/General+News/Palantir+partners+to+develop+AI+software+for+nuclear+construction/24979685.html) |
| Vertex for Oil & Gas | Energia / O&G | Gêmeos digitais de ativos para otimizar operações (whitepaper de 2022) | Baixa: o trecho lido não trata de regulação (o PDF não foi lido inteiro) | [Whitepaper Palantir](https://www.palantir.com/assets/xrfr7uokpv1b/4iJcF4I6pdyGbzGbLXFcN9/181518cf67af2106e87bfa4be4c9601e/Whitepaper_-_Vertex_for_Oil___Gas.pdf) |

**Item (4):** não encontrei produto da Palantir, nem de parceiros, voltado a analisar **decisões de colegiados reguladores** (votos, falas, perfis de diretores). Licenciamento só aparece como acompanhamento de marcos no caso nuclear. A pesquisa também não encontrou contrato com a SEC nem com a PG&E. Esses pontos ficam em aberto.

## (5) Como vende
- **Sem tabela pública de preço.** A cobrança mistura licença e consumo; o armazenamento na Ontologia é medido em GB-mês ([Redress](https://redresscompliance.com/palantir-aip-foundry-guide.html)).
- **Bootcamp de 5 dias** com dados reais do cliente leva a contrato plurianual. Exemplos citados por terceiros, sem verificação: um cliente de bens de consumo com contrato de US$ 19 mi em 5 anos depois do piloto, e uma empresa de energia que passou de US$ 4 mi para mais de US$ 20 mi/ano em 12 meses ([Redress](https://redresscompliance.com/palantir-aip-foundry-guide.html)).
- **Governo:** a FCA pagou £ 30 mil/semana no piloto; o HHS assinou BPA de US$ 90 mi; o NHS, até £ 330 mi (fontes na tabela).

## O que adotar
- **Ontologia regulatória explícita**: agência → diretoria/cadeira → diretor (mandato) → processo → reunião → item → voto → fala (trecho + link &t=) → precedente. Mostrar isso como um diagrama no material comercial.
- **Rastreabilidade até a fonte** como argumento central: cada afirmação leva ao vídeo no minuto exato. É o equivalente público e verificável da «linhagem de dados».
- **Painéis de decisão**, não de dados: «o que vem na pauta, quem relata, como votou em casos parecidos, placar provável (inferência com backtest)».
- **Piloto curto pago** no formato bootcamp: 1–2 semanas com 3 processos reais do cliente, entregando o raio-X e o alerta pré-pauta, que depois viram assinatura mensal.
- **Linguagem**: «inteligência de decisão», «sistema operacional regulatório», «da evidência à decisão».

## O que NÃO copiar
- **Lock-in e opacidade de preço**: tenha preço claro por pacote e entregue os dados exportáveis (CSV/XLSX), que já fazem parte do produto.
- **Dados pessoais sensíveis e vigilância**: as polêmicas do NHS e do IRS mostram o risco. Fique só em atos públicos, com LGPD, e sem perfilar a vida privada de diretores.
- **Promessas de ROI sem base** (ex.: «90% de redução de custo»): mantenha n, confiança e taxa da conferência cega.
- **Engenharia sob medida cara**: o nosso diferencial é o conteúdo já pronto e curado por agência, não uma plataforma vazia.
- **Uso de marca/nome da Palantir** em material próprio: cite só como referência de mercado.
