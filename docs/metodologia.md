# Metodologia (piloto ANTT)

**Fonte:** legendas automáticas do YouTube (@canalANTT) das reuniões públicas da Diretoria Colegiada. Falantes inferidos por contexto (a legenda quase não marca troca de voz e erra nomes).
**Pipeline:** `01_coletar` (lista vídeos) → `02_transcrever`/`baixar_tudo.sh` (legendas, rodam no Mac do usuário) → `03_preparar` (turnos, nomes normalizados) → *leitura e extração por revisão humana-assistida* → `data/analise/{id}.analise.json` → `validar.py` → `05_indexar.py` (SQLite `data/regulacao.db`) → `consulta.py` (perfis, busca, temas).
**Esquema da análise:** reunião (nº, data, presidente, presentes), itens (processo, interessado, assunto, tema, relator, resultado, resumo do voto), votos por diretor (voto, ts, justificativa, tom, confiança), retirados, limites.
**Temas (normalizados):** onibus, cargas, concessoes_rodoviarias, pedagio_freeflow, reequilibrio_contratual, ferrovias, fiscalizacao_sancoes, sandbox_inovacao, participacao_social, leilao_otimizacao, sustentabilidade, institucional, regulacao_normativa, judicializacao.
**Rigor:** todo voto cita reunião e minuto (link do YouTube no instante); `confianca` indica se o voto foi ouvido ou inferido; `limites_da_analise` lista o que a legenda não permite confirmar. Rótulos como "raivoso" não são usados: o perfil mostra contagens (relatorias, % de acompanhamento, vistas, divergências), argumentos recorrentes e o tom *inferido*, sempre com n. Com n < 5 trata-se de indício.
**Cobertura atual:** ver `data/analise/_status.json` (reuniões com transcrição, analisadas, descartadas por falta de conteúdo).
**Uso:** `python3 pipeline/consulta.py perfil "Alex Azevedo" --tema onibus` · `... tema onibus` · `... busca "cassação fretamento"`.
