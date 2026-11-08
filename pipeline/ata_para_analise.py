"""Cria análises a partir de atas oficiais para reuniões SEM vídeo analisado.
Uso: bash pipeline/ag.sh anm python3 pipeline/ata_para_analise.py
Gera data/analise/ata_<TIPO>_<NNN>.analise.json (mesmo esquema; meta.fonte = «ata oficial (sem vídeo)»).
Votos: unânime -> relator «relator», demais presentes «acompanha o relator (ata: unanimidade)»; maioria -> quem a ata nomeia
como divergente fica «diverge (segundo a ata)», demais «não captado»; vista -> quem pediu «pede vista». Sem trecho literal nem minuto."""
import json, glob, os, re, unicodedata
norm = lambda s: unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
A = json.load(open("data/atas/indice_atas.json"))
CFG = json.load(open("data/config_agencia.json"))
def canon(nome):
    s = norm(nome)
    for n, rx in CFG["alias"].items():
        if re.search(rx, s, re.I): return n
    return nome
txt = open(f"agencias/{os.environ.get('AGENCIA','anm')}/qualidade/cruzamento_atas.md").read()
m = re.search(r"atas sem vídeo analisado: \d+ \(([^)]*)\)", txt)
alvo = [(x.split()[0], int(x.split()[1])) for x in m.group(1).split(", ")] if m else []
n = 0
for a in A:
    k = (a["tipo"], int(a["numero"] or 0))
    if k not in alvo: continue
    pres = [canon(p) for p in a.get("presentes", [])]
    itens = []
    for it in a.get("itens", []):
        rel = canon(it["relator"]) if it.get("relator") else None
        r = it.get("resultado") or "outro"; texto = it.get("deliberacao") or ""
        votos = []
        for p in pres:
            if p == rel: v = "relator, voto aprovado (segundo a ata)" if r in ("unanime", "maioria") else "relator"
            elif r == "unanime": v = "acompanha o relator (ata: unanimidade dos presentes)"
            elif r == "vista": v = "pede vista (segundo a ata)" if norm(p.split()[0]) in norm(texto) and "vista" in norm(texto) else "voto não captado (item em vista)"
            elif r == "maioria": v = "diverge (segundo a ata)" if norm(p.split()[-1]) in norm(texto) and re.search(r"diverg|vencid", norm(texto)) else "voto não captado (maioria; ata não detalha)"
            else: continue
            votos.append({"diretor": p, "voto": v, "ts": None, "justificativa": None, "confianca": "ata"})
        itens.append({"id": it.get("id") or f"item{len(itens)+1}", "ts": None, "processo": it.get("processo"), "interessado": None, "assunto": texto[:300] or "(ata sem descrição)",
                      "tema": [texto[:300]], "relator": rel, "resultado": {"unanime": "aprovado por unanimidade", "maioria": "aprovado por maioria", "vista": "pedido de vista", "retirado": "retirado de pauta"}.get(r, r), "resumo_voto": texto[:500], "votos": votos})
    out = {"meta": {"video_id": f"ata_{k[0]}_{k[1]:03d}", "fonte": "ata oficial (sem vídeo)", "url": a.get("url"), "ata": list(k), "versao_esquema": 1},
           "reuniao": {"numero": f"{k[1]}ª {'Reunião Ordinária' if k[0]=='ROP' else 'Reunião Extraordinária'} Pública (só ata)", "data": a.get("data"), "formato": "sem vídeo publicado",
                       "presidente_da_sessao": None, "diretores_presentes": pres, "ausentes": [], "observacoes": [a.get("observacao") or "", "reunião sem vídeo: dados da ata oficial; sem trecho literal nem minuto"]},
           "itens": itens, "retirados": [], "limites_da_analise": ["Fonte única: ata oficial. Voto por diretor deduzido da lista de presentes e do resultado; temas não classificados."]}
    if not itens and not a.get("data"): continue  # REP 25 cancelada
    json.dump(out, open(f"data/analise/ata_{k[0]}_{k[1]:03d}.analise.json", "w"), ensure_ascii=False, indent=1); n += 1
print(n, "reuniões criadas a partir de atas:", alvo)
