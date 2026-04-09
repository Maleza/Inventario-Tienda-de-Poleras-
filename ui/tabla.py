import tkinter as tk
from servicios import inventario_servicios
from ui import state

TALLAS = ["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"]


def crear_tabla(frame):

    frame.pack_propagate(False)

    # =========================
    # 🔹 ESTRUCTURA PRINCIPAL
    # =========================
    contenedor_principal = tk.Frame(frame)
    contenedor_principal.pack(fill="both", expand=True)

    # HEADER (fijo)
    frame_header = tk.Frame(contenedor_principal)
    frame_header.pack(fill="x")

    # BODY (scroll)
    frame_body = tk.Frame(contenedor_principal)
    frame_body.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_body, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_body, orient="vertical", command=canvas.yview)

    contenedor = tk.Frame(canvas)

    # 🔥 FIX CLAVE: ajustar ancho del canvas
    window_id = canvas.create_window((0, 0), window=contenedor, anchor="nw")

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # scroll dinámico
    contenedor.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # =========================
    # 🔹 FUNCIONES
    # =========================
    def seleccionar(modelo, talla):
        state.modelo_seleccionado = modelo
        state.talla_seleccionada = talla
        cargar_datos()

    def crear_header():
        for w in frame_header.winfo_children():
            w.destroy()

        tk.Label(frame_header, text="Modelo",
                 bg="#1E1E1E", fg="white",
                 font=("Segoe UI", 10, "bold"),
                 padx=5, pady=5)\
            .grid(row=0, column=0, sticky="nsew")

        for i, talla in enumerate(TALLAS):
            tk.Label(frame_header, text=talla,
                     bg="#1E1E1E", fg="white",
                     font=("Segoe UI", 10, "bold"),
                     padx=5, pady=5)\
                .grid(row=0, column=i+1, sticky="nsew")

        # 🔥 MISMA CONFIGURACIÓN QUE LA TABLA
        for col in range(len(TALLAS) + 1):
            frame_header.grid_columnconfigure(col, weight=1, uniform="col")
            contenedor.grid_columnconfigure(col, weight=1, uniform="col")

    def cargar_datos():

        for w in contenedor.winfo_children():
            w.destroy()

        datos = inventario_servicios.obtener_stock(state.categoria_actual)
        filtro = state.busqueda_modelo.lower().strip()

        matriz = {}

        for (modelo, talla), valores in datos.items():

            if filtro and filtro not in modelo.lower():
                continue

            if modelo not in matriz:
                matriz[modelo] = {t: {"local": 0, "bodega": 0} for t in TALLAS}

            matriz[modelo][talla] = valores

        # =========================
        # 🔹 FILAS
        # =========================
        for i, (modelo, tallas) in enumerate(matriz.items()):

            # columna modelo
            tk.Label(
                contenedor,
                text=modelo,
                bg="#f0f0f0",
                padx=5,
                pady=5
            ).grid(row=i, column=0, sticky="nsew")

            for j, talla in enumerate(TALLAS, start=1):

                val = tallas[talla]

                borde = 3 if (
                    modelo == state.modelo_seleccionado and
                    talla == state.talla_seleccionada
                ) else 1

                celda_frame = tk.Frame(
                    contenedor,
                    relief="solid",
                    borderwidth=borde,
                    bg="white"
                )
                celda_frame.grid(row=i, column=j, sticky="nsew")

                # LOCAL
                label_local = tk.Label(
                    celda_frame,
                    text=str(val["local"]),
                    bg="#4CAF50" if val["local"] > 0 else "#EEEEEE",
                    fg="white" if val["local"] > 0 else "black"
                )
                label_local.pack(side="left", fill="both", expand=True)

                # BODEGA
                label_bodega = tk.Label(
                    celda_frame,
                    text=str(val["bodega"]),
                    bg="#F44336" if val["bodega"] > 0 else "#EEEEEE",
                    fg="white" if val["bodega"] > 0 else "black"
                )
                label_bodega.pack(side="left", fill="both", expand=True)

                # eventos
                def bind_event(widget, m=modelo, t=talla, frame_ref=celda_frame):

                    def hover_on(e):
                        frame_ref.config(bg="#dfe6e9")

                    def hover_off(e):
                        frame_ref.config(bg="white")

                    widget.bind("<Button-1>", lambda e: seleccionar(m, t))
                    widget.bind("<Enter>", hover_on)
                    widget.bind("<Leave>", hover_off)

                for w in (celda_frame, label_local, label_bodega):
                    bind_event(w)

    # =========================
    # 🔹 INIT
    # =========================
    crear_header()

    return cargar_datos
