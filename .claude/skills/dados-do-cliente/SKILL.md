---
name: dados-do-cliente
description: Como receber, usar, proteger e apagar dados de processos que o cliente informa (e-mail/planilha → clientes/<x>/<pasta>/processos.json com fonte e sigiloso; raio-X; eliminação no término). Use ao receber andamentos/intimações do cliente, montar o raio-X ou encerrar contrato.
---
# Dados do cliente

Base contratual: `documentos/contratos/clausulas_cliente_final.md` cláusula 14 e `dpa_lgpd.md` seção 6-A. **Nunca** usamos login/senha/certificado do cliente no SEI, nunca automatizamos acesso nem contornamos CAPTCHA (CP art. 154-A; Lei 12.737/2012). O cliente **envia**.

## 1. Receber
- Canal: e-mail corporativo ou planilha enviada pelo cliente (pedido na conversa mensal: skill `consulta-mensal-cliente`). Guarde o original em `clientes/<x>/<pasta>/recebidos/AAAA-MM-DD_<origem>.*`.
- Converta para `clientes/<x>/<pasta>/processos.json`:
```json
{"processos": [{
  "processo": "50500.000000/2026-00",
  "titulo": "Reequilíbrio do contrato de arrendamento",
  "etapa_sei": "Análise técnica na superintendência",
  "area": "SOG",
  "andamentos": [{"data": "2026-10-03", "texto": "Nota técnica juntada"}],
  "fonte": "informado pelo cliente em 05/11/2026",
  "sigiloso": false
}]}
```
- `fonte` obrigatório no formato «informado pelo cliente em DD/MM/AAAA» (data do envio). Atualização posterior → nova data. Dado que você achou em fonte pública → `fonte: "público: <URL> em DD/MM/AAAA"` (LAI, Lei 12.527/2011, ou consulta pública).
- `sigiloso: true` sempre que o cliente disser que é sigiloso/restrito ou na dúvida.

## 2. Usar
- Raio-X: skill `raio-x-processos` (`pipeline/raio_x.py`, que usa `monitoramento.py raio_x` e `prazos.py`). Nas entregas, todo dado vindo daqui aparece marcado «informado pelo cliente».
- Só para o próprio cliente. Nunca em demo (`demo-prospect`), marketing ou relatório de outro cliente.

## 3. Proteger
- `clientes/` está no `.gitignore`; `python3 pipeline/checar_integridade.py` falha se algum `clientes/` entrar no stage ou no git.
- Antes de entrega/commit/post: agente `guardiao-dados-cliente` + skill `conformidade-entrega`.
- Material de divulgação: só versão anônima sem processo, número, previsão ou estratégia, salvo autorização escrita.

## 4. Apagar (término do contrato — LGPD arts. 15 e 16)
1. Exporte para o cliente (PDF/CSV) as entregas e o `processos.json`.
2. Em até 30 dias: `rm -rf clientes/<x>/` (e cópias locais/e-mail de trabalho), salvo obrigação legal.
3. Registre a data em `docs/` (só "cliente encerrado, dados eliminados em DD/MM/AAAA", sem dados) e avise o cliente por escrito.
