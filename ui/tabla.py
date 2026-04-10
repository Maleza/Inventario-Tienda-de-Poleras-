import tkinter as tk
from servicios import inventario_servicios
from ui import state

TALLAS = ["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"]


def crear_tabla(frame):

    frame.pack_propagate(False)

    # =========================
    # 🔹 ESTRUCTURA
    # =========================
    contenedor_principal = tk.Frame(frame)
    contenedor_principal.pack(fill="both", expand=True)

    frame_header = tk.Frame(contenedor_principal)
    frame_header.pack(fill="x")

    frame_body = tk.Frame(contenedor_principal)
    frame_body.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_body, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_body, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    contenedor = tk.Frame(canvas)
    window_id = canvas.create_window((0, 0), window=contenedor, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    # 🔥 ajustar ancho automático
    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    contenedor.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # scroll SOLO sobre canvas (no global)
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # =========================
    # 🔹 CACHE (CLAVE)
    # =========================
    celdas = {}       # (modelo, talla) → (label_local, label_bodega, frame)
    filas_modelo = {} # modelo → label modelo

    # =========================
    # 🔹 HEADER
    # =========================
    def crear_header():
        tk.Label(frame_header, text="Modelo",
                 bg="#1E1E1E", fg="white",
                 font=("Segoe UI", 10, "bold"),
                 padx=5, pady=5).grid(row=0, column=0, sticky="nsew")

        for i, talla in enumerate(TALLAS):
            tk.Label(frame_header, text=talla,
                     bg="#1E1E1E", fg="white",
                     font=("Segoe UI", 10, "bold"),
                     padx=5, pady=5).grid(row=0, column=i+1, sticky="nsew")

        for col in range(len(TALLAS) + 1):
            frame_header.grid_columnconfigure(col, weight=1, uniform="col")
            contenedor.grid_columnconfigure(col, weight=1, uniform="col")

    # =========================
    # 🔹 SELECCIÓN (SIN RECARGA)
    # =========================
    def actualizar_seleccion():
        for (modelo, talla), (_, _, frame_ref) in celdas.items():
            if modelo == state.modelo_seleccionado and talla == state.talla_seleccionada:
                frame_ref.config(borderwidth=3)
            else:
                frame_ref.config(borderwidth=1)

    def seleccionar(modelo, talla):
        state.modelo_seleccionado = modelo
        state.talla_seleccionada = talla
        actualizar_seleccion()

    # =========================
    # 🔹 CREAR TABLA (SOLO 1 VEZ)
    # =========================
    def construir_tabla(matriz):

        for i, (modelo, tallas) in enumerate(matriz.items()):

            label_modelo = tk.Label(
                contenedor,
                text=modelo,
                bg="#f0f0f0",
                padx=5,
                pady=5
            )
            label_modelo.grid(row=i, column=0, sticky="nsew")
            filas_modelo[modelo] = label_modelo

            for j, talla in enumerate(TALLAS, start=1):

                celda_frame = tk.Frame(
                    contenedor,
                    relief="solid",
                    borderwidth=1,
                    bg="white"
                )
                celda_frame.grid(row=i, column=j, sticky="nsew")

                label_local = tk.Label(celda_frame)
                label_local.pack(side="left", fill="both", expand=True)

                label_bodega = tk.Label(celda_frame)
                label_bodega.pack(side="left", fill="both", expand=True)

                celdas[(modelo, talla)] = (label_local, label_bodega, celda_frame)

                for w in (celda_frame, label_local, label_bodega):
                    w.bind("<Button-1>", lambda e, m=modelo, t=talla: seleccionar(m, t))

    # =========================
    # 🔹 ACTUALIZAR DATOS (RÁPIDO)
    # =========================
    def actualizar_tabla():

        datos = inventario_servicios.obtener_stock(state.categoria_actual)
        filtro = state.busqueda_modelo.lower().strip()

        matriz = {}

        for (modelo, talla), valores in datos.items():

            if filtro and filtro not in modelo.lower():
                continue

            if modelo not in matriz:
                matriz[modelo] = {t: {"local": 0, "bodega": 0} for t in TALLAS}

            matriz[modelo][talla] = valores

        # 🔥 construir solo si no existe
        if not celdas:
            construir_tabla(matriz)

        # 🔥 actualizar valores sin redibujar
        for (modelo, talla), (l_local, l_bodega, frame_ref) in celdas.items():

            val = matriz.get(modelo, {}).get(talla, {"local": 0, "bodega": 0})

            l_local.config(
                text=str(val["local"]),
                bg="#4CAF50" if val["local"] > 0 else "#EEEEEE",
                fg="white" if val["local"] > 0 else "black"
            )

            l_bodega.config(
                text=str(val["bodega"]),
                bg="#F44336" if val["bodega"] > 0 else "#EEEEEE",
                fg="white" if val["bodega"] > 0 else "black"
            )

        actualizar_seleccion()

    # =========================
    # 🔹 INIT
    # =========================
    crear_header()

    return actualizar_tabla
