import tkinter as tk
from servicios import inventario_servicios
from ui import state

TALLAS = ["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"]


def crear_tabla(frame):

    contenedor = tk.Frame(frame)
    contenedor.pack(fill="both", expand=True)

    frame.pack_propagate(False)

    def seleccionar(modelo, talla):
        state.modelo_seleccionado = modelo
        state.talla_seleccionada = talla
        cargar_datos()

    def cargar_datos():

        for w in contenedor.winfo_children():
            w.destroy()

        datos = inventario_servicios.obtener_stock(state.categoria_actual)

        matriz = {}

        for (modelo, talla), valores in datos.items():
            if modelo not in matriz:
                matriz[modelo] = {t: {"local": 0, "bodega": 0} for t in TALLAS}
            matriz[modelo][talla] = valores

        # =========================
        # 🔹 ENCABEZADOS
        # =========================
        tk.Label(contenedor, text="Modelo",
                 bg="#222", fg="white", font=("Arial", 10, "bold"))\
            .grid(row=0, column=0, sticky="nsew")

        for i, talla in enumerate(TALLAS):
            tk.Label(contenedor, text=talla,
                     bg="#222", fg="white", font=("Arial", 10, "bold"))\
                .grid(row=0, column=i+1, sticky="nsew")

        # =========================
        # 🔹 FILAS Y CELDAS
        # =========================
        for i, (modelo, tallas) in enumerate(matriz.items(), start=1):

            tk.Label(contenedor, text=modelo, bg="#ddd")\
                .grid(row=i, column=0, sticky="nsew")

            for j, talla in enumerate(TALLAS, start=1):

                val = tallas[talla]

                borde = 3 if (
                    modelo == state.modelo_seleccionado and
                    talla == state.talla_seleccionada
                ) else 1

                # =========================
                # 🔹 CELDA
                # =========================
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

                # =========================
                # 🔹 EVENTOS (CORREGIDO)
                # =========================
                def bind_event(widget, m=modelo, t=talla, frame_ref=celda_frame):

                    widget.bind(
                        "<Button-1>",
                        lambda e: seleccionar(m, t)
                    )

                    widget.bind(
                        "<Enter>",
                        lambda e: frame_ref.config(bg="#dfe6e9")
                    )

                    widget.bind(
                        "<Leave>",
                        lambda e: frame_ref.config(bg="white")
                    )

                for w in (celda_frame, label_local, label_bodega):
                    bind_event(w)

        # =========================
        # 🔹 EXPANSIÓN (UNA SOLA VEZ)
        # =========================
        total_columnas = len(TALLAS) + 1
        for col in range(total_columnas):
            contenedor.grid_columnconfigure(col, weight=1, uniform="col")

        total_filas = len(matriz) + 1
        for fila in range(total_filas):
            contenedor.grid_rowconfigure(fila, weight=1)

    return cargar_datos