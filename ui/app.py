import tkinter as tk
from tkinter import ttk
from ui import tabla, formulario


def iniciar_app():
    root = tk.Tk()
    root.title("Inventario Poleras")
    root.geometry("1000x600")

    style = ttk.Style()
    style.theme_use("clam")

    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # 🔹 TOP → formulario horizontal
    frame_top = tk.LabelFrame(contenedor, text="Agregar Polera")
    frame_top.pack(fill="x", pady=5)

    # 🔹 CENTRO → tabla
    frame_tabla = tk.LabelFrame(contenedor, text="Inventario")
    frame_tabla.pack(fill="both", expand=True, pady=5)

    # 🔹 BOTTOM → controles
    frame_bottom = tk.LabelFrame(contenedor, text="Control de Stock")
    frame_bottom.pack(fill="x", pady=5)

    cargar_tabla = tabla.crear_tabla(frame_tabla)

    formulario.crear_formulario_superior(frame_top, cargar_tabla)
    formulario.crear_controles(frame_bottom, cargar_tabla)

    cargar_tabla()

    root.mainloop()
    