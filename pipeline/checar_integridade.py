"""Checagem antes de commit (obrigatória; ver .claude/skills/cuidados-pipeline). Uso: python3 pipeline/checar_integridade.py [--atualizar]
Falha (código 1) se:
 - algum arquivo versionado em pastas protegidas foi APAGADO no working tree (qualidade/, mandatos/, docs/, data/analise*/, data/qualidade/, data/transcricoes/, .claude/skills/);
 - o banco data/regulacao.db foi alterado/adicionado no stage (não versionar a cada lote);
 - as contagens (reuniões, itens, votos, eventos, falas) CAÍRAM em relação a data/contagens.json;
 - há análise inválida (validar.py / validar_evento.py).
--atualizar grava as contagens atuais como nova referência (use após um aumento legítimo)."""
import subprocess, sqlite3, json, sys, os
PROT = ("agencias/antt/qualidade/", "agencias/antt/mandatos/", "agencias/anm/qualidade/", "agencias/anm/mandatos/", "data/anm/analise", "data/anm/transcricoes/", "data/anm/qualidade/", "data/anm/mandatos.json", "docs/", "data/analise/", "data/analise_eventos/", "data/qualidade/", "data/transcricoes/", ".claude/skills/", "data/mandatos.json", "data/vacancias.json", "CLAUDE.md")
erros = []
sh = lambda c: subprocess.run(c, shell=True, capture_output=True, text=True).stdout
apagados = [l[3:] for l in sh("git status --porcelain").splitlines() if l[:2].strip() == "D" or l[1] == "D"]
apagados = [f for f in apagados if f.startswith(PROT)]
if apagados: erros.append(f"{len(apagados)} arquivo(s) protegido(s) APAGADO(s): " + ", ".join(apagados[:10]) + (" …" if len(apagados) > 10 else ""))
if "data/regulacao.db" in sh("git diff --cached --name-only"): erros.append("data/regulacao.db está no stage: rode `git restore --staged data/regulacao.db` (só versionar em marcos, com aviso ao usuário).")
for v in ("pipeline/validar.py", "pipeline/validar_evento.py"):
    r = subprocess.run([sys.executable, v], capture_output=True, text=True)
    ruins = [l for l in (r.stdout + r.stderr).splitlines() if l.strip() and not l.startswith("ok") and ("erro" in l.lower() or "invál" in l.lower() or "traceback" in l.lower())]
    if r.returncode != 0 or ruins: erros.append(f"{v}: " + "; ".join(ruins[:5] or [f"código {r.returncode}"]))
if os.path.exists("data/regulacao.db"):
    c = sqlite3.connect("data/regulacao.db")
    atual = {t: c.execute(f"select count(*) from {t}").fetchone()[0] for t in ("reunioes", "itens", "votos", "eventos", "falas_diretores")}
    ref = json.load(open("data/contagens.json")) if os.path.exists("data/contagens.json") else {}
    for k, v in atual.items():
        if v < ref.get(k, 0): erros.append(f"contagem caiu: {k} {ref[k]} → {v}")
    if "--atualizar" in sys.argv or not ref: json.dump(atual, open("data/contagens.json", "w"), indent=1); print("referência de contagens gravada:", atual)
    print("contagens:", atual)
else: erros.append("data/regulacao.db não existe: rode python3 pipeline/05_indexar.py")
if erros: print("FALHOU:\n- " + "\n- ".join(erros)); sys.exit(1)
print("OK: nenhuma perda detectada.")
