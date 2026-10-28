CREATE TABLE IF NOT EXISTS videos(id TEXT PRIMARY KEY, agencia TEXT, titulo TEXT, data TEXT, duracao INT, url TEXT);
CREATE TABLE IF NOT EXISTS diretores(id INTEGER PRIMARY KEY, agencia TEXT, nome TEXT, UNIQUE(agencia,nome));
CREATE TABLE IF NOT EXISTS itens_pauta(id INTEGER PRIMARY KEY, video_id TEXT REFERENCES videos(id), ts_ini REAL, ts_fim REAL,
  processo TEXT, tema TEXT, resumo TEXT, relator_id INT REFERENCES diretores(id), resultado TEXT);
CREATE TABLE IF NOT EXISTS falas(id INTEGER PRIMARY KEY, item_id INT REFERENCES itens_pauta(id), diretor_id INT REFERENCES diretores(id),
  ts_ini REAL, ts_fim REAL, texto TEXT, posicao TEXT, voto TEXT, argumentos TEXT, tom TEXT, confianca REAL);
CREATE VIRTUAL TABLE IF NOT EXISTS falas_fts USING fts5(texto, content='falas', content_rowid='id');
