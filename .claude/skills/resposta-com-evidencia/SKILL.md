---
name: resposta-com-evidencia
description: Formato obrigatório (ficha fixa) para responder perguntas sobre diretores de agências — perfil, tema, empresa, divergências, falas, mandatos. Use sempre que o usuário perguntar algo como «o diretor X costuma…», «como vota em…», «quem diverge…», «o que disse sobre…».
---
# Resposta com evidência (ficha fixa)

1. `python3 pipeline/05_indexar.py` (se a base mudou) e `python3 pipeline/consulta.py ficha "<diretor>" [--tema <tema>]` (temas: `consulta.py temas`). Para empresa: `consulta.py empresa <nome|sigla>` (histórico, desfechos, relatores, votos por diretor); microtema: `consulta.py microtema <microtema> [--diretor X]`; casos parecidos: `consulta.py precedentes "<texto>"`; relator provável: `consulta.py relator <empresa|microtema>`; assunto livre: `consulta.py busca "<texto>"`; falas literais: `consulta.py trecho "<texto>"`; eventos: `consulta.py falas <nome>`.
2. Leia as evidências e escreva SEMPRE nesta ordem:
   1. **Resposta curta** (2 linhas): o padrão observado e o porquê (argumentos recorrentes).
   2. **Números**: n de votos, período, relatorias, % acompanha, vistas, divergências, vencido.
   3. **3–5 evidências**: RD nº (data), item, assunto, voto, justificativa, **trecho literal** («…») e **[link no minuto](…&t=Ns)**. Se o trecho automático for só saudação/protocolo, troque por uma frase melhor com `consulta.py trecho` na mesma reunião e corrija o minuto.
   4. **Contra-exemplos**: votos que fogem do padrão (vista, voto-vista divergente, vencido).
   5. **Falas em eventos**, se houver (avise que a maioria das audiências não tem fala de diretor).
   6. **Confiança e lacunas**: taxa da conferência (≈ 94–95% nos votos; ver `agencias/antt/qualidade/README.md`), legenda automática, «janela_do_item» = minuto aproximado, sigilosos/sem transcrição, voto escrito completo no SEI.
3. Proibido rótulo sem base («raivoso», «problemático»): use contagens e tom como inferência registrada.
4. Discordância/erro de dado: diga **qual diretor, RD e item**.
5. Se a pergunta vier de cliente, use a skill `relatorio-cliente` para gerar o documento.

**Sempre**: inclua o bloco da skill `cobertura-em-toda-resposta` (a seção 6 da ficha já traz).
