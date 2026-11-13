"""Começa uma agência nova em 1 sessão: pasta, raiz virtual, config a partir do modelo, prompts de análise/evento.
Uso: python3 pipeline/iniciar_agencia.py <sigla> @Canal "Nome da agência" [--simular]
Depois (skill nova-agencia-rapida): inventário daqui, pesquisador-mandatos + pesquisador-superintendentes, coleta no Mac."""
import sys, os, json, re
sig, canal, nome = sys.argv[1].lower(), sys.argv[2], sys.argv[3]
SIM = "--simular" in sys.argv
D = f"data/{sig}"
base = json.load(open("data/antaq/config_agencia.json"))
cfg = {"sigla": sig, "nome": nome, "canal": canal, "playlists": [], "atas_url": "", "diretores": [], "alias": {}, "rx_nomes": "",
       "temas": [], "_preencher": "diretores/alias/rx_nomes via pesquisador-mandatos; temas do setor (ver exemplos em data/antaq e data/anm)"}
pa = open("data/antaq/prompt_analise.txt").read().replace("ANTAQ — Agência Nacional de Transportes Aquaviários —", f"{sig.upper()} — {nome} —").replace("data/antaq", D)
pa = re.sub(r"com o nome canônico do diretor \(.*?\) e ts", "com o nome canônico do diretor (lista em " + D + "/config_agencia.json, campo diretores; nomes fora da lista → como ditos, registrar em limites_da_analise) e ts", pa, flags=re.S)
pe = open("data/antaq/prompt_evento.txt").read().replace("ANTAQ", sig.upper()).replace("data/antaq", D)
acoes = [f"mkdir {D} e {D}/{{transcricoes,analise,analise_eventos,qualidade}}", f"{D}/config_agencia.json", f"{D}/prompt_analise.txt", f"{D}/prompt_evento.txt", f"{D}/mandatos.json, bios.json, vacancias.json, superintendentes.json (vazios)", f"bash pipeline/ag.sh {sig} true (raiz virtual)"]
if SIM:
    print("SIMULAÇÃO — criaria:\n- " + "\n- ".join(acoes)); sys.exit()
for p in ("transcricoes", "analise", "analise_eventos", "qualidade"): os.makedirs(f"{D}/{p}", exist_ok=True)
json.dump(cfg, open(f"{D}/config_agencia.json", "w"), ensure_ascii=False, indent=1)
open(f"{D}/prompt_analise.txt", "w").write(pa); open(f"{D}/prompt_evento.txt", "w").write(pe)
for f in ("mandatos", "bios", "vacancias", "superintendentes"):
    if not os.path.exists(f"{D}/{f}.json"): json.dump([], open(f"{D}/{f}.json", "w"))
os.system(f"bash pipeline/ag.sh {sig} true")
print(f"Pronto: {D}. Próximos: inventário (bash pipeline/ag.sh {sig} python3 pipeline/01_coletar.py {canal} 0), agentes de mandatos/superintendentes/bios, e no Mac: caffeinate -i bash pipeline/coletar_tudo_e_enviar.sh {sig} {canal}")
