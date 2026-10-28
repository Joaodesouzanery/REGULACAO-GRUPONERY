import sqlite3; c = sqlite3.connect("data/regulacao.db"); c.executescript(open("pipeline/schema.sql").read()); c.commit()
