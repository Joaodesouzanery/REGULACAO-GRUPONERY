---
name: perfis-dirigentes
description: Perfis de diretores e superintendentes (foto oficial, formação, minibio, mandato) guardados no repositório em data/<ag>/dirigentes/ e prontos para qualquer relatório; atualiza quando alguém entra ou sai (checagem do dia 1). Use ao precisar de foto/minibio, quando mudar a diretoria ou ao iniciar agência.
---
# Perfis de dirigentes

- **Fonte canônica:** `data/<ag>/dirigentes/<slug>.json` + `<slug>.jpg` (repositório privado). `bios.json` e `superintendentes.json` são **gerados**: `python3 pipeline/dirigentes.py gerar`.
- **O que falta:** `python3 pipeline/dirigentes.py faltas` (quem está em exercício sem perfil, foto ou formação).
- **Entrou alguém** (novo diretor, substituto convocado, superintendente nomeado): subagente `pesquisador-dirigentes` só para essa pessoa (gov.br composição + minicurrículo, Senado MSF, DOU); cria o perfil e a foto oficial; `dirigentes.py gerar`; `relatorio_diretoria.py <ag>`.
- **Saiu alguém:** no perfil, `status: ex-dirigente`, `data_saida`, fonte. Nunca apagar (histórico e relatórios antigos).
- **Foto:** só oficial (gov.br/Senado), 400×400; sem oficial → iniciais (skill `fotos-oficiais`).
- **Sempre com fonte e `verificado_em`.** Nome da base (`nome_chave`) deve bater com o usado nas análises (alias no config).
