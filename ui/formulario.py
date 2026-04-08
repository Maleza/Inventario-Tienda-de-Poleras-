import tkinter as tk
from tkinter import ttk
from servicios import inventario_servicios
from ui import state, resumen, app



# ===============================
# 🔹 FORMULARIO SUPERIOR (AGREGAR)
# ===============================
def crear_formulario_superior(frame, actualizar_todo):

    frame.config(padx=10, pady=10)

    nombre_var = tk.StringVar()
    categoria_var = tk.StringVar(value="Musica")
    ubicacion_var = tk.StringVar(value="local")
    cantidad_var = tk.IntVar(value=1)
    talla_var = tk.StringVar(value="M")

    # 🔹 Layout ordenado
    tk.Label(frame, text="Nombre").grid(row=0, column=0, padx=5)
    tk.Entry(frame, textvariable=nombre_var, width=25).grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Categoría").grid(row=0, column=2, padx=5)
    ttk.Combobox(frame, textvariable=categoria_var,
                 values=["Musica", "Animacion"],
                 state="readonly",
                 width=12).grid(row=0, column=3, padx=5)

    tk.Label(frame, text="Talla").grid(row=0, column=4, padx=5)
    ttk.Combobox(frame, textvariable=talla_var,
                 values=["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"],
                 state="readonly",
                 width=6).grid(row=0, column=5, padx=5)

    tk.Label(frame, text="Ubicación").grid(row=0, column=6, padx=5)
    ttk.Combobox(frame, textvariable=ubicacion_var,
                 values=["local", "bodega"],
                 state="readonly",
                 width=10).grid(row=0, column=7, padx=5)

    tk.Label(frame, text="Cantidad").grid(row=0, column=8, padx=5)
    tk.Entry(frame, textvariable=cantidad_var, width=5).grid(row=0, column=9, padx=5)

    def agregar():
        if not nombre_var.get() or cantidad_var.get() <= 0:
            return

        inventario_servicios.agregar_stock(
            nombre_var.get(),
            categoria_var.get(),
            talla_var.get(),
            ubicacion_var.get(),
            cantidad_var.get()
        )

        nombre_var.set("")
        cantidad_var.set(1)
        actualizar_todo()

    ttk.Button(frame, text="Agregar Polera",
               command=agregar).grid(row=0, column=10, padx=10)


# ===============================
# 🔹 CONTROLES INFERIORES (+ / -)
# ===============================
def crear_controles(frame, actualizar_todo):

    frame.config(padx=10, pady=10)

    cantidad = tk.IntVar(value=1)
    ubicacion_var = tk.StringVar(value="local")
    busqueda_var = tk.StringVar()

    fila = tk.Frame(frame)
    fila.pack(fill="x")

    # 🔹 BUSCADOR
    tk.Label(fila, text="Buscar:").pack(side="left", padx=5)

    entrada_busqueda = tk.Entry(fila, textvariable=busqueda_var, width=20)
    entrada_busqueda.pack(side="left", padx=5)

    
    ttk.Button(
        fila,
        text="X",
        command=lambda: busqueda_var.set(""),
        width=3
    ).pack(side="left", padx=2)

    def filtrar(*args):
        state.busqueda_modelo = busqueda_var.get()
        actualizar_todo()

    busqueda_var.trace_add("write", filtrar)

    # 🔹 SELECCIÓN
    label = tk.Label(fila, text="Selecciona celda",
                     font=("Arial", 10, "bold"))
    label.pack(side="left", padx=10)

    # 🔹 UBICACIÓN
    ttk.Combobox(fila,
                 textvariable=ubicacion_var,
                 values=["local", "bodega"],
                 state="readonly",
                 width=10).pack(side="left", padx=5)

    # 🔹 CONTROL STOCK
    def cambiar_stock(valor):
        if not state.modelo_seleccionado:
            return

        inventario_servicios.agregar_stock(
            state.modelo_seleccionado,
            state.categoria_actual,
            state.talla_seleccionada,
            ubicacion_var.get(),
            valor
        )

        actualizar_todo()

    ttk.Button(fila, text="-",
               command=lambda: cambiar_stock(-cantidad.get()),
               width=4).pack(side="left", padx=5)

    ttk.Entry(fila, textvariable=cantidad,
              width=5).pack(side="left", padx=5)

    ttk.Button(fila, text="+",
               command=lambda: cambiar_stock(cantidad.get()),
               width=4).pack(side="left", padx=5)

    # 🔹 ELIMINAR
    def eliminar():
        if state.modelo_seleccionado:
            inventario_servicios.eliminar_modelo(state.modelo_seleccionado)
            actualizar_todo()

    ttk.Button(fila, text="Eliminar",
               command=eliminar).pack(side="right", padx=10)

    # 🔹 LABEL DINÁMICO
    def actualizar_label():
        if state.modelo_seleccionado:
            label.config(
                text=f"{state.modelo_seleccionado} - {state.talla_seleccionada}"
            )
        frame.after(300, actualizar_label)

    actualizar_label()