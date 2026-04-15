import tkinter as tk
from servicios import inventario_servicios
from ui import state

TALLAS = ["7/8","9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"]

celdas = {}
filas_modelo = {}
entrada_activa = None
__all__ = ["crear_tabla"]


def crear_tabla(frame):
    frame.pack_propagate(False)
    celdas.clear()
    filas_modelo.clear()

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
            seleccionado = (m == state.modelo_seleccionado and t == state.talla_seleccionada)
            f.config(
                borderwidth=3 if seleccionado else 1,
                highlightthickness=1 if seleccionado else 0,
                highlightbackground="#1976D2"
            )

    def construir_grilla(matriz):
        for widget in contenedor.winfo_children():
            widget.destroy()

        celdas.clear()
        filas_modelo.clear()

        for fila, (modelo, _tallas) in enumerate(matriz.items()):
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

    def asegurar_celda_visible(modelo, talla):
        if (modelo, talla) not in celdas:
            return

        frame_ref = celdas[(modelo, talla)][2]
        frame.update_idletasks()

        viewport_top = canvas.canvasy(0)
        viewport_bottom = viewport_top + canvas.winfo_height()
        celda_top = frame_ref.winfo_y()
        celda_bottom = celda_top + frame_ref.winfo_height()

        total_alto = max(1, contenedor.winfo_height())

        if celda_top < viewport_top:
            canvas.yview_moveto(max(0.0, celda_top / total_alto))
        elif celda_bottom > viewport_bottom:
            destino = (celda_bottom - canvas.winfo_height()) / total_alto
            canvas.yview_moveto(min(1.0, max(0.0, destino)))

    # =========================
    # 🔹 HEADER
    # =========================
    def crear_header():
        tk.Label(frame_header, text="Modelo", bg="#222", fg="white").grid(row=0, column=0, sticky="nsew")

        for i, talla in enumerate(TALLAS):
            tk.Label(frame_header, text=talla, bg="#222", fg="white").grid(row=0, column=i + 1, sticky="nsew")

        for col in range(len(TALLAS) + 1):
            frame_header.grid_columnconfigure(col, weight=1, uniform="col")
            contenedor.grid_columnconfigure(col, weight=1, uniform="col")

    # =========================
    # 🔹 EDITOR EXCEL
    # =========================
    def editar_celda(modelo, talla):
        global entrada_activa

        if (modelo, talla) not in celdas:
            return

        if entrada_activa:
            entrada_activa.destroy()

        l_local, l_bodega, frame_ref = celdas[(modelo, talla)]

        editor = tk.Frame(frame_ref)
        editor.pack(fill="both", expand=True)

        valor_local = l_local.cget("text") or "0"
        valor_bodega = l_bodega.cget("text") or "0"

        entry_local = tk.Entry(editor, width=5, justify="center")
        entry_bodega = tk.Entry(editor, width=5, justify="center")

        entry_local.pack(side="left", fill="both", expand=True)
        entry_bodega.pack(side="left", fill="both", expand=True)

        entry_local.insert(0, valor_local)
        entry_bodega.insert(0, valor_bodega)
        entry_local.select_range(0, tk.END)
        entry_local.focus()

        entrada_activa = editor
        seleccionar(modelo, talla)

        def guardar(event=None):
            global entrada_activa

            try:
                val_local = int(entry_local.get() or 0)
                val_bodega = int(entry_bodega.get() or 0)
            except ValueError:
                return "break"

            inventario_servicios.actualizar_stock_directo(
                modelo,
                state.categoria_actual,
                talla,
                val_local,
                val_bodega
            )
            state.modelo_seleccionado = modelo
            state.talla_seleccionada = talla

            if entrada_activa:
                entrada_activa.destroy()
                entrada_activa = None

            actualizar_tabla()
            return "break"

        def vender(event=None):
            global entrada_activa

            inventario_servicios.agregar_stock(
                modelo,
                state.categoria_actual,
                talla,
                "local",
                -1
            )
            state.modelo_seleccionado = modelo
            state.talla_seleccionada = talla

            if entrada_activa:
                entrada_activa.destroy()
                entrada_activa = None

            actualizar_tabla()
            return "break"

        def cancelar(event=None):
            global entrada_activa

            if entrada_activa:
                entrada_activa.destroy()
                entrada_activa = None

            actualizar_tabla()
            return "break"

        def mover_y_editar(df, dc):
            guardar()
            return mover(df, dc, modelo, talla)

        # ENTER = guardar
        entry_local.bind("<Return>", guardar)
        entry_bodega.bind("<Return>", guardar)

        # SHIFT+ENTER = venta directa
        entry_local.bind("<Shift-Return>", vender)

        # ESC = cancelar
        entry_local.bind("<Escape>", cancelar)
        entry_bodega.bind("<Escape>", cancelar)

        # navegación tipo excel
        entry_local.bind("<Right>", lambda e: entry_bodega.focus() or "break")
        entry_bodega.bind("<Left>", lambda e: entry_local.focus() or "break")
        entry_local.bind("<Left>", lambda e: mover_y_editar(0, -1))
        entry_bodega.bind("<Right>", lambda e: mover_y_editar(0, 1))
        entry_local.bind("<Down>", lambda e: mover_y_editar(1, 0))
        entry_bodega.bind("<Down>", lambda e: mover_y_editar(1, 0))
        entry_local.bind("<Up>", lambda e: mover_y_editar(-1, 0))
        entry_bodega.bind("<Up>", lambda e: mover_y_editar(-1, 0))

        # click fuera del editor guarda cambios
        editor.bind("<FocusOut>", lambda e: frame.after(1, guardar))

    # =========================
    # 🔹 NAVEGACIÓN
    # =========================
    def mover(df, dc, modelo, talla):
        modelos = list(filas_modelo.keys())
        if not modelos:
            return "break"

        if modelo not in modelos:
            modelo = modelos[0]

        fila = modelos.index(modelo)
        col = TALLAS.index(talla)

        nueva_fila = max(0, min(len(modelos) - 1, fila + df))
        nueva_col = max(0, min(len(TALLAS) - 1, col + dc))

        siguiente_modelo = modelos[nueva_fila]
        siguiente_talla = TALLAS[nueva_col]

        seleccionar(siguiente_modelo, siguiente_talla)
        asegurar_celda_visible(siguiente_modelo, siguiente_talla)
        editar_celda(siguiente_modelo, siguiente_talla)
        return "break"

    # =========================
    # 🔹 ACTUALIZAR TABLA
    # =========================
    def actualizar_tabla():
        global entrada_activa

        datos = inventario_servicios.obtener_stock(state.categoria_actual)
        filtro = state.busqueda_modelo.lower().strip()

        matriz = {}

        for (modelo, talla), valores in datos.items():
            if filtro and filtro not in modelo.lower():
                continue

            if modelo not in matriz:
                matriz[modelo] = {t: {"local": 0, "bodega": 0} for t in TALLAS}

            if talla in matriz[modelo]:
                matriz[modelo][talla] = valores

        modelos_actuales = list(filas_modelo.keys())
        modelos_nuevos = list(matriz.keys())
        requiere_reconstruccion = modelos_actuales != modelos_nuevos or not celdas

        if requiere_reconstruccion:
            if entrada_activa:
                entrada_activa.destroy()
                entrada_activa = None
            construir_grilla(matriz)

        for (modelo, talla), (l1, l2, _) in celdas.items():
            val = matriz.get(modelo, {}).get(talla, {"local": 0, "bodega": 0})
            l1.config(text=val["local"], bg="#4CAF50" if val["local"] else "#eee")
            l2.config(text=val["bodega"], bg="#F44336" if val["bodega"] else "#eee")

        if state.modelo_seleccionado not in filas_modelo:
            state.modelo_seleccionado = None
            state.talla_seleccionada = None

        actualizar_seleccion()

    crear_header()

    def abrir_seleccion_actual(event=None):
        if state.modelo_seleccionado and state.talla_seleccionada:
            editar_celda(state.modelo_seleccionado, state.talla_seleccionada)
            return "break"

    def mover_seleccion(df, dc):
        if state.modelo_seleccionado and state.talla_seleccionada:
            return mover(df, dc, state.modelo_seleccionado, state.talla_seleccionada)
        if filas_modelo:
            primer_modelo = next(iter(filas_modelo.keys()))
            seleccionar(primer_modelo, TALLAS[0])
        return "break"

    frame.bind_all("<Return>", abrir_seleccion_actual)
    frame.bind_all("<Up>", lambda e: mover_seleccion(-1, 0))
    frame.bind_all("<Down>", lambda e: mover_seleccion(1, 0))
    frame.bind_all("<Left>", lambda e: mover_seleccion(0, -1))
    frame.bind_all("<Right>", lambda e: mover_seleccion(0, 1))

    return actualizar_tabla