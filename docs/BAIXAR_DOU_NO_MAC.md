# Confirmar posses e nomeações no DOU (feito no Mac)

O site do DOU (in.gov.br) bloqueia robôs na nuvem. No Mac, pelo navegador:

1. Abra https://www.in.gov.br/consulta e pesquise cada linha abaixo (aspas incluídas), **Seção 2**, no período indicado.
2. Em cada resultado relevante (decreto de nomeação, termo de posse, exoneração/renúncia, portaria de convocação de substituto), clique em **Versão certificada** e salve o PDF em `data/fontes_dou/` com o nome `<sobrenome>_<tipo>_<AAAA-MM-DD>.pdf` (ex.: `asfor_nomeacao_2022-12-07.pdf`).
3. `git add data/fontes_dou && git commit -m "PDFs DOU" && git push`. No chat: «leia os PDFs do DOU e atualize os mandatos».

| Pessoa | Buscar | Período | O que falta |
|---|---|---|---|
| Weber Ciloni | "Weber Ciloni" | 01/2018–12/2021 | nomeação, posse, renúncia/exoneração (2021) |
| Alexandre Porto | "Alexandre Porto Mendes de Souza" | 01/2020–12/2021 | nomeação (20/07/2021), posse, renúncia (~ago/2021) |
| Murshed Menezes Ali | "Murshed Menezes Ali" | 01/2020–12/2021 | designação como substituto, períodos de exercício |
| Eduardo José Marra | "Eduardo José Marra" | 01/2020–12/2021 | designação como substituto, períodos |
| Davi Barreto | "Davi Ferreira Gomes Barreto" | 05/2019–03/2023 | nomeação, posse |
| Marcelo Vinaud | "Marcelo Vinaud Prado" | 2017–2021 | recondução (DOU 20/04/2017), posse |
| Rafael Vitale | "Rafael Vitale Rodrigues" | 07/2021–02/2025 | nomeação, posse |
| Guilherme Sampaio | "Guilherme Theo Rodrigues da Rocha Sampaio" | 07/2021 e 08–09/2025 | posse como diretor e como DG; prazo do mandato de DG |
| Fábio Rogério | "Fábio Rogério Teixeira Dias de Almeida Carvalho" | 07/2021–02/2023 | posse, saída |
| Luciano Lourenço | "Luciano Lourenço da Silva" | 04/2022–02/2025 | posse |
| Felipe Queiroz | "Felipe Fernandes Queiroz" ou "Felipe Queiroz" + ANTT | 12/2022–02/2023 | posse |
| Lucas Asfor | "Lucas Asfor Rocha Lima" | 12/2022–03/2023 | posse; prazo do mandato |
| Alex Azevedo | "Alex Antonio de Azevedo Cruz" | 08–09/2025 | nomeação, posse, **prazo do mandato** (há conflito) |
| Severino Neto | "Severino Medeiros Ramos Neto" | 11/2025–02/2026 | posse |
| Substitutos 2025–26 | "José Aires Amaral Filho", "Alessandro Baumgartner", "Marcelo Cardoso Fonseca" | 2025–2026 | portarias de convocação |

Atas: a ANTT publica **pautas** em PDF (gov.br/antt) e **deliberações** no DOU/ANTTlegis; não achamos uma listagem pública de **atas**. Se encontrar (ex.: gov.br/antt → Acesso à informação → Reuniões de diretoria), salve 2–3 exemplos em `data/fontes_atas/` para eu avaliar o formato.
