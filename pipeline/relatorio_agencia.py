"""Relatório de apresentação de uma agência (PDF Grupo Nery), montado da base. Uso: python3 pipeline/relatorio_agencia.py antt|anm
Gera agencias/<ag>/apresentacao/{perguntas.md, respostas/, relatorio.pdf} reaproveitando pipeline/relatorio.py
(cada seção vira uma «pergunta»; os perfis de diretor usam [diretor: X] e ganham números, gráfico e evidências)."""
import sqlite3, json, os, re, sys, subprocess, collections, shutil
AG = sys.argv[1]; ROOT = "" if AG == "antt" else f"data/{AG}/"
c = sqlite3.connect(f"{ROOT or 'data/'}regulacao.db" if AG == "antt" else f"data/{AG}/regulacao.db"); c.row_factory = sqlite3.Row
OUT = f"agencias/{AG}/apresentacao"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(f"{OUT}/respostas")
NOME = {"antt": "ANTT — Agência Nacional de Transportes Terrestres", "anm": "ANM — Agência Nacional de Mineração"}[AG]
SETOR = {"antt": "rodovias", "anm": "mineracao"}[AG]
q1 = lambda sql, *a: c.execute(sql, a).fetchone()[0]
secoes = []
def secao(titulo, md, tags=""): secoes.append((titulo, tags, md))
# 1. o que temos
n_r, n_i, n_v = q1("select count(*) from reunioes"), q1("select count(*) from itens"), q1("select count(*) from votos")
d0, d1 = q1("select min(data) from reunioes where data like '2%'"), q1("select max(data) from reunioes")
ev = q1("select count(*) from eventos"); fa = q1("select count(*) from falas_diretores where fonte='estruturada'")
por_ano = c.execute("select substr(data,1,4) a, count(*) n, (select count(*) from itens i where i.reuniao_id in (select id from reunioes r2 where substr(r2.data,1,4)=substr(r.data,1,4))) it from reunioes r where data like '2%' group by 1 order by 1").fetchall()
cob = open(f"agencias/{AG}/COBERTURA.md").read() if os.path.exists(f"agencias/{AG}/COBERTURA.md") else ""
sem = re.search(r"Total: \*\*(\d+)\*\*", open(f"agencias/{AG}/sem_transcricao.md").read()) if os.path.exists(f"agencias/{AG}/sem_transcricao.md") else None
md = [f"**1. Resposta curta:** a base cobre **{n_r} reuniões de diretoria** ({d0[:7]} a {d1[:7]}), **{f"{n_i:,}".replace(",", ".")} itens** deliberados e **{f"{n_v:,}".replace(",", ".")} votos** de diretores, mais **{ev} eventos** públicos (audiências, participativas) com {fa} falas de diretores estruturadas.", "",
      "| Ano | Reuniões | Itens |", "|---|---|---|"] + [f"| {r['a']} | {r['n']} | {r['it']} |" for r in por_ano] + ["",
      f"- Fonte: todas as transmissões públicas no canal oficial da agência no YouTube (inventário do canal inteiro, todas as abas e playlists).",
      f"- Vídeos sem texto utilizável (sem legenda ou ininteligível): {sem.group(1) if sem else 'ver sem_transcricao.md'} — candidatos a transcrição de áudio (Whisper)."]
if AG == "anm": md.append("- 12 reuniões sem vídeo publicado foram incorporadas a partir das atas oficiais (sem trecho literal nem minuto).")
md.append("- Fora do alcance do YouTube: voto escrito completo (SEI), itens sigilosos, deliberações em circuito/fora de sessão e período anterior ao início das transmissões.")
secao("O que temos: cobertura da base", "\n".join(md))
# 2. qualidade
qr = open(f"agencias/{AG}/qualidade/README.md").read() if os.path.exists(f"agencias/{AG}/qualidade/README.md") else ""
linhas = [l for l in qr.splitlines() if l.startswith("|") or l.startswith("**") or l.startswith("- ")]
secao("Qualidade: quanto confiar", "**1. Resposta curta:** cada análise foi conferida por releitura cega de amostras (outro leitor, sem ver a análise) e, na ANM, cruzada com as atas oficiais. Os números medem consistência, não verdade absoluta: a fonte é a legenda automática.\n\n" + "\n".join(linhas[:30]))
# 3. diretoria e mandatos
mand = json.load(open("data/mandatos.json" if AG == "antt" else f"data/{AG}/mandatos.json"))
res = {r["diretor"]: r for r in c.execute("select v.diretor, count(*) n, sum(eh_relator) rel, sum(categoria in ('acompanha','revisor_acompanha')) ac, sum(categoria in ('vencido','revisor_diverge')) dv, sum(categoria='vista') vi, min(r.data) a, max(r.data) b from votos v join itens i on i.id=v.item_id join reunioes r on r.id=i.reuniao_id group by 1")}
md = ["**1. Resposta curta:** quem votou no período, quanto relatou, quanto acompanha o relator quando não relata e quantas vezes ficou fora do padrão (vista, voto-vista divergente, vencido).", "",
      "| Diretor | Período nos votos | Votos | Relatorias | Acompanha | Vistas | Diverge/vencido |", "|---|---|---|---|---|---|---|"]
for d, r in sorted(res.items(), key=lambda x: -x[1]["n"]):
    md.append(f"| {d} | {r['a'][:7]} a {r['b'][:7]} | {r['n']} | {r['rel']} | {round(100*r['ac']/max(r['n']-r['rel'],1))}% | {r['vi']} | {r['dv']} |")
vac = open(f"agencias/{AG}/mandatos/README.md").read() if os.path.exists(f"agencias/{AG}/mandatos/README.md") else ""
md += ["", "**Vacância de cadeiras:**"] + [l for l in vac.splitlines() if l.startswith("- ")][:4]
secao("Diretoria: quem decide", "\n".join(md))
# 4. perfis dos principais diretores (ativos ou com mais votos)
top = [d for d, r in sorted(res.items(), key=lambda x: (-(x[1]["b"] >= "2025"), -x[1]["n"]))][:6]
for d in top:
    f = subprocess.run(["python3", "pipeline/consulta.py", "ficha", d], capture_output=True, text=True, cwd="." if AG == "antt" else f"data/{AG}/.raiz").stdout
    secao(f"Perfil: {d}", re.sub(r"\s*\[Completar[^\]]*\]", "", f), f"[agencia: {AG}] [diretor: {d}]")
# 5. temas e microtemas
tm = c.execute("select tema, count(distinct item_id) n from item_temas group by 1 order by 2 desc").fetchall()
mt = c.execute("select microtema, tema, count(distinct item_id) n from item_microtema group by 1 order by 3 desc limit 15").fetchall()
cobm = q1("select count(distinct item_id) from item_microtema")
md = [f"**1. Resposta curta:** os itens são classificados em {len(tm)} temas e, num recorte mais fino, em microtemas ({cobm} de {n_i} itens, {round(100*cobm/n_i)}%, com ao menos um microtema).", "",
      "| Tema | Itens |", "|---|---|"] + [f"| {r['tema']} | {r['n']} |" for r in tm[:12]] + ["", "| Microtema | Tema | Itens |", "|---|---|---|"] + [f"| {r['microtema']} | {r['tema']} | {r['n']} |" for r in mt]
secao("Temas e microtemas", "\n".join(md))
# 6. empresas
ne = q1("select count(*) from entidades"); cobe = q1("select count(distinct item_id) from item_entidade")
emp = c.execute("select e.nome, e.tipo, coalesce(e.grupo,'') g, count(*) n from item_entidade ie join entidades e on e.id=ie.entidade where e.tipo not like 'orgao%' group by e.id order by n desc limit 15").fetchall()
grp = c.execute("select e.grupo, count(distinct e.id) ne, count(*) n from item_entidade ie join entidades e on e.id=ie.entidade where e.grupo is not null group by 1 order by n desc limit 10").fetchall()
md = [f"**1. Resposta curta:** os interessados foram normalizados em **{ne} entidades** (empresas, pessoas, órgãos), cobrindo {round(100*cobe/n_i)}% dos itens; as variações de grafia da legenda foram agrupadas e cada entidade tem tipo, setor e, quando conhecido, grupo econômico.", "",
      "| Empresa | Tipo | Grupo | Itens |", "|---|---|---|---|"] + [f"| {r['nome']} | {r['tipo']} | {r['g']} | {r['n']} |" for r in emp] + ["", "| Grupo econômico | Empresas | Itens |", "|---|---|---|"] + [f"| {r['grupo']} | {r['ne']} | {r['n']} |" for r in grp]
secao("Empresas e grupos econômicos", "\n".join(md))
# 7. as 10 funcionalidades
ex_emp = emp[0]["nome"] if emp else ""
def cmd(*a):
    return subprocess.run(["python3", "pipeline/consulta.py", *a], capture_output=True, text=True, cwd="." if AG == "antt" else f"data/{AG}/.raiz").stdout
F = [("Histórico de uma empresa", f"empresa «{ex_emp}»", "\n".join(cmd("empresa", ex_emp.split()[0]).splitlines()[2:5])),
     ("Empresa × diretor", "votos de cada diretor nos processos da empresa", "\n".join([l for l in cmd("empresa", ex_emp.split()[0]).splitlines() if l.startswith("- ") and "votos ·" in l][:4])),
     ("Relator mais provável", f"para «{ex_emp.split()[0]}»", "\n".join(cmd("relator", ex_emp.split()[0]).splitlines()[2:5])),
     ("Microtema × diretor", f"«{mt[0]['microtema']}»", "\n".join(cmd("microtema", mt[0]["microtema"]).splitlines()[2:7])),
     ("Precedentes", "casos mais parecidos com um texto livre", "\n".join(cmd("precedentes", mt[1]["microtema"].replace("_", " ")).splitlines()[2:4])),
     ("Reincidência", "empresas com mais processos sancionadores", "\n".join(cmd("reincidencia").splitlines()[2:6])),
     ("Grupo econômico", f"«{grp[0]['grupo'] if grp else '-'}»", "\n".join(cmd("grupo", grp[0]["grupo"]).splitlines()[2:5]) if grp else ""),
     ("Sustentação oral", "efeito de a empresa falar na sessão", "\n".join(cmd("sustentacoes").splitlines()[2:4])),
     ("Tramitação", "processos que voltam à pauta e quem pede vista", "\n".join(cmd("tramitacao").splitlines()[2:5])),
     ("Monitor por cliente", "aviso semanal do que saiu para as empresas, temas e relatores de cada cliente", "Configurado em data/monitor.json; roda na tarefa semanal (pipeline/monitor.py).")]
md = ["**1. Resposta curta:** dez consultas prontas sobre a base, cada uma com evidência (reunião, item, voto, link no minuto). Exemplos reais abaixo."]
for i, (t, sub, ex) in enumerate(F, 1):
    md += ["", f"**{i}. {t}** — {sub}", ex]
secao("O que dá para perguntar: as 10 funcionalidades", "\n".join(md))
# 8. limites
secao("Limites e próximos passos", "\n".join(["**1. Resposta curta:** o que a base não diz, para não ser usado como se dissesse.", "",
    "- A legenda automática erra nomes, números de processo e valores; os erros mais comuns ficam marcados como incertos.",
    "- Quem só acompanha o relator raramente fala: o minuto do link é o do item, aproximado.",
    "- Desfecho «favorável/desfavorável» à empresa é classificação automática pelo texto do resultado; tom e argumentos são inferência registrada, nunca rótulo pessoal.",
    "- Voto escrito completo (SEI), itens sigilosos e decisões fora de sessão pública não estão na base.",
    "- O período de cada diretor nos votos pode passar do mandato: votos dados antes (voto-vista retomado, voto de diretor que saiu) são registrados na reunião em que o item é concluído.",
    "- Mandatos: Senado e DOU por fontes públicas; posses ainda não confirmadas no DOU (download pelo INLABS pendente).",
    "- Próximos passos: transcrição por áudio (Whisper) dos vídeos sem legenda; atas como gabarito contínuo; novas agências."]))
open(f"{OUT}/perguntas.md", "w").write("\n".join(f"- {t} {tags} [setor: {SETOR}]".rstrip() for t, tags, _ in secoes) + "\n")
for i, (_, _, m) in enumerate(secoes, 1): open(f"{OUT}/respostas/{i:02d}.md", "w").write(m + "\n")
r = subprocess.run(["python3", "pipeline/relatorio.py", OUT, "--titulo", f"Base de inteligência regulatória — {AG.upper()}", "--agencia", AG, "--cliente", "apresentação institucional", "--periodo", f"{d0[:4]}–{d1[:4]}"], capture_output=True, text=True)
print(r.stdout.strip() or r.stderr[-800:])
