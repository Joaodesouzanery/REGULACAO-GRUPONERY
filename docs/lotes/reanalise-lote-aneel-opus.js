export const meta = {
  name: 'reanalise-lote-aneel-opus',
  description: 'Reanalisa reuniões da ANEEL de 2022-2023 com modelo maior (um analista-reuniao por reunião) e regrava .analise.json validados',
  phases: [{ title: 'Reanalisar', detail: 'um analista-reuniao por reunião, modelo maior' }],
}
const SCHEMA = { type: 'object', properties: { arquivo: { type: 'string' }, itens: { type: 'number' }, votos: { type: 'number' }, valido: { type: 'boolean' }, duvidas: { type: 'string' } }, required: ['arquivo', 'itens', 'votos', 'valido'] }
phase('Reanalisar')
const res = await parallel(args.map((id, k) => () => agent(
  `Agência: aneel. Repositório em /home/user/REGULACAO-GRUPONERY (trabalhe a partir dele). Entrada: data/aneel/analise/${id}.md (já preparado). Destino: data/aneel/analise/${id}.analise.json (REESCREVA do zero, ignorando o arquivo existente — esta é uma reanálise de qualidade). ` +
  `Siga data/aneel/prompt_analise.txt e a lista de diretores de data/aneel/config_agencia.json. REGRA IMPORTANTE sobre pedido de vista: só o diretor que pediu vista recebe categoria "pede vista"; os demais diretores da sessão, que ainda não votaram no mérito porque o item ficou pendente, devem ter o voto registrado como algo como "não votou (vista)" — nunca marque todos os diretores como se tivessem "pedido vista". Valide com: bash pipeline/ag.sh aneel python3 pipeline/validar.py data/aneel/analise/${id}.analise.json (o caminho dentro da raiz virtual é analise/${id}.analise.json se o primeiro falhar). ` +
  `Se a reunião não tiver deliberações (teste, transmissão vazia, só abertura), grave um JSON válido com itens vazios e diga isso em duvidas. Não faça commit nem edite outros arquivos.`,
  { label: `aneel-opus ${id}`, agentType: 'analista-reuniao', model: 'opus', schema: SCHEMA })))
const ok = res.filter(Boolean)
log(`${ok.length}/${args.length} reuniões reanalisadas; ${ok.filter(r => r.valido).length} válidas`)
return { total: args.length, ok: ok.length, validos: ok.filter(r => r.valido).length, itens: ok.reduce((a, r) => a + (r.itens || 0), 0), votos: ok.reduce((a, r) => a + (r.votos || 0), 0), falhas: res.map((r, k) => r ? null : args[k]).filter(Boolean), duvidas: ok.filter(r => r.duvidas).map(r => `${r.arquivo}: ${r.duvidas}`).slice(0, 40) }
