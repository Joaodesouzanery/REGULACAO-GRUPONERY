# Perguntas que funcionam, e como será a melhor resposta

Formato padrão de toda resposta: **1) resposta direta em 2–3 linhas** · **2) números** (n de reuniões/itens/votos, período, confiança) · **3) como e por quê** (argumentos recorrentes, justificativas registradas) · **4) evidências**: reunião, item, voto, citação literal curta e link `youtube.com/watch?v=ID&t=SEGs` · **5) limites** (legenda automática, amostra pequena, itens sigilosos, anos não analisados).

| Tipo | Exemplo | Como respondo (fonte) |
|---|---|---|
| Perfil por tema | «Em assuntos de empresas de ônibus, o Alex Azevedo costuma se envolver? Como e por quê?» | `perfil "Alex Azevedo" --tema onibus` (e `onibus_regular`, `onibus_fretamento`): nº de votos e relatorias no tema, % de «acompanha», cassações/vistas, argumentos recorrentes (usuário, concorrência, proporcionalidade), tom, 3–5 evidências com link |
| Comparar diretores | «Felipe Queiroz e Lucas Asfor: quem diverge mais em concessões rodoviárias?» | perfis lado a lado: votos divergentes/vistas/vencidos, relatorias, argumentos; só afirmo diferença se n permitir |
| Divergências e vistas | «Quem pediu vista em 2025 e por quê?» / «quais decisões não foram unânimes?» | filtro por categoria `vista`, `vencido`, `revisor_diverge`; cada caso com justificativa e link |
| Evolução no tempo | «O voto do Guilherme Sampaio em fretamento mudou depois que virou Diretor-Geral?» | corte antes/depois de 29/08/2025 (mandatos), n de cada lado, aviso se n < 5 |
| Relatoria | «O que o Lucas Asfor relatou sobre free flow?» | itens onde é relator, resumo do voto, resultado, link |
| Empresa / processo | «O que a ANTT decidiu sobre a Candango e quem votou como?» | `busca Candango` + votos por diretor, trechos literais, linha do tempo das deliberações |
| Fala literal | «O que se disse nas audiências sobre pagamento avulso do free flow?» | `trecho "pagamento avulso" --tipo audiencia` e `falas <diretor>`: frase exata + minuto |
| Tom / «raivoso» | «O diretor X é duro em fiscalização?» | NUNCA rótulo: frequência de sanção máxima (cassação), divergência, justificativas («concorrência desleal», «reincidência»), tom registrado como inferência, com n |
| Mandatos / quórum | «Quanto tempo o colegiado ficou incompleto e quem decidia?» | `mandatos` + `vacancias.json`: períodos, cadeiras vagas, substitutos, votos desses períodos |
| Cobertura | «O que vocês não conseguem saber?» | `COBERTURA.md`, `sem_transcricao.md`, itens sigilosos, anos pendentes |

## Exemplo real (teste)
Pergunta: «Alex Azevedo em ônibus». Resposta-modelo: no tema `onibus`, 45 votos e 11 relatorias; acompanhou o relator em 94% dos votos em que não era relator; relatou cassações de fretamento «por concorrência desleal» (RD 1033 item 1.4.2, 21/05/2026, link no minuto); pediu vista em casos de TAR quando havia dúvida jurídica; argumentos recorrentes: usuário, proporcionalidade, concorrência; limites: amostra em fretamento pequena; legenda automática.
