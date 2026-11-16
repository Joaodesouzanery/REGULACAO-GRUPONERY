"""Auditoria automática das falas citadas num documento (skill auditoria-falas).
Para cada «trecho literal» seguido de link do YouTube com &t=, confere se o trecho existe na transcrição do vídeo
e se o minuto do link está a até 2 min do ponto onde o trecho aparece.
Uso: python3 pipeline/auditar_falas.py <documento.html> [--ag antaq]   → imprime resumo e grava <documento>.auditoria_falas.json
Sai com código 1 se algum trecho não for encontrado."""
import sys, os, re, json, html, glob, unicodedata, difflib

H = sys.argv[1]
AG = sys.argv[sys.argv.index("--ag") + 1] if "--ag" in sys.argv else None
TXT = html.unescape(open(H).read())
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode())).strip()
dirs = [f"data/{AG}" if AG and AG != "antt" else "data"] if AG else ["data", *glob.glob("data/*/")]
_cache = {}


def transcricao(vid):
    if vid in _cache: return _cache[vid]
    for d in dirs:
        p = os.path.join(d, "transcricoes", f"{vid}.json")
        if os.path.exists(p):
            seg = json.load(open(p)); _cache[vid] = seg; return seg
    _cache[vid] = None; return None


def achar(seg, trecho):
    """devolve (segundo, razão) do melhor casamento do trecho numa janela deslizante da transcrição."""
    alvo = norm(trecho)[:160]
    if len(alvo) < 15: return None, 0
    pal = alvo.split(); n = len(pal)
    toks = []
    for s in seg:
        for w in norm(s["x"]).split(): toks.append((w, s["t"]))
    melhor = (None, 0.0)
    primeira = pal[0]
    for k, (w, t) in enumerate(toks):
        if w != primeira and (k % 3): continue
        jan = " ".join(x for x, _ in toks[k:k + n + 3])
        r = difflib.SequenceMatcher(None, alvo, jan[:len(alvo) + 20]).ratio()
        if r > melhor[1]: melhor = (t, r)
    return melhor


# padrão: «trecho» ... href="https://www.youtube.com/watch?v=ID&t=NNs"
pares = re.findall(r"«([^»]{15,400})»(?:(?!«).){0,400}?href=\"https://www\.youtube\.com/watch\?v=([\w-]{11})&(?:amp;)?t=(\d+)s?\"", TXT, re.S)
res = []
for trecho, vid, t in pares:
    seg = transcricao(vid)
    if not seg: res.append({"trecho": trecho[:80], "video": vid, "status": "sem transcrição local"}); continue
    pos, r = achar(seg, trecho)
    st = "ok" if r >= .72 and pos is not None and abs(pos - int(t)) <= 120 else "minuto distante" if r >= .72 else "não encontrado"
    res.append({"trecho": trecho[:80], "video": vid, "t_link": int(t), "t_achado": round(pos or 0), "semelhanca": round(r, 2), "status": st})
cont = {}
for x in res: cont[x["status"]] = cont.get(x["status"], 0) + 1
json.dump(res, open(H.rsplit(".", 1)[0] + ".auditoria_falas.json", "w"), ensure_ascii=False, indent=1)
print(f"{H}: {len(res)} falas com link · " + " · ".join(f"{k}: {v}" for k, v in cont.items()))
for x in res:
    if x["status"] not in ("ok", "sem transcrição local"): print(f"  [{x['status']}] {x['video']} t={x.get('t_link')} achado={x.get('t_achado')} ({x.get('semelhanca')}) «{x['trecho']}»")
sys.exit(1 if cont.get("não encontrado") else 0)
