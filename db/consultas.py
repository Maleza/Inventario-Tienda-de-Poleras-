from db.conexion import conectar_db


def obtener_o_crear_categoria(nombre):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO categorias(nombre) VALUES(?)", (nombre,))
    conn.commit()

    cursor.execute("SELECT id_categoria FROM categorias WHERE nombre=?", (nombre,))
    id_categoria = cursor.fetchone()[0]

    conn.close()
    return id_categoria


def insertar_modelo(nombre, categoria):
    conn = conectar_db()
    cursor = conn.cursor()

    id_categoria = obtener_o_crear_categoria(categoria)

    cursor.execute("""
    INSERT OR IGNORE INTO modelos(nombre, id_categoria)
    VALUES (?, ?)
    """, (nombre, id_categoria))

    conn.commit()

    cursor.execute("""
    SELECT id_modelo FROM modelos WHERE nombre=? AND id_categoria=?
    """, (nombre, id_categoria))

    id_modelo = cursor.fetchone()[0]
    conn.close()
    return id_modelo


def insertar_talla(nombre):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO tallas(nombre) VALUES(?)", (nombre,))
    conn.commit()

    cursor.execute("SELECT id_talla FROM tallas WHERE nombre=?", (nombre,))
    id_talla = cursor.fetchone()[0]

    conn.close()
    return id_talla


def insertar_inventario(modelo_id, talla_id, ubicacion, cantidad):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO inventario (id_modelo, id_talla, ubicacion, cantidad)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(id_modelo, id_talla, ubicacion)
    DO UPDATE SET cantidad = cantidad + excluded.cantidad
    """, (modelo_id, talla_id, ubicacion, cantidad))

    conn.commit()
    conn.close()

def actualizar_cantidad_inventario(modelo_id, talla_id, ubicacion, cantidad):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO inventario (id_modelo, id_talla, ubicacion, cantidad)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(id_modelo, id_talla, ubicacion)
    DO UPDATE SET cantidad = excluded.cantidad
    """, (modelo_id, talla_id, ubicacion, max(0, int(cantidad))))

    conn.commit()
    conn.close()


def obtener_inventario(categoria=None):
    conn = conectar_db()
    cursor = conn.cursor()

    query = """
    SELECT m.nombre, c.nombre, t.nombre, i.ubicacion, i.cantidad
    FROM inventario i
    JOIN modelos m ON i.id_modelo = m.id_modelo
    JOIN categorias c ON m.id_categoria = c.id_categoria
    JOIN tallas t ON i.id_talla = t.id_talla
    """

    if categoria:
        query += " WHERE c.nombre = ?"
        cursor.execute(query, (categoria,))
    else:
        cursor.execute(query)

    datos = cursor.fetchall()
    conn.close()
    return datos


def eliminar_modelo(nombre):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM modelos WHERE nombre=?", (nombre,))
    conn.commit()
    conn.close()

    