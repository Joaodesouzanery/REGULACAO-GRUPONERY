export const meta = {
  name: 'analise-lote-aneel',
  description: 'Analisa um lote de reuniões da diretoria da ANEEL (um analista-reuniao por reunião) e grava .analise.json validados',
  phases: [{ title: 'Analisar', detail: 'um analista-reuniao por reunião' }],
}
const SCHEMA = { type: 'object', properties: { arquivo: { type: 'string' }, itens: { type: 'number' }, votos: { type: 'number' }, valido: { type: 'boolean' }, duvidas: { type: 'string' } }, required: ['arquivo', 'itens', 'votos', 'valido'] }
phase('Analisar')
const res = await parallel(args.map((id, k) => () => agent(
  `Agência: aneel. Repositório em /home/user/REGULACAO-GRUPONERY (trabalhe a partir dele). Entrada: data/aneel/analise/${id}.md (já preparado). Destino: data/aneel/analise/${id}.analise.json. ` +
  `Siga data/aneel/prompt_analise.txt e a lista de diretores de data/aneel/config_agencia.json. Valide com: bash pipeline/ag.sh aneel python3 pipeline/validar.py data/aneel/analise/${id}.analise.json (o caminho dentro da raiz virtual é analise/${id}.analise.json se o primeiro falhar). ` +
  `Se a reunião não tiver deliberações (teste, transmissão vazia, só abertura), grave um JSON válido com itens vazios e diga isso em duvidas. Não faça commit nem edite outros arquivos.`,
  { label: `aneel ${id}`, agentType: 'analista-reuniao', schema: SCHEMA })))
const ok = res.filter(Boolean)
log(`${ok.length}/${args.length} reuniões analisadas; ${ok.filter(r => r.valido).length} válidas`)
return { total: args.length, ok: ok.length, validos: ok.filter(r => r.valido).length, itens: ok.reduce((a, r) => a + (r.itens || 0), 0), votos: ok.reduce((a, r) => a + (r.votos || 0), 0), falhas: res.map((r, k) => r ? null : args[k]).filter(Boolean), duvidas: ok.filter(r => r.duvidas).map(r => `${r.arquivo}: ${r.duvidas}`).slice(0, 40) }