# Produto: consultoria de inteligência regulatória (você é o ativo)

**Princípio:** o cliente compra respostas e relatórios, não acesso à base. A base (transcrições, votos estruturados, trechos literais, mandatos, conferência de qualidade) e o método ficam com você. O cliente depende do serviço porque a base cresce toda semana e é cara de reproduzir.

## Dois relatórios = dois produtos (nov/2026)
- **(A) «10 perguntas»** — `pipeline/relatorio_v2.py <pasta> --agencia <ag>`: capa → sumário → **quadro da diretoria** → 10 perguntas → **comparador (quem relata, quem diverge) + superintendentes** → como ler. ~17 páginas. `--sem-diretoria` gera só as perguntas.
- **(B) «Empresa»** — `pipeline/relatorio_empresa.py clientes/<x>/<pasta>` (nome + CNPJ, até 3 agências). Produto separado.
- **Boletim mensal da agência** (premium, à parte) — `pipeline/boletim.py <ag> AAAA-MM`.
- O PDF só de diretoria (`relatorio_diretoria.py`) é peça interna/prospecção.

## Ofertas sugeridas
| Oferta | O que o cliente recebe | Ritmo | Como cobrar |
|---|---|---|---|
| **Pacote de perguntas** | até N perguntas/semana (ex.: 10) → relatório .docx com uma ficha por pergunta (números, evidências com trecho literal e link no minuto, contra-exemplos, confiança) | semanal | mensalidade por faixa (5 / 10 / 20 perguntas) |
| **Dossiê de diretor** | perfil completo de um diretor (temas, padrão de voto, argumentos, divergências, falas, mandato) | sob demanda | preço fechado por dossiê |
| **Dossiê pré-pauta** | para a próxima reunião de diretoria: quem relata cada item de interesse e como cada diretor tende a votar em casos parecidos | por reunião | por reunião ou incluso no plano premium |
| **Monitoramento** | «o que mudou na semana»: decisões, divergências, mudanças de diretoria, vacâncias | semanal | assinatura |
| **Comparativo de agências** | vacância, ritmo decisório, padrões por tema em várias agências | trimestral | projeto |

Diferenciais a vender: evidência verificável (link no minuto), cobertura histórica (2019–hoje), taxa de confiabilidade medida (≈ 94–95%), resposta em dias.

## Fluxo de atendimento (skill `relatorio-cliente`)
1. Cliente envia perguntas (e-mail/WhatsApp). Você cola no chat: «perguntas do cliente X, semana NN: …».
2. O Claude grava em `clientes/<cliente>/<AAAA-semNN>/perguntas.md` (fora do GitHub), monta as fichas (`consulta.py ficha`/`busca`/`trecho`), revisa e gera `relatorio.docx` (`pipeline/relatorio.py`).
3. Você revisa e envia. Histórico em `clientes/<cliente>/historico.md`.

## Boas perguntas de cliente (modelos)
- «Em processos de empresas de ônibus (cassação, novos mercados), como o diretor X vota? Relata? Diverge?»
- «Quem relata reequilíbrio contratual de concessões rodoviárias e qual o padrão de decisão?»
- «A empresa Y já teve processos na diretoria? Quais votos e argumentos?»
- «Para a RD da próxima semana, item Z: precedentes e tendência de cada diretor.»
- «Quanto tempo a ANTT fica com cadeira vaga? Há vaga aberta hoje? Quem são os substitutos?»

## Limites a declarar ao cliente
Legenda automática; quem apenas acompanha raramente fala; itens sigilosos e voto escrito completo (SEI) fora; análise de comportamento é inferência baseada em contagens e falas, nunca rótulo pessoal.

## Cuidados
- Dados de clientes nunca no GitHub (`clientes/` está no `.gitignore`); faça backup local.
- Uso de dados públicos é legítimo; evite apresentar inferências como fato e não faça juízo pessoal sobre diretores.
