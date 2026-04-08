import tkinter as tk
from tkinter import ttk
from ui import tabla, formulario, resumen


def iniciar_app():
    root = tk.Tk()
    root.title("Inventario Poleras")
    root.geometry("1000x600")

    style = ttk.Style()
    style.theme_use("clam")

    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # 🔹 TOP
    frame_top = tk.LabelFrame(contenedor, text="Agregar Polera")
    frame_top.pack(fill="x", pady=5)

    # 🔹 TABLA
    frame_tabla = tk.LabelFrame(contenedor, text="Inventario")
    frame_tabla.pack(fill="both", expand=True, pady=5)

    # 🔹 CONTROLES
    frame_bottom = tk.LabelFrame(contenedor, text="Control de Stock")
    frame_bottom.pack(fill="x", pady=5)

    # 🔹 RESUMEN
    frame_resumen = tk.LabelFrame(contenedor, text="Resumen")
    frame_resumen.pack(fill="x", pady=5)

    
    cargar_tabla = tabla.crear_tabla(frame_tabla)
    cargar_resumen = resumen.crear_resumen(frame_resumen)

    #FUNCION CENTRAL PARA ACTUALIZAR LOS ELEMENTOS
    def actualizar_todo():
        cargar_tabla()
        cargar_resumen()

    # CONECTAR UI
    formulario.crear_formulario_superior(frame_top, actualizar_todo)
    formulario.crear_controles(frame_bottom, actualizar_todo)

    # CARGA INICIAL
    actualizar_todo()

    root.mainloop()