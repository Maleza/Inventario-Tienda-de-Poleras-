import sqlite3

DB_NAME = "inventario.db"

def conectar_db():
    return sqlite3.connect(DB_NAME)


def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS modelos (
        id_modelo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        id_categoria INTEGER,
        UNIQUE(nombre, id_categoria)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tallas (
        id_talla INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id_inventario INTEGER PRIMARY KEY AUTOINCREMENT,
        id_modelo INTEGER,
        id_talla INTEGER,
        ubicacion TEXT,
        cantidad INTEGER,
        UNIQUE(id_modelo, id_talla, ubicacion)
    )
    """)

    conn.commit()
    conn.close()
    