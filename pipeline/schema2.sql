DROP TABLE IF EXISTS votos; DROP TABLE IF EXISTS item_temas; DROP TABLE IF EXISTS itens; DROP TABLE IF EXISTS presenca; DROP TABLE IF EXISTS reunioes;
DROP TABLE IF EXISTS busca;
CREATE TABLE reunioes(id INTEGER PRIMARY KEY, video_id TEXT UNIQUE, numero TEXT, data TEXT, presidente TEXT, formato TEXT, observacoes TEXT);
CREATE TABLE presenca(reuniao_id INT REFERENCES reunioes(id), diretor TEXT, presente INT);
CREATE TABLE itens(id INTEGER PRIMARY KEY, reuniao_id INT REFERENCES reunioes(id), item TEXT, ts TEXT, processo TEXT, interessado TEXT, assunto TEXT,
  relator TEXT, relator_texto TEXT, revisor TEXT, resultado TEXT, unanime INT, resumo TEXT);
CREATE TABLE item_temas(item_id INT REFERENCES itens(id), tema TEXT);
CREATE TABLE votos(id INTEGER PRIMARY KEY, item_id INT REFERENCES itens(id), diretor TEXT, voto TEXT, categoria TEXT, ts TEXT,
  justificativa TEXT, tom TEXT, confianca TEXT, eh_relator INT);
CREATE VIRTUAL TABLE busca USING fts5(item_id UNINDEXED, texto);
