import tkinter as tk
from servicios import inventario_servicios
from ui import state

def crear_resumen(frame):

    contenedor = tk.Frame(frame)
    contenedor.pack(fill="both", expand=True)

    def cargar_resumen():

        for w in contenedor.winfo_children():
            w.destroy()

        resumen = inventario_servicios.obtener_resumen(state.categoria_actual)

        total_general = 0

        # 🔹 TARJETAS
        cards = tk.Frame(contenedor)
        cards.pack(fill="x", pady=5)

        for talla, valores in resumen.items():

            total = valores["local"] + valores["bodega"]
            total_general += total

            card = tk.Frame(cards, bg="#f5f5f5", bd=1, relief="solid")
            card.pack(side="left", padx=5, pady=5, expand=True, fill="x")

            tk.Label(card, text=talla,
                     font=("Arial", 10, "bold"),
                     bg="#f5f5f5").pack()

            tk.Label(card, text=f"Local: {valores['local']}",
                     fg="green", bg="#f5f5f5").pack()

            tk.Label(card, text=f"Bodega: {valores['bodega']}",
                     fg="red", bg="#f5f5f5").pack()

            tk.Label(card, text=f"Total: {total}",
                     font=("Arial", 9, "bold"),
                     bg="#f5f5f5").pack()

        tk.Label(contenedor,
                 text=f"TOTAL: {total_general}",
                 font=("Arial", 12, "bold"),
                 fg="blue").pack(pady=5)

    return cargar_resumen