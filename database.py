import sqlite3
from datetime import datetime

DB_PATH = "data/encomendas.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS encomendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        nome TEXT,
        telefone TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_encomenda(produto, nome, telefone, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO encomendas (produto, nome, telefone, data)
    VALUES (?, ?, ?, ?)
    """, (produto, nome, telefone, data))

    conn.commit()
    conn.close()


def get_encomendas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM encomendas")
    data = c.fetchall()

    conn.close()
    return data


def get_encomendas_por_data(datas):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    query = f"""
    SELECT * FROM encomendas
    WHERE date(data) IN ({','.join(['?']*len(datas))})
    """

    c.execute(query, datas)
    data = c.fetchall()

    conn.close()
    return data