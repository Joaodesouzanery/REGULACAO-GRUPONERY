"""Dashboard HTML (protótipo estático) — Monitoramento de Processos Regulatórios, 8 abas, dados reais embutidos, design Grupo Nery.
Uso: python3 pipeline/dashboard.py clientes/<x>/<pasta>   → <pasta>/dashboard.html (abre direto no navegador, sem servidor)."""
import sys, os, re, json, datetime, collections, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, prazos, similares, mapa_tema, notas_cliente as nc, design as d
from desfecho import desfecho_item

P = sys.argv[1].rstrip("/"); EMP = json.load(open(f"{P}/empresa.json")); AG = EMP.get("agencias", ["antaq"])[0]
D = "data" if AG == "antt" else f"data/{AG}"; ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
MAN = ld(f"{P}/desfechos_manuais.json", {}); HOJE = datetime.date.today()
ROT = {"favorável": "a favor", "parcial": "em parte", "neutro": "sem efeito direto", "desfavorável": "contra", "pendente": "sem decisão"}
c = previsao.conn(AG)
its = [i for i in previsao.itens_empresa(c, EMP["aliases"]) if i["data"] >= "2018-01-01"]
ALI, IP = MAN.get("_processos_alias", {}), MAN.get("_item_processo", {})
chave = lambda i: (lambda k: ALI.get(k, k) if k else None)(IP.get(str(i["id"])) or prazos.chave(i["processo"]))
DUR = prazos.duracoes(AG)

dec = []
for i in its:
    v = c.execute("select * from votos where item_id=? and trecho is not null and trecho!='' order by eh_relator desc limit 1", (i["id"],)).fetchone()
    tema = (c.execute("select tema from item_temas where item_id=? limit 1", (i["id"],)).fetchone() or ["outros"])[0]
    pl = nc.placar(c, i["id"], i["resultado"])
    votos = [{"d": x["diretor"], "c": "relator" if x["eh_relator"] else (x["categoria"] or "vota")} for x in c.execute("select diretor, categoria, eh_relator from votos where item_id=?", (i["id"],))]
    dec.append({"id": i["id"], "data": i["data"], "n": i["numero"], "item": str(i["item"]), "proc": chave(i) or "sem nº", "assunto": i["assunto"] or "", "res": i["resultado"] or "",
                "rel": i["relator"] or "", "des": ROT.get(x := ((MAN.get(str(i["id"])) or {}).get("desfecho") or desfecho_item(c, i["id"])), x), "placar": pl[0], "pt": pl[1],
                "tema": tema.replace("_", " "), "link": mapa_tema.link(i["video_id"], (v["ts"] if v else None) or i["ts"]), "fala": (v["trecho"][:260] if v else ""), "quem": (v["diretor"] if v else ""), "votos": votos})
procs = collections.OrderedDict()
for x in sorted(dec, key=lambda x: x["data"]): procs.setdefault(x["proc"], []).append(x)
plist = []
for k, ss in procs.items():
    u = ss[-1]; r = u["res"].lower()
    st = "retirado" if re.match(r"\s*retirad", r) else "vista" if re.match(r"\s*(pedido de )?vista", r) else "decidido"
    du = DUR.get(k); e = prazos.estatistica(DUR, du[1]) if du else None
    plist.append({"proc": k, "titulo": ss[0]["assunto"][:140], "status": st, "rel": u["rel"], "tema": u["tema"], "ult": u["data"], "n": len(ss),
                  "dias": du[0] if du and du[2] > 1 else None, "med": e["mediana"] if e else None, "p25": e["p25"] if e else None, "p75": e["p75"] if e else None, "nsim": e["n"] if e else None, "sess": [s["id"] for s in ss]})
plist.sort(key=lambda p: p["ult"], reverse=True)
por = collections.defaultdict(list)
for v in DUR.values(): por[v[1]].append(v)
prazo_tipo = [{"t": t.replace("_", " "), **e} for t in por if (e := prazos.estatistica(DUR, t))]
prazo_tipo.sort(key=lambda x: x["mediana"])
cal = [dict(x, periodo=nc.periodo(x), dias_n=len(nc.dias_reuniao(x))) for x in ld(f"{D}/calendario.json", []) if max(nc.dias_reuniao(x)) >= HOJE.isoformat()][:4]
bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
pr = previsao.calcular(AG, EMP["aliases"])
def foto(n):
    for p in [(bios.get(n) or {}).get("foto"), f"{D}/dirigentes/{re.sub(r'[^a-z0-9]+', '-', n.lower())}.jpg"]:
        if p and os.path.exists(p):
            from PIL import Image; import io
            im = Image.open(p).convert("RGB"); im.thumbnail((160, 160)); b = io.BytesIO(); im.save(b, "JPEG", quality=80)
            return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    return ""
board = [{"n": n, "cargo": (bios.get(n) or {}).get("cargo", ""), "bio": ((bios.get(n) or {}).get("minibio") or "")[:320], "form": ((bios.get(n) or {}).get("formacao") or "")[:140], "foto": foto(n),
          "rel": sum(1 for x in dec if x["rel"] == n), "pac": round(100 * pr["por_diretor"].get(n, (0, 0))[0]) if n in pr["por_diretor"] else None} for n in pr["colegiado"]]
sups = [{"n": s.get("nome", ""), "u": s.get("superintendencia") or s.get("cargo") or ""} for s in ld(f"{D}/superintendentes.json", [])]
cad = ld(f"{D}/cadeiras.json", {}).get("cadeiras", [])
notas = [t for _, _, t in nc.notas(AG, EMP, [dict(i) for i in its], cal, cad, HOJE)]
sims = {}
for p in plist[:8]:
    s = similares.similares(AG, re.sub(r"[^\w\s]", " ", p["titulo"])[:120], 10)
    sims[p["proc"]] = [{"data": x["data"], "n": x["numero"], "assunto": (x["assunto"] or "")[:120], "des": ROT.get(x["desfecho"], x["desfecho"]), "rel": x["relator"] or "", "link": x["link"], "just": (x.get("justificativa") or "")[:200]} for x in s if x["id"] not in p["sess"]][:6]
DATA = {"emp": EMP["nome"].split("(")[0].strip(), "ag": AG.upper(), "hoje": HOJE.isoformat(), "dec": dec, "procs": plist, "prazo": prazo_tipo, "cal": cal, "board": board, "sups": sups, "cad": cad, "notas": notas, "sims": sims,
        "logo": d.img("nery_a"), "cli": d.b64(EMP.get("logo")) if EMP.get("logo") else ""}

H = r"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Monitoramento regulatório</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"><style>
:root{--az:#003B4C;--az2:#0F5468;--li:#BCCFFF;--ti:#0B1A20;--ci:#6B7780;--fi:#D5DCE0;--ne:#F2F5F7}
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ti);background:#fff;font-size:14px}
header{background:var(--az);color:#fff;padding:14px 24px;display:flex;align-items:center;gap:16px}header img{height:26px;background:#fff;padding:4px 8px;border-radius:3px}header h1{font-size:17px;font-weight:400;margin:0}header .sp{flex:1}header small{color:var(--li);font-size:12px}
nav{display:flex;gap:2px;padding:0 24px;border-bottom:1px solid var(--fi);overflow-x:auto;background:#fff;position:sticky;top:0;z-index:2}nav button{border:0;background:none;padding:12px 14px;font:inherit;font-size:13px;color:var(--ci);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap}nav button.on{color:var(--az);border-color:var(--az);font-weight:500}
main{padding:20px 24px;max-width:1400px;margin:auto}section{display:none}section.on{display:block}h2{font-weight:400;color:var(--az);font-size:22px;margin:4px 0 14px}h3{font-weight:500;font-size:14px;color:var(--az2);margin:18px 0 8px}
.kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:14px}.kp div{border-top:1px solid var(--az);padding-top:6px}.kp b{font-size:28px;font-weight:300;color:var(--az);display:block}.kp span{font-size:12px;color:var(--ci)}
table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;font-weight:500;color:var(--ci);font-size:11px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--ti);padding:6px}td{border-bottom:1px solid var(--fi);padding:7px 6px;vertical-align:top}tr.cl{cursor:pointer}tr.cl:hover{background:var(--ne)}
.sl{display:inline-block;font-size:11px;padding:1px 7px;font-weight:600}.unanime{background:var(--az);color:#fff}.maioria{background:var(--li);color:var(--az)}.neutro{background:var(--fi)}
.st-decidido{color:var(--az)}.st-vista,.st-retirado{color:#000;background:var(--li);padding:1px 6px}
.nb{border-left:3px solid var(--li);background:var(--ne);padding:10px 14px;margin:8px 0}.nb li{margin:4px 0}
.filtros{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}select,input{font:inherit;padding:7px 9px;border:1px solid var(--fi);background:#fff}input.busca{flex:1;min-width:240px}
.tl{border-left:2px solid var(--fi);margin-left:8px;padding-left:18px}.ev{position:relative;padding:8px 0 12px}.ev:before{content:"";position:absolute;left:-25px;top:12px;width:10px;height:10px;border-radius:50%;background:var(--az)}.ev .dt{font-size:12px;color:var(--ci)}.ev q{display:block;font-style:italic;color:#333;margin-top:4px}
.bar{display:grid;grid-template-columns:200px 1fr 70px;gap:10px;align-items:center;margin:6px 0;font-size:13px}.trk{position:relative;height:14px;background:var(--ne)}.iqr{position:absolute;top:0;bottom:0;background:var(--li)}.med{position:absolute;top:-3px;width:3px;height:20px;background:var(--az)}.me{position:absolute;top:-5px;width:12px;height:12px;border-radius:50%;background:#000;border:2px solid #fff}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.card{border:1px solid var(--fi);border-top:3px solid var(--az);padding:10px 12px}.card.v{border-top-color:var(--li);background:var(--ne)}.card b{font-size:20px;font-weight:300;color:var(--az);display:block}
.pp{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}.pe{display:flex;gap:12px;border-top:1px solid var(--fi);padding-top:10px}.pe img,.pe .ini{width:64px;height:64px;border-radius:50%;object-fit:cover;flex:none;background:var(--ne);display:flex;align-items:center;justify-content:center;color:var(--az2)}.pe p{margin:4px 0;font-size:12.5px}
a{color:var(--az)}small.c{color:var(--ci)}footer{color:var(--ci);font-size:11.5px;padding:18px 24px;border-top:1px solid var(--fi);margin-top:30px}
@media(max-width:700px){.bar{grid-template-columns:110px 1fr 50px}main{padding:14px}}
</style></head><body>
<header><img id="lg"><div><h1 id="tt"></h1><small id="st"></small></div><span class="sp"></span><img id="lc"></header>
<nav id="nv"></nav><main id="mn"></main>
<footer>Protótipo estático: dados públicos da agência até a data indicada; estimativas não são certeza; legenda automática pode errar nomes e números. Grupo Nery · inteligência regulatória.</footer>
<script>const D=__DATA__;
const $=s=>document.querySelector(s),E=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])),fd=s=>s?s.slice(8,10)+"/"+s.slice(5,7)+"/"+s.slice(0,4):"";
$("#tt").textContent=D.emp+" · "+D.ag;$("#st").textContent="Monitorar → Analisar → Antecipar · dados até "+fd(D.hoje);$("#lg").src=D.logo;if(D.cli)$("#lc").src=D.cli;else $("#lc").remove();
const T=[["geral","1 Visão geral"],["mapa","2 Mapeamento"],["prazo","3 Prazo"],["agenda","4 Agenda"],["agencia","5 Agência"],["busca","6 Busca"],["comp","7 Comparativa"],["cliente","8 Visão do cliente"]];
$("#nv").innerHTML=T.map(([k,t],i)=>`<button data-k="${k}" class="${i?"":"on"}">${t}</button>`).join("");$("#mn").innerHTML=T.map(([k],i)=>`<section id="s-${k}" class="${i?"":"on"}"></section>`).join("");
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>ir(b.dataset.k));
function ir(k,p){document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x.dataset.k==k));document.querySelectorAll("section").forEach(x=>x.classList.toggle("on",x.id=="s-"+k));if(p)mapa(p);scrollTo(0,0)}
const sl=d=>`<span class="sl ${d.pt}">${E(d.placar)}</span>`,dec=Object.fromEntries(D.dec.map(x=>[x.id,x]));
// 1
(function(){const P=D.procs,ab=P.filter(p=>p.status!="decidido");
$("#s-geral").innerHTML=`<h2>Visão geral</h2><div class="kp"><div><b>${P.length}</b><span>processos monitorados</span></div><div><b>${ab.length}</b><span>em andamento (vista ou retirado)</span></div><div><b>${D.dec.length}</b><span>decisões da diretoria desde 2018</span></div><div><b>${Math.round(100*D.dec.filter(x=>x.pt=="unanime").length/Math.max(D.dec.length,1))}%</b><span>decididas por unanimidade</span></div></div>
${D.notas.length?`<div class="nb"><b>O que observar</b><ul>${D.notas.map(n=>`<li>${n}</li>`).join("")}</ul></div>`:""}
<div class="filtros"><select id="fs"><option value="">Todos os status</option><option>decidido</option><option>vista</option><option>retirado</option></select><select id="fr"><option value="">Todos os relatores</option>${[...new Set(P.map(p=>p.rel).filter(Boolean))].map(r=>`<option>${E(r)}</option>`).join("")}</select><select id="ft"><option value="">Todos os temas</option>${[...new Set(P.map(p=>p.tema))].map(r=>`<option>${E(r)}</option>`).join("")}</select></div>
<table><thead><tr><th>Status</th><th>Processo</th><th>Assunto</th><th>Relator</th><th>Tema</th><th>Última sessão</th><th>Dias na diretoria</th></tr></thead><tbody id="tp"></tbody></table>
<h3>Movimentações mais recentes</h3><table><tbody>${D.dec.slice(-6).reverse().map(x=>`<tr><td>${fd(x.data)}<br><small class="c">${x.n}ª, item ${E(x.item)}</small></td><td>${E(x.assunto.slice(0,140))}</td><td>${sl(x)}</td><td>${E(x.des)}</td><td><a href="${x.link}" target="_blank">▶ minuto</a></td></tr>`).join("")}</tbody></table>`;
const f=()=>{const s=$("#fs").value,r=$("#fr").value,t=$("#ft").value;$("#tp").innerHTML=P.filter(p=>(!s||p.status==s)&&(!r||p.rel==r)&&(!t||p.tema==t)).map(p=>`<tr class="cl" onclick="ir('mapa','${p.proc}')"><td><span class="st-${p.status}">${p.status}</span></td><td>${E(p.proc)}</td><td>${E(p.titulo)}</td><td>${E(p.rel)}</td><td>${E(p.tema)}</td><td>${fd(p.ult)}</td><td>${p.dias??"—"}</td></tr>`).join("")};["#fs","#fr","#ft"].forEach(s=>$(s).onchange=f);f()})();
// 2
function mapa(k){const p=D.procs.find(x=>x.proc==k)||D.procs[0];$("#s-mapa").innerHTML=`<h2>Mapeamento do processo</h2><select id="mp">${D.procs.map(x=>`<option ${x.proc==p.proc?"selected":""} value="${E(x.proc)}">${E(x.proc)} · ${E(x.titulo.slice(0,70))}</option>`).join("")}</select>
<p><b>${E(p.titulo)}</b><br><small class="c">Status: ${p.status} · relator: ${E(p.rel)} · área técnica e etapa no SEI: a informar pelo cliente</small></p>
<div class="tl">${p.sess.map(i=>dec[i]).map(x=>`<div class="ev"><div class="dt">${fd(x.data)} · ${x.n}ª reunião, item ${E(x.item)}</div><b>${E(x.res.slice(0,160))}</b> ${sl(x)} <small class="c">${E(x.des)}</small><br><small class="c">${x.votos.map(v=>E(v.d.split(" ")[0])+": "+E(v.c)).join(" · ")}</small>${x.fala?`<q>«${E(x.fala)}» — ${E(x.quem)}</q>`:""}<a href="${x.link}" target="_blank">▶ vídeo no minuto</a></div>`).join("")}
${p.status!="decidido"?`<div class="ev"><div class="dt">próximo passo previsto</div><b>volta à pauta</b> <small class="c">${D.cal[0]?"próxima reunião: "+D.cal[0].periodo:""} (inferência)</small></div>`:""}</div>`;$("#mp").onchange=e=>mapa(e.target.value)}mapa([...D.procs].sort((a,b)=>b.n-a.n)[0]?.proc);
// 3
(function(){const mx=Math.max(...D.prazo.map(x=>x.p75),...D.procs.map(p=>p.dias||0),1);
$("#s-prazo").innerHTML=`<h2>Inteligência de prazo</h2><p><small class="c">Dias na diretoria (1ª sessão → decisão), processos com mais de uma sessão desde 2018. Faixa lilás = 25% a 75% dos casos; traço = mediana.</small></p>
<h3>Por tipo de processo</h3>${D.prazo.map(x=>`<div class="bar"><span>${E(x.t)} <small class="c">n=${x.n}</small></span><span class="trk"><i class="iqr" style="left:${100*x.p25/mx}%;width:${100*(x.p75-x.p25)/mx}%"></i><i class="med" style="left:${100*x.mediana/mx}%"></i></span><b>${Math.round(x.mediana)} d</b></div>`).join("")}
<h3>Processos da empresa × semelhantes (ponto preto = este processo)</h3>${D.procs.filter(p=>p.dias!=null&&p.med!=null&&p.n>1).map(p=>`<div class="bar"><span>${E(p.proc)}</span><span class="trk"><i class="iqr" style="left:${100*p.p25/mx}%;width:${100*(p.p75-p.p25)/mx}%"></i><i class="med" style="left:${100*p.med/mx}%"></i><i class="me" style="left:${100*p.dias/mx}%"></i></span><b>${p.dias} d</b></div><small class="c">${p.dias>p.p75?"acima":p.dias<p.p25?"abaixo":"dentro"} da faixa típica de ${p.nsim} semelhantes (${E(p.tema)})</small>`).join("")||"<p>Nenhum processo da empresa com mais de uma sessão.</p>"}`})();
// 4
$("#s-agenda").innerHTML=`<h2>Agenda regulatória</h2><div class="cards">${D.cal.map(x=>`<div class="card ${x.formato=="virtual"?"v":""}"><b>${E(x.periodo)}</b>${E(x.reuniao)}ª reunião da diretoria<br><small class="c">${x.formato=="virtual"?"virtual · "+x.dias_n+" dias · sem transmissão: resultado só na ata":E(x.formato||"")+" · transmitida"}</small>${x.pauta?`<br><a href="${x.pauta}" target="_blank">pauta publicada</a>`:"<br><small class=c>pauta a publicar</small>"}</div>`).join("")}</div>
<h3>Reunião → item → processo → resultado</h3><table><thead><tr><th>Reunião</th><th>Item</th><th>Processo</th><th>Resultado</th><th>Placar</th><th></th></tr></thead><tbody>${D.dec.slice(-15).reverse().map(x=>`<tr><td>${x.n}ª · ${fd(x.data)}</td><td>${E(x.item)}</td><td>${E(x.proc)}</td><td>${E(x.res.slice(0,110))}</td><td>${sl(x)}</td><td><a href="${x.link}" target="_blank">▶</a></td></tr>`).join("")}</tbody></table>
<p><small class="c">Aviso prévio por e-mail: no pacote, o alerta pré-pauta sai quando a pauta é publicada.</small></p>`;
// 5
$("#s-agencia").innerHTML=`<h2>Inteligência sobre a agência</h2><div class="pp">${D.board.map(b=>`<div class="pe">${b.foto?`<img src="${b.foto}">`:`<div class="ini">${E(b.n.split(" ").map(w=>w[0]).join("").slice(0,2))}</div>`}<div><b>${E(b.n)}</b><br><small class="c">${E(b.cargo)}</small><p>${E(b.bio)}</p><p><small class="c">Formação: ${E(b.form)}</small></p><p>Relatou <b>${b.rel}</b> decisões da empresa${b.pac!=null?` · acompanha o relator em ${b.pac}% (temas da empresa)`:""}</p></div></div>`).join("")}</div>
<h3>Cadeiras e mandatos</h3><table><thead><tr><th>Cadeira</th><th>Ocupante atual</th><th>Mandato até</th><th>Ex-ocupantes desde 2018</th></tr></thead><tbody>${D.cad.map(c=>{const o=c.ocupantes||[],a=o.find(x=>!x.saida);return `<tr><td>${E(c.cadeira)}</td><td>${a?E(a.nome)+" <small class=c>("+E(a.tipo)+")</small>":"<b>VAGO</b>"}</td><td>${a?fd(a.fim_legal):""}</td><td><small class="c">${o.filter(x=>x.saida).map(x=>E(x.nome)).join(" · ")}</small></td></tr>`}).join("")}</tbody></table>
<h3>Superintendências</h3><table><tbody>${D.sups.map(s=>`<tr><td>${E(s.n)}</td><td>${E(s.u)}</td></tr>`).join("")}</tbody></table>`;
// 6
$("#s-busca").innerHTML=`<h2>Busca e banco de dados</h2><div class="filtros"><input class="busca" id="q" placeholder="Busque por processo, assunto, relator, tema ou ano (ex.: passivo, Caio, 2025)"></div><div id="rq"></div>`;
const busca=()=>{const q=$("#q").value.toLowerCase().trim(),r=D.dec.filter(x=>!q||(x.proc+" "+x.assunto+" "+x.rel+" "+x.tema+" "+x.data+" "+x.res).toLowerCase().includes(q)).reverse();$("#rq").innerHTML=`<p><small class="c">${r.length} decisões</small></p><table><thead><tr><th>Sessão</th><th>Processo</th><th>Assunto</th><th>Relator</th><th>Resultado</th><th>Para a empresa</th><th></th></tr></thead><tbody>${r.slice(0,80).map(x=>`<tr><td>${fd(x.data)}<br><small class=c>${x.n}ª, item ${E(x.item)}</small></td><td>${E(x.proc)}</td><td>${E(x.assunto.slice(0,150))}</td><td>${E(x.rel)}</td><td>${sl(x)}</td><td>${E(x.des)}</td><td><a href="${x.link}" target="_blank">▶</a></td></tr>`).join("")}</tbody></table>`};$("#q").oninput=busca;busca();
// 7
$("#s-comp").innerHTML=`<h2>Inteligência comparativa</h2>${D.procs.filter(p=>D.sims[p.proc]&&D.sims[p.proc].length).slice(0,6).map(p=>{const s=D.sims[p.proc],c={};s.forEach(x=>c[x.des]=(c[x.des]||0)+1);return `<h3>${E(p.proc)} · ${E(p.titulo.slice(0,90))}</h3><p><small class="c">Padrão nos ${s.length} casos mais parecidos: ${Object.entries(c).map(([k,v])=>v+" "+E(k)).join(", ")}</small></p><table><tbody>${s.map(x=>`<tr><td>${fd(x.data)}<br><small class=c>${x.n}ª</small></td><td>${E(x.assunto)}<br><small class=c>${E(x.just)}</small></td><td>${E(x.des)}</td><td>${E(x.rel)}</td><td><a href="${x.link}" target="_blank">▶</a></td></tr>`).join("")}</tbody></table>`}).join("")}`;
// 8
$("#s-cliente").innerHTML=`<h2>Visão do cliente</h2>${D.notas.length?`<div class="nb"><b>Alertas e ações</b><ul>${D.notas.map(n=>`<li>${n}</li>`).join("")}</ul></div>`:""}<div class="cards">${D.procs.slice(0,9).map(p=>`<div class="card ${p.status!="decidido"?"v":""}"><small class="c">${E(p.proc)}</small><br><b style="font-size:15px;font-weight:500">${E(p.status)}</b><p style="margin:6px 0">${E(p.titulo.slice(0,110))}</p><small class="c">Relator: ${E(p.rel)} · última sessão ${fd(p.ult)}<br>Prazo típico do tema: ${p.med?Math.round(p.med)+" dias (estimativa)":"sem base"}<br>Próximo marco: ${p.status!="decidido"?(D.cal[0]?"volta à pauta, "+E(D.cal[0].periodo):"volta à pauta"):"cumprimento ou recurso"}</small><br><a href="#" onclick="ir('mapa','${p.proc}');return false">ver histórico →</a></div>`).join("")}</div>`;
</script></body></html>"""
out = f"{P}/dashboard.html"
open(out, "w").write(H.replace("__DATA__", json.dumps(DATA, ensure_ascii=False)))
print(out, os.path.getsize(out) // 1024, "KB ·", len(dec), "decisões ·", len(plist), "processos")
