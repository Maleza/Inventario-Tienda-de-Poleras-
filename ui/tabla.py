import tkinter as tk
from servicios import inventario_servicios
from ui import state

TALLAS = ["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"]

celdas = {}
filas_modelo = {}
entrada_activa = None


def crear_tabla(frame):

    frame.pack_propagate(False)

    contenedor_principal = tk.Frame(frame)
    contenedor_principal.pack(fill="both", expand=True)

    frame_header = tk.Frame(contenedor_principal)
    frame_header.pack(fill="x")

    frame_body = tk.Frame(contenedor_principal)
    frame_body.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_body, highlightthickness=0)
    scrollbar = tk.Scrollbar(frame_body, orient="vertical", command=canvas.yview)

    contenedor = tk.Frame(canvas)

    window_id = canvas.create_window((0, 0), window=contenedor, anchor="nw")

    def resize_canvas(event):
        canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    contenedor.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # =========================
    # 🔹 SELECCIÓN
    # =========================
    def seleccionar(modelo, talla):
        state.modelo_seleccionado = modelo
        state.talla_seleccionada = talla
        actualizar_seleccion()

    def actualizar_seleccion():
        for (m, t), (_, _, f) in celdas.items():
            f.config(borderwidth=3 if (m == state.modelo_seleccionado and t == state.talla_seleccionada) else 1)

    # =========================
    # 🔹 HEADER
    # =========================
    def crear_header():
        tk.Label(frame_header, text="Modelo", bg="#222", fg="white").grid(row=0, column=0, sticky="nsew")

        for i, talla in enumerate(TALLAS):
            tk.Label(frame_header, text=talla, bg="#222", fg="white").grid(row=0, column=i+1, sticky="nsew")

        for col in range(len(TALLAS)+1):
            frame_header.grid_columnconfigure(col, weight=1, uniform="col")
            contenedor.grid_columnconfigure(col, weight=1, uniform="col")

    # =========================
    # 🔹 EDITOR EXCEL
    # =========================
    def editar_celda(modelo, talla):

        global entrada_activa

        if entrada_activa:
            entrada_activa.destroy()

        l_local, l_bodega, frame_ref = celdas[(modelo, talla)]

        editor = tk.Frame(frame_ref)
        editor.pack(fill="both", expand=True)

        entry_local = tk.Entry(editor, width=5, justify="center")
        entry_bodega = tk.Entry(editor, width=5, justify="center")

        entry_local.pack(side="left", fill="both", expand=True)
        entry_bodega.pack(side="left", fill="both", expand=True)

        entry_local.focus()

        entrada_activa = editor

        def guardar(event=None):

            try:
                val_local = int(entry_local.get() or 0)
                val_bodega = int(entry_bodega.get() or 0)
            except:
                return

            inventario_servicios.actualizar_stock_directo(
                modelo,
                state.categoria_actual,
                talla,
                val_local,
                val_bodega
            )

            editor.destroy()
            actualizar_tabla()

        def vender(event=None):
            # 🔹 resta 1 unidad del LOCAL
            inventario_servicios.agregar_stock(
                modelo,
                state.categoria_actual,
                talla,
                "local",
                -1
            )
            editor.destroy()
            actualizar_tabla()

        # ENTER = guardar
        entry_local.bind("<Return>", guardar)
        entry_bodega.bind("<Return>", guardar)

        # SHIFT+ENTER = venta directa
        entry_local.bind("<Shift-Return>", vender)

        # ESC = cancelar
        entry_local.bind("<Escape>", lambda e: editor.destroy())
        entry_bodega.bind("<Escape>", lambda e: editor.destroy())

        # navegación
        entry_local.bind("<Right>", lambda e: entry_bodega.focus())
        entry_bodega.bind("<Left>", lambda e: entry_local.focus())

        entry_local.bind("<Down>", lambda e: mover(1, 0, modelo, talla))
        entry_local.bind("<Up>", lambda e: mover(-1, 0, modelo, talla))

    # =========================
    # 🔹 NAVEGACIÓN
    # =========================
    def mover(df, dc, modelo, talla):

        modelos = list(filas_modelo.keys())
        fila = modelos.index(modelo)
        col = TALLAS.index(talla)

        nueva_fila = max(0, min(len(modelos)-1, fila+df))
        nueva_col = max(0, min(len(TALLAS)-1, col+dc))

        editar_celda(modelos[nueva_fila], TALLAS[nueva_col])

    # =========================
    # 🔹 ACTUALIZAR TABLA
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

        fila = 0

        for modelo, tallas in matriz.items():

            if modelo not in filas_modelo:

                lbl = tk.Label(contenedor, text=modelo, bg="#eee")
                lbl.grid(row=fila, column=0, sticky="nsew")

                filas_modelo[modelo] = lbl

                for j, talla in enumerate(TALLAS, start=1):

                    frame_ref = tk.Frame(contenedor, relief="solid", borderwidth=1)
                    frame_ref.grid(row=fila, column=j, sticky="nsew")

                    l1 = tk.Label(frame_ref)
                    l1.pack(side="left", expand=True, fill="both")

                    l2 = tk.Label(frame_ref)
                    l2.pack(side="left", expand=True, fill="both")

                    celdas[(modelo, talla)] = (l1, l2, frame_ref)

                    for w in (frame_ref, l1, l2):
                        w.bind("<Button-1>", lambda e, m=modelo, t=talla: seleccionar(m, t))

                    frame_ref.bind("<Double-1>", lambda e, m=modelo, t=talla: editar_celda(m, t))

                fila += 1

        for (modelo, talla), (l1, l2, _) in celdas.items():

            val = matriz.get(modelo, {}).get(talla, {"local": 0, "bodega": 0})

            l1.config(text=val["local"], bg="#4CAF50" if val["local"] else "#eee")
            l2.config(text=val["bodega"], bg="#F44336" if val["bodega"] else "#eee")

        actualizar_seleccion()

    crear_header()

    return actualizar_tabla