from db import consultas


def agregar_stock(modelo, categoria, talla, ubicacion, cantidad):
    if cantidad == 0:
        return

    modelo_id = consultas.insertar_modelo(modelo, categoria)
    talla_id = consultas.insertar_talla(talla)

    consultas.insertar_inventario(modelo_id, talla_id, ubicacion, cantidad)


def obtener_stock(categoria=None):
    datos = consultas.obtener_inventario(categoria)

    resultado = {}

    for modelo, cat, talla, ubicacion, cantidad in datos:
        key = (modelo, talla)

        if key not in resultado:
            resultado[key] = {"local": 0, "bodega": 0}

        resultado[key][ubicacion] = cantidad

    return resultado
#funcion para mostrar el dashboard en el footer
def obtener_resumen(categoria=None):

    datos = consultas.obtener_inventario(categoria)

    resumen = {}

    for modelo, cat, talla, ubicacion, cantidad in datos:

        if talla not in resumen:
            resumen[talla] = {"local": 0, "bodega": 0}

        resumen[talla][ubicacion] += cantidad

    return resumen


def eliminar_modelo(nombre):
    consultas.eliminar_modelo(nombre)