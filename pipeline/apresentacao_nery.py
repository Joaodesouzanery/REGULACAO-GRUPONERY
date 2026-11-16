"""Apresentação institucional do Grupo Nery (comercial), no padrão visual dos relatórios, com densidade de whitepaper.
Não cita ferramenta, repositório nem método de coleta. Uso: python3 pipeline/apresentacao_nery.py [--one-pager]
Saída: proposta2/comercial/apresentacao_grupo_nery.pdf (ou one_pager_grupo_nery.pdf)."""
import sys, os, re, json, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design as d, previsao
E = d.E
K = {s: d.kit(s) for s in ["portos", "rodovias", "mineracao", "energia", "petroleo_gas", "agua", "ferrovias"]}
CONTATO = "Grupo Nery · inteligência regulatória"


def so_nery(h):
    """tira a marca do parceiro: material do Grupo Nery."""
    h = re.sub(r'<img src="[^"]+" class="lgc"><span class="sep"></span><span class="parc">em parceria com</span>', "", h)
    return re.sub(r'<div class="tpe">.*?</div>', "", h, flags=re.S).replace('class="hcp"', 'class="hcp" style="display:none"')


# números da base (agregados, públicos)
tot = {}
for ag in ("antt", "anm", "antaq", "aneel"):
    try: tot[ag] = previsao.conn(ag).execute("select count(*) from itens i join reunioes r on r.id=i.reuniao_id where r.data>='2018-01-01'").fetchone()[0]
    except Exception: tot[ag] = 0
dec = sum(tot.values())
MA = json.load(open("data/mandatos_agencias.json"))["agencias"]
vagas = sum(1 for ps in MA.values() for p in ps if p["tipo"] == "vaga")
T = lambda s, t, c: d.tecnica(s, t, c, "nery").replace(">NERY ·", ">Grupo Nery ·")
d.NOME_AG["nery"] = "Grupo Nery"

S = []
S.append(d.capa(K["portos"]["capa"], "50% 55%", "Inteligência regulatória", "Grupo Nery", "Como as agências reguladoras decidem, antes de decidirem sobre você",
                "Diretorias de agências reguladoras federais acompanhadas voto a voto, com a fala e o minuto exato de cada sessão.",
                [(f"{dec:,}".replace(",", "."), "decisões de diretoria mapeadas desde 2018"), ("12", "agências federais acompanhadas"), (vagas, "cadeiras sem titular hoje, monitoradas"), ("4", "documentos por mês para cada cliente")]))
SEC = [("O problema", "decisões de milhões, cinco votos"), ("O que fazemos", "monitorar, analisar, antecipar"), ("Serviços", "o que entregamos e para quem"), ("Agências", "onde atuamos e o que vem"), ("Valor", "exemplos de economia e eficiência"), ("Como trabalhar conosco", "formatos, prévia e contato")]
S.append(d.sumario(SEC, K["energia"]["divisores"][0]))

# 01 problema
S.append(d.divisor(1, SEC[0][0], "Contratos, tarifas, outorgas e concessões passam por diretorias colegiadas de cinco pessoas. Quem chega à reunião sem saber como cada uma decide, decide no escuro.", K["rodovias"]["divisores"][0]))
S.append(T("01 · O problema", "Por que a decisão regulatória ainda é surpresa", d.whitepaper("Contexto", [
    ("Decisões de alto valor, pouca previsibilidade", "<p>Reequilíbrios, revisões tarifárias, prorrogações, autorizações e sanções somam bilhões por ano e são decididos por colegiados pequenos. Um pedido de vista ou uma retirada de pauta pode adiar uma decisão por meses, com custo financeiro direto para a empresa.</p>"),
    ("Informação pública, mas espalhada", "<p>As sessões são públicas, mas o histórico de como cada diretor vota, com quais argumentos, em quanto tempo e com que divergências não está organizado em lugar nenhum. Pesquisar precedentes consome dezenas de horas por caso.</p>"),
    ("Diretorias em constante mudança", f"<p>Hoje há <b>{vagas} cadeiras sem titular</b> nas 12 agências federais, ocupadas por substitutos. Cada troca muda a composição que vai julgar os processos, e quase ninguém acompanha isso de forma sistemática.</p>"),
    ("O resultado", "<p>Empresas e escritórios chegam às reuniões com pareceres jurídicos sólidos, mas sem saber como aquela diretoria específica costuma decidir aquele tema.</p>")],
    foto=K["portos"]["divisores"][1], h_foto="auto")))

# 02 o que fazemos
S.append(d.divisor(2, SEC[1][0], "Organizamos como cada diretoria decide: quem vota o quê, com quais argumentos, em quanto tempo, e o que deve vir a seguir.", K["mineracao"]["divisores"][0]))
S.append(T("02 · O que fazemos", "Monitorar, analisar, antecipar", d.lista_tripla([
    ("Monitorar", ["Agenda e pautas das diretorias", "Resultado de cada reunião", "Mandatos, vagas e substitutos", "Processos do cliente, sessão a sessão"]),
    ("Analisar", ["Voto de cada diretor, tema por tema", "Argumentos e falas, com o minuto exato", "Prazo de decisão por tipo de processo", "Casos semelhantes e mudanças de entendimento"]),
    ("Antecipar", ["Alerta antes de cada reunião", "Estimativa de placar, sempre identificada como estimativa", "Prazo provável do processo", "Riscos e próximos passos"])])
    + '<div style="height:.2in"></div>' + d.whitepaper("Princípios", [
        ("Prova em cada afirmação", "<p>Toda conclusão traz a reunião, o item, o trecho literal e o link do vídeo oficial no minuto exato. O cliente clica e confere.</p>"),
        ("Estimativa é estimativa", "<p>Previsões vêm com o tamanho da amostra e o teste no passado. Nunca vendemos certeza.</p>"),
        ("Só fontes públicas, dados do cliente protegidos", "<p>Usamos informação pública da agência. O que o cliente nos informa fica sob confidencialidade e LGPD.</p>")], foto=K["rodovias"]["capa"], h_foto="auto")))

# 03 serviços
S.append(d.divisor(3, SEC[2][0], "Do pacote mensal à consulta avulsa: para empresas reguladas, escritórios, investidores e associações.", K["energia"]["divisores"][1] if len(K["energia"]["divisores"]) > 1 else K["energia"]["capa"]))
srv = [("Pacote mensal da empresa", "Relatório da empresa, boletim mensal com alerta pré-pauta e respostas às perguntas do mês, raio-X dos processos, agenda e inteligência comparativa, e o monitoramento em 8 blocos."),
       ("Alerta pré-pauta", "Antes de cada reunião: os itens que interessam à empresa, quem relata, como esse relator decidiu casos parecidos e a estimativa de placar."),
       ("Perfil de diretoria", "Como cada diretor vota num tema, com os argumentos recorrentes e as falas no minuto. Base para sustentação oral e reuniões com diretores."),
       ("Due diligence regulatória", "Para fundos, bancos e compradores: histórico da diretoria sobre um ativo, desfechos, prazos, precedentes e mandatos que vencem."),
       ("Precedentes e casos semelhantes", "Decisões parecidas com o voto de cada diretor e a justificativa, prontas para petições, recursos e memoriais.")]
srv2 = [("Mandatos e vacância", "Quem sai, quando, quem substitui e o efeito provável no colegiado, nas 12 agências federais."),
        ("Relatório setorial", "Como a agência decide os grandes temas do setor, trimestralmente. Ideal para associações e seus associados."),
        ("Preparação de sustentação oral", "Os argumentos que convenceram cada diretor em casos parecidos e as objeções já registradas."),
        ("Consulta avulsa", "Uma pergunta, uma resposta com evidência: «como a diretoria tratou X?», «quem relata Y?»."),
        ("Comparativo entre agências", "Tempo de decisão, vacância, transparência e previsibilidade lado a lado, para grupos com ativos em vários setores.")]
S.append(T("03 · Serviços", "O que entregamos", d.whitepaper("Para a empresa", srv, foto=K["energia"]["capa"], h_foto="auto")))
S.append(T("03 · Serviços", "Mais serviços e para quem", d.whitepaper("Sob medida", srv2) + '<div style="height:.15in"></div>' + d.lista_tripla([
    ("Empresas reguladas", ["Concessionárias e arrendatários", "Distribuidoras, geradoras, transmissoras", "Mineradoras, petroleiras, aéreas"]),
    ("Escritórios e consultorias", ["Direito regulatório e de infraestrutura", "Relações governamentais", "Consultorias econômicas"]),
    ("Investidores e associações", ["Fundos de infraestrutura e bancos", "Compradores em M&A", "Associações setoriais"])]) + '<div class="wf" style="background-image:url(' + d.b64(K["portos"]["capa"]) + ');background-position:50% 50%"></div>'))

# 04 agências
S.append(d.divisor(4, SEC[3][0], "Começamos por transportes, portos, mineração e energia. As demais agências federais entram em sequência.", K["petroleo_gas"]["capa"]))
ops = [("ANTT", "Transportes terrestres", "em operação"), ("ANTAQ", "Portos e navegação", "em operação"), ("ANM", "Mineração", "em operação"), ("ANEEL", "Energia elétrica", "em operação (base em expansão)"),
       ("ANP", "Petróleo, gás e biocombustíveis", "próxima"), ("ANA", "Águas e saneamento", "em breve"), ("ANAC", "Aviação civil", "em breve"), ("ANATEL", "Telecomunicações", "em breve"),
       ("ANVISA", "Vigilância sanitária", "em breve"), ("ANS", "Saúde suplementar", "em breve"), ("ANCINE", "Cinema e audiovisual", "em breve"), ("ANPD", "Proteção de dados", "em breve")]
rows = []
for a, s_, st in ops:
    ps = MA.get(a, []); vg = sum(1 for p in ps if p["tipo"] == "vaga")
    rows.append([f"<b>{a}</b>", E(s_), E(st), str(sum(1 for p in ps if p["tipo"] == "titular")), str(vg)])
S.append(T("04 · Agências", "Doze agências federais, uma mesma leitura", d.tabela(["Agência", "Setor", "Situação", "Titulares hoje", "Cadeiras vagas"], rows, ["12%", "34%", "26%", "14%", "14%"])
           + '<p style="font-size:8pt;color:#6B7780;margin-top:.1in">Composição das diretorias acompanhada para todas as agências, com o ato de nomeação no Diário Oficial; análise de votos completa nas agências em operação.</p>'))

# 05 valor
S.append(d.divisor(5, SEC[4][0], "O valor aparece em meses ganhos, horas poupadas e riscos precificados. Exemplos ilustrativos, com a premissa explícita.", K["agua"]["capa"]))
ex = [("Arrendatário portuário com reequilíbrio", "<p>Chega à reunião sabendo que dois diretores divergiram antes em metodologia de cálculo e quais argumentos os convenceram. Evita um pedido de vista. <i>Premissa: cada mês de atraso num reequilíbrio de R$ 50 milhões custa cerca de R$ 500 mil em custo de capital.</i></p>"),
      ("Distribuidora em revisão tarifária", "<p>Ajusta o pleito com as objeções registradas de cada diretor nas últimas revisões, em vez de recorrer depois. <i>Premissa: um recurso administrativo leva de 3 a 6 meses.</i></p>"),
      ("Escritório preparando um recurso", "<p>Recebe os precedentes com o voto de cada diretor e o minuto da fala. <i>Premissa: 15 a 25 horas de pesquisa poupadas por caso.</i></p>"),
      ("Fundo avaliando uma concessão", "<p>Precifica o risco regulatório com o histórico da diretoria sobre o ativo, os prazos médios e os mandatos que vencem. <i>Premissa: 1 ponto na taxa de desconto muda dezenas de milhões no valor.</i></p>"),
      ("Mineradora com outorga parada", "<p>Compara o prazo do seu processo com mais de 20 semelhantes e sabe quando escalar. <i>Premissa: cada mês de atraso adia receita da expansão.</i></p>")]
S.append(T("05 · Valor", "Como isso se paga", d.whitepaper("Exemplos", ex, foto=K["mineracao"]["capa"], h_foto="auto")))

# 06 como trabalhar
S.append(T("06 · Como trabalhar conosco", "Do primeiro contato ao pacote mensal", d.whitepaper("Começo", [
    ("Prévia gratuita", "<p>Uma prévia de 4 páginas sobre a sua empresa, feita só com informação pública: as decisões mais recentes, o desfecho para a empresa, quem decide e uma amostra do perfil de um diretor.</p>"),
    ("Piloto de 3 meses", "<p>Escolhemos os processos e temas a monitorar. Todo mês, os documentos com alerta antes de cada reunião e respostas às perguntas da equipe.</p>"),
    ("Formatos", "<p>Pacote mensal, consulta avulsa, relatório setorial ou due diligence. Atendimento direto ou por meio de parceiros.</p>"),
    ("Confidencialidade", "<p>Os dados que a empresa informa ficam sob termo de confidencialidade e LGPD e não entram em nenhum material de terceiros.</p>")],
    foto=K["ferrovias"]["capa"], h_foto="auto")))
S.append(d.fim("Fontes públicas das agências reguladoras. Estimativas são sempre identificadas como estimativas e não substituem orientação jurídica.", CONTATO, K["portos"]["divisores"][0]))

out = "proposta2/comercial/apresentacao_grupo_nery"
if "--one-pager" in sys.argv:
    S = [S[0], S[4], S[11]]; out = "proposta2/comercial/one_pager_grupo_nery"
S = [so_nery(x) for x in S]
os.makedirs("proposta2/comercial", exist_ok=True)
print(d.documento(S, "Grupo Nery · Inteligência regulatória", out), len(S), "páginas")
