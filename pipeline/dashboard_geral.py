"""Dashboard GERAL de consulta (todas as agências com base de votos, várias empresas ao mesmo tempo) — HTML único, dados públicos, design Grupo Nery.
Filtros: agências, empresas (uma ou várias, por nome), período. 8 abas: visão geral, mapeamento, prazo, agenda, agências, busca, comparativa, visão por empresa.
Uso: python3 pipeline/dashboard_geral.py   → documentos/dashboard/index.html (pode ir ao GitHub: só dado público)."""
import sys, os, re, json, datetime, collections, base64, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import previsao, prazos, mapa_tema, notas_cliente as nc, design as d
AGS = [a for a in ["antt", "antaq", "anm", "aneel", "anp"] if os.path.exists(("data" if a == "antt" else f"data/{a}") + "/regulacao.db")]
HOJE = datetime.date.today(); TRES = (HOJE - datetime.timedelta(days=3 * 365)).isoformat()
ld = lambda p, x: json.load(open(p)) if os.path.exists(p) else x
OUT = "documentos/dashboard"; os.makedirs(OUT, exist_ok=True)
DEC, PROCS, PRAZO, CAL, DIR = [], [], [], [], {}
for ag in AGS:
    D = "data" if ag == "antt" else f"data/{ag}"
    try: c = previsao.conn(ag); c.execute("select 1 from itens limit 1")
    except Exception: continue
    tema_de = {iid: t for iid, t in c.execute("select item_id, tema from item_temas")}
    div = {x for (x,) in c.execute("select distinct item_id from votos where categoria in ('vencido','revisor_diverge')")}
    fala = {}
    for v in c.execute("select item_id, diretor, trecho, ts, trecho_t from votos where trecho is not null and trecho!='' order by eh_relator desc"):
        fala.setdefault(v["item_id"], v)
    rows = c.execute("select i.id, i.item, i.processo, i.interessado, i.assunto, i.resultado, i.relator, i.ts, r.numero, r.data, r.video_id from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01' order by r.data").fetchall()
    for i in rows:
        r = (i["resultado"] or "").lower()
        pt = "retirado" if re.match(r"\s*retirad", r) else "vista" if re.match(r"\s*(pedido de )?vista", r) else ("maioria" if i["id"] in div or "maioria" in r else "unanime")
        f = fala.get(i["id"]) if i["data"] >= TRES else None
        DEC.append({"a": ag.upper(), "id": f"{ag}{i['id']}", "dt": i["data"], "n": str(i["numero"])[:40], "it": str(i["item"]), "p": prazos.chave(i["processo"]) or "", "int": (i["interessado"] or "")[:120],
                    "as": (i["assunto"] or "")[:220], "r": (i["resultado"] or "")[:140], "rel": i["relator"] or "", "pt": pt, "t": (tema_de.get(i["id"]) or "outros").replace("_", " "),
                    "l": mapa_tema.link(i["video_id"], (f["ts"] if f else None) or i["ts"]), "f": (f["trecho"][:180] if f else ""), "q": (f["diretor"] if f else "")})
    DUR = prazos.duracoes(ag); por = collections.defaultdict(list)
    for k, v in DUR.items(): por[v[1]].append(v)
    for t in por:
        e = prazos.estatistica(DUR, t)
        if e: PRAZO.append({"a": ag.upper(), "t": t.replace("_", " "), "n": e["n"], "med": e["mediana"], "p25": e["p25"], "p75": e["p75"]})
    for k, v in DUR.items():
        if v[2] > 1: PROCS.append({"a": ag.upper(), "p": k, "dias": v[0], "t": v[1].replace("_", " "), "ok": v[3]})
    for x in ld(f"{D}/calendario.json", []):
        if max(nc.dias_reuniao(x)) >= HOJE.isoformat(): CAL.append({"a": ag.upper(), "r": str(x.get("reuniao", "")), "per": nc.periodo(x) + "/" + x["data"][:4], "dt": x["data"], "fmt": x.get("formato", ""), "dias": len(nc.dias_reuniao(x)), "pauta": x.get("pauta")})
    bios = {b["diretor"]: b for b in ld(f"{D}/bios.json", [])}
    try: board = previsao.colegiado_atual(c)[0]
    except Exception: board = []
    def foto(n):
        for p in [(bios.get(n) or {}).get("foto"), f"{D}/dirigentes/{re.sub(r'[^a-z0-9]+', '-', n.lower())}.jpg"]:
            if p and os.path.exists(p):
                from PIL import Image
                im = Image.open(p).convert("RGB"); im.thumbnail((120, 120)); b = io.BytesIO(); im.save(b, "JPEG", quality=75)
                return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
        return ""
    DIR[ag.upper()] = [{"n": n, "cargo": (bios.get(n) or {}).get("cargo", ""), "bio": ((bios.get(n) or {}).get("minibio") or "")[:260], "foto": foto(n)} for n in board]
MA = ld("data/mandatos_agencias.json", {}).get("agencias", {})
TR = {}
for ag, d0 in [("ANTT", "data"), ("ANTAQ", "data/antaq"), ("ANM", "data/anm"), ("ANEEL", "data/aneel")]:
    t = ld(f"{d0}/transparencia.json", {})
    if t: TR[ag] = sum(x["nota"] for x in t.get("criterios", []))
DATA = {"hoje": HOJE.isoformat(), "dec": DEC, "procs": PROCS, "prazo": PRAZO, "cal": sorted(CAL, key=lambda x: x["dt"]), "dir": DIR, "ma": MA, "tr": TR, "logo": d.img("nery_a")}

H = r"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Inteligência regulatória · consulta geral</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet"><style>
:root{--az:#003B4C;--az2:#0F5468;--li:#BCCFFF;--ti:#0B1A20;--ci:#6B7780;--fi:#D5DCE0;--ne:#F2F5F7}*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,sans-serif;color:var(--ti);font-size:14px;background:#fff}
header{background:var(--az);color:#fff;padding:12px 24px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}header img{height:24px;background:#fff;padding:4px 8px;border-radius:3px}header h1{font-size:17px;font-weight:400;margin:0}header small{color:var(--li);font-size:12px;display:block}
.fil{background:var(--ne);padding:10px 24px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;border-bottom:1px solid var(--fi)}.fil label{font-size:12px;color:var(--ci)}.ags label{margin-right:8px;color:var(--ti);font-size:13px}input,select{font:inherit;padding:6px 8px;border:1px solid var(--fi);background:#fff}#emp{min-width:280px}
nav{display:flex;gap:2px;padding:0 24px;border-bottom:1px solid var(--fi);overflow-x:auto;position:sticky;top:0;background:#fff;z-index:2}nav button{border:0;background:none;padding:11px 13px;font:inherit;font-size:13px;color:var(--ci);cursor:pointer;border-bottom:2px solid transparent;white-space:nowrap}nav button.on{color:var(--az);border-color:var(--az);font-weight:500}
main{padding:18px 24px;max-width:1400px;margin:auto}section{display:none}section.on{display:block}h2{font-weight:400;color:var(--az);font-size:21px;margin:2px 0 12px}h3{font-weight:500;font-size:14px;color:var(--az2);margin:18px 0 8px}
.kp{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:12px}.kp div{border-top:1px solid var(--az);padding-top:6px}.kp b{font-size:26px;font-weight:300;color:var(--az);display:block}.kp span{font-size:12px;color:var(--ci)}
table{width:100%;border-collapse:collapse;font-size:13px}th{text-align:left;font-weight:500;color:var(--ci);font-size:11px;text-transform:uppercase;letter-spacing:.05em;border-bottom:1px solid var(--ti);padding:6px}td{border-bottom:1px solid var(--fi);padding:6px;vertical-align:top}
.sl{display:inline-block;font-size:11px;padding:1px 7px;font-weight:600}.unanime{background:var(--az);color:#fff}.maioria{background:var(--li);color:var(--az)}.vista,.retirado{background:var(--fi)}
.bar{display:grid;grid-template-columns:230px 1fr 70px;gap:10px;align-items:center;margin:5px 0;font-size:13px}.trk{position:relative;height:13px;background:var(--ne)}.iqr{position:absolute;top:0;bottom:0;background:var(--li)}.med{position:absolute;top:-3px;width:3px;height:19px;background:var(--az)}.fill{position:absolute;top:0;bottom:0;left:0;background:var(--az)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px}.card{border:1px solid var(--fi);border-top:3px solid var(--az);padding:10px 12px}.card.v{border-top-color:var(--li);background:var(--ne)}.card b{font-size:18px;font-weight:300;color:var(--az);display:block}
.pp{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.pe{display:flex;gap:10px;border-top:1px solid var(--fi);padding-top:8px}.pe img,.pe .ini{width:54px;height:54px;border-radius:50%;object-fit:cover;flex:none;background:var(--ne);display:flex;align-items:center;justify-content:center;color:var(--az2)}.pe p{margin:3px 0;font-size:12px}
.tl{border-left:2px solid var(--fi);margin-left:8px;padding-left:18px}.ev{position:relative;padding:7px 0 11px}.ev:before{content:"";position:absolute;left:-25px;top:11px;width:10px;height:10px;border-radius:50%;background:var(--az)}.ev q{display:block;font-style:italic;color:#333;margin-top:3px}
a{color:var(--az)}small.c{color:var(--ci)}footer{color:var(--ci);font-size:11.5px;padding:16px 24px;border-top:1px solid var(--fi);margin-top:28px}
</style></head><body>
<header><img id="lg"><div><h1>Inteligência de decisão regulatória · consulta geral</h1><small id="st"></small></div></header>
<div class="fil"><span class="ags" id="ags"></span><label>Empresas <input id="emp" placeholder="uma ou várias, separadas por vírgula (ex.: Vale, Rumo, Energisa)"></label><label>De <select id="de"></select></label><label>até <select id="ate"></select></label></div>
<nav id="nv"></nav><main id="mn"></main>
<footer>Consulta de demonstração com dados públicos das reuniões de diretoria (vídeos oficiais), calendário e Diário Oficial. Legenda automática pode errar nomes e números; estimativas não são certeza. Grupo Nery.</footer>
<script>const D=__DATA__;
const $=s=>document.querySelector(s),E=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])),fd=s=>s?s.slice(8,10)+"/"+s.slice(5,7)+"/"+s.slice(0,4):"";
$("#lg").src=D.logo;$("#st").textContent="Todas as agências com base de votos · "+D.dec.length.toLocaleString("pt-BR")+" decisões · dados até "+fd(D.hoje);
const AG=[...new Set(D.dec.map(x=>x.a))];$("#ags").innerHTML=AG.map(a=>`<label><input type="checkbox" value="${a}" checked> ${a}</label>`).join("");
const anos=[...new Set(D.dec.map(x=>x.dt.slice(0,4)))].sort();$("#de").innerHTML=anos.map(a=>`<option>${a}</option>`).join("");$("#ate").innerHTML=anos.map(a=>`<option ${a==anos.at(-1)?"selected":""}>${a}</option>`).join("");$("#de").value=String(+anos.at(-1)-2>=+anos[0]?+anos.at(-1)-2:anos[0]);
const T=[["geral","1 Visão geral"],["mapa","2 Mapeamento"],["prazo","3 Prazo"],["agenda","4 Agenda"],["agencia","5 Agências"],["busca","6 Busca"],["comp","7 Comparativa"],["emp","8 Visão por empresa"]];
$("#nv").innerHTML=T.map(([k,t],i)=>`<button data-k="${k}" class="${i?"":"on"}">${t}</button>`).join("");$("#mn").innerHTML=T.map(([k],i)=>`<section id="s-${k}" class="${i?"":"on"}"></section>`).join("");
document.querySelectorAll("nav button").forEach(b=>b.onclick=()=>{document.querySelectorAll("nav button").forEach(x=>x.classList.toggle("on",x==b));document.querySelectorAll("section").forEach(x=>x.classList.toggle("on",x.id=="s-"+b.dataset.k))});
const sl=x=>`<span class="sl ${x.pt}">${{unanime:"unânime",maioria:"maioria",vista:"vista",retirado:"retirado"}[x.pt]}</span>`;
function filtro(){const ag=[...document.querySelectorAll("#ags input:checked")].map(x=>x.value),em=$("#emp").value.split(",").map(s=>s.trim().toLowerCase()).filter(Boolean),de=$("#de").value,ate=$("#ate").value;
 const F=D.dec.filter(x=>ag.includes(x.a)&&x.dt.slice(0,4)>=de&&x.dt.slice(0,4)<=ate&&(!em.length||em.some(e=>(x.int+" "+x.as).toLowerCase().includes(e))));return {F,ag,em}}
function pct(a,b){return b?Math.round(100*a/b):0}
function render(){const {F,ag,em}=filtro();
 // 1
 const byA=ag.map(a=>{const X=F.filter(x=>x.a==a);return {a,n:X.length,u:X.filter(x=>x.pt=="unanime").length,v:X.filter(x=>x.pt=="vista").length,r:X.filter(x=>x.pt=="retirado").length}});
 $("#s-geral").innerHTML=`<h2>Visão geral${em.length?" · "+E(em.join(", ")):""}</h2><div class="kp"><div><b>${F.length.toLocaleString("pt-BR")}</b><span>decisões no recorte</span></div><div><b>${pct(F.filter(x=>x.pt=="unanime").length,F.length)}%</b><span>unânimes</span></div><div><b>${pct(F.filter(x=>x.pt=="vista").length,F.length)}%</b><span>com pedido de vista</span></div><div><b>${new Set(F.map(x=>x.p).filter(Boolean)).size}</b><span>processos com nº</span></div></div>
 <table><thead><tr><th>Agência</th><th>Decisões</th><th>Unânimes</th><th>Vista</th><th>Retirados</th></tr></thead><tbody>${byA.map(x=>`<tr><td><b>${x.a}</b></td><td>${x.n}</td><td>${pct(x.u,x.n)}%</td><td>${pct(x.v,x.n)}%</td><td>${pct(x.r,x.n)}%</td></tr>`).join("")}</tbody></table>
 <h3>Movimentações mais recentes</h3><table><tbody>${F.slice(-12).reverse().map(x=>`<tr><td><b>${x.a}</b> · ${fd(x.dt)}<br><small class=c>${E(x.n)}, item ${E(x.it)}</small></td><td>${E(x.as.slice(0,150))}<br><small class=c>${E(x.int)}</small></td><td>${sl(x)}</td><td><a href="${x.l}" target="_blank">▶</a></td></tr>`).join("")}</tbody></table>`;
 // 2
 const ps=[...new Set(F.map(x=>x.p).filter(Boolean))];const pc=ps.map(p=>[p,F.filter(x=>x.p==p).length]).sort((a,b)=>b[1]-a[1]).slice(0,300);
 $("#s-mapa").innerHTML=`<h2>Mapeamento do processo</h2><select id="mp">${pc.map(([p,n])=>`<option value="${p}">${p} · ${n} sessões</option>`).join("")}</select><div id="tl"></div>`;
 const tl=p=>{$("#tl").innerHTML=`<div class="tl">${F.filter(x=>x.p==p).map(x=>`<div class="ev"><small class=c>${x.a} · ${fd(x.dt)} · ${E(x.n)}, item ${E(x.it)}</small><br><b>${E(x.r)}</b> ${sl(x)}<br>${E(x.as.slice(0,180))}${x.f?`<q>«${E(x.f)}» (${E(x.q)})</q>`:""}<a href="${x.l}" target="_blank">▶ vídeo no minuto</a></div>`).join("")}</div>`};$("#mp").onchange=e=>tl(e.target.value);if(pc[0])tl(pc[0][0]);
 // 3
 const P=D.prazo.filter(x=>ag.includes(x.a)).sort((a,b)=>a.med-b.med),mx=Math.max(...P.map(x=>x.p75),1);
 $("#s-prazo").innerHTML=`<h2>Inteligência de prazo</h2><p><small class=c>Dias na diretoria (1ª sessão → decisão), processos com mais de uma sessão desde 2018. Lilás = 25% a 75%; traço = mediana.</small></p>${P.map(x=>`<div class="bar"><span><b>${x.a}</b> ${E(x.t)} <small class=c>n=${x.n}</small></span><span class="trk"><i class="iqr" style="left:${100*x.p25/mx}%;width:${100*(x.p75-x.p25)/mx}%"></i><i class="med" style="left:${100*x.med/mx}%"></i></span><b>${Math.round(x.med)} d</b></div>`).join("")}`;
 // 4
 $("#s-agenda").innerHTML=`<h2>Agenda regulatória</h2><div class="cards">${D.cal.filter(x=>ag.includes(x.a)).map(x=>`<div class="card ${x.fmt=="virtual"?"v":""}"><small class=c>${x.a}</small><b>${E(x.per)}</b>${E(x.r)} ${/^\d/.test(x.r)?"ª reunião":""}<br><small class=c>${x.fmt=="virtual"?"virtual · "+x.dias+" dias · sem transmissão":E(x.fmt)}</small>${x.pauta?`<br><a href="${x.pauta}" target="_blank">pauta</a>`:""}</div>`).join("")||"<p>Sem reuniões futuras cadastradas.</p>"}</div>`;
 // 5
 const MA=Object.entries(D.ma);
 $("#s-agencia").innerHTML=`<h2>Agências e diretorias</h2><table><thead><tr><th>Agência</th><th>Titulares</th><th>Cadeiras vagas</th><th>Vaga mais antiga</th><th>Transparência</th></tr></thead><tbody>${MA.map(([a,p])=>{const vg=p.filter(x=>x.tipo=="vaga");const d0=vg.map(x=>x.vaga_desde).sort()[0];return `<tr><td><b>${a}</b></td><td>${p.filter(x=>x.tipo=="titular").length}</td><td>${vg.length}</td><td>${d0?fd(d0):"—"}</td><td>${D.tr[a]!=null?D.tr[a]+"/16":"—"}</td></tr>`}).join("")}</tbody></table>
 ${ag.map(a=>D.dir[a]?`<h3>${a}: diretoria em exercício</h3><div class="pp">${D.dir[a].map(b=>`<div class="pe">${b.foto?`<img src="${b.foto}">`:`<div class="ini">${E(b.n.split(" ").map(w=>w[0]).join("").slice(0,2))}</div>`}<div><b>${E(b.n)}</b><br><small class=c>${E(b.cargo)}</small><p>${E(b.bio)}</p></div></div>`).join("")}</div>`:"").join("")}`;
 // 6
 $("#s-busca").innerHTML=`<h2>Busca e banco de dados</h2><input id="q" style="width:100%" placeholder="processo, assunto, relator, tema, empresa…"><div id="rq"></div>`;
 const bq=()=>{const q=$("#q").value.toLowerCase().trim(),R=F.filter(x=>!q||(x.p+" "+x.as+" "+x.rel+" "+x.t+" "+x.int+" "+x.r).toLowerCase().includes(q)).reverse();$("#rq").innerHTML=`<p><small class=c>${R.length} decisões (mostrando até 150)</small></p><table><thead><tr><th>Sessão</th><th>Processo</th><th>Assunto / interessado</th><th>Relator</th><th>Resultado</th><th></th></tr></thead><tbody>${R.slice(0,150).map(x=>`<tr><td><b>${x.a}</b> ${fd(x.dt)}<br><small class=c>${E(x.n)}, item ${E(x.it)}</small></td><td>${E(x.p)}</td><td>${E(x.as.slice(0,160))}<br><small class=c>${E(x.int)}</small></td><td>${E(x.rel)}</td><td>${sl(x)}</td><td><a href="${x.l}" target="_blank">▶</a></td></tr>`).join("")}</tbody></table>`};$("#q").oninput=bq;bq();
 // 7
 const tem={};F.forEach(x=>{const k=x.a+" · "+x.t;tem[k]=tem[k]||{n:0,u:0,v:0};tem[k].n++;if(x.pt=="unanime")tem[k].u++;if(x.pt=="vista")tem[k].v++});const TT=Object.entries(tem).filter(([k,v])=>v.n>=10).sort((a,b)=>b[1].n-a[1].n).slice(0,30);
 $("#s-comp").innerHTML=`<h2>Inteligência comparativa</h2><h3>Padrão por agência e tema (mínimo 10 decisões)</h3>${TT.map(([k,v])=>`<div class="bar"><span>${E(k)} <small class=c>n=${v.n}</small></span><span class="trk"><i class="fill" style="width:${pct(v.u,v.n)}%"></i></span><b>${pct(v.u,v.n)}%</b></div>`).join("")}<p><small class=c>Barra = % decidido por unanimidade. Diferenças entre agências no mesmo tema indicam padrões distintos de colegiado.</small></p>`;
 // 8
 const emps=em.length?em:[];
 $("#s-emp").innerHTML=`<h2>Visão por empresa</h2>${emps.length?"":"<p>Digite uma ou várias empresas no filtro acima (separadas por vírgula) para comparar lado a lado.</p>"}<div class="cards">${emps.map(e=>{const X=F.filter(x=>(x.int+" "+x.as).toLowerCase().includes(e));const rel={};X.forEach(x=>{if(x.rel)rel[x.rel]=(rel[x.rel]||0)+1});const tr=Object.entries(rel).sort((a,b)=>b[1]-a[1]).slice(0,3);const u=X.at(-1);
 return `<div class="card"><small class=c>empresa</small><b>${E(e)}</b>${X.length} decisões · ${pct(X.filter(x=>x.pt=="unanime").length,X.length)}% unânimes · ${X.filter(x=>x.pt=="vista").length} vistas<br><small class=c>Agências: ${[...new Set(X.map(x=>x.a))].join(", ")}<br>Quem mais relatou: ${tr.map(([n,v])=>E(n)+" ("+v+")").join(", ")}<br>Última: ${u?fd(u.dt)+" · "+E(u.as.slice(0,80)):"—"}</small></div>`}).join("")}</div>`;
}
document.querySelectorAll("#ags input").forEach(x=>x.onchange=render);["#emp","#de","#ate"].forEach(s=>$(s).oninput=render);render();
</script></body></html>"""
out = f"{OUT}/index.html"
open(out, "w").write(H.replace("__DATA__", json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))))
print(out, os.path.getsize(out) // 1024, "KB ·", len(DEC), "decisões ·", ", ".join(AGS))
