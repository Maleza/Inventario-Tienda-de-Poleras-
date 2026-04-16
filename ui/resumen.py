import tkinter as tk

from servicios import inventario_servicios
from ui import state
from ui.theme import ACCENT, BG_ACCENT, BG_PRIMARY, BG_SECONDARY, FG_MUTED, FG_PRIMARY, SUCCESS, WARNING


def crear_resumen(frame):
    frame.config(bg=BG_PRIMARY)

    contenedor = tk.Frame(frame, bg=BG_PRIMARY)
    contenedor.pack(fill="both", expand=True)

    def cargar_resumen():
        for w in contenedor.winfo_children():
            w.destroy()

        resumen = inventario_servicios.obtener_resumen(state.categoria_actual)
        total_general = 0

        cards = tk.Frame(contenedor, bg=BG_PRIMARY)
        cards.pack(fill="x", pady=5)

        for talla, valores in resumen.items():
            total = valores["local"] + valores["bodega"]
            total_general += total

            card = tk.Frame(cards, bg=BG_SECONDARY, bd=1, relief="solid", highlightbackground=BG_ACCENT)
            card.pack(side="left", padx=5, pady=5, expand=True, fill="x")

            tk.Label(
                card,
                text=talla,
                font=("Segoe UI", 10, "bold"),
                bg=BG_SECONDARY,
                fg=FG_PRIMARY,
            ).pack(pady=(5, 2))

            tk.Label(
                card,
                text=f"Local: {valores['local']}",
                fg=SUCCESS,
                bg=BG_SECONDARY,
                font=("Segoe UI", 9),
            ).pack()

            tk.Label(
                card,
                text=f"Bodega: {valores['bodega']}",
                fg=WARNING,
                bg=BG_SECONDARY,
                font=("Segoe UI", 9),
            ).pack()

            tk.Label(
                card,
                text=f"Total: {total}",
                font=("Segoe UI", 9, "bold"),
                bg=BG_SECONDARY,
                fg=FG_MUTED,
            ).pack(pady=(2, 5))

        tk.Label(
            contenedor,
            text=f"TOTAL GENERAL: {total_general}",
            font=("Segoe UI", 12, "bold"),
            fg=ACCENT,
            bg=BG_PRIMARY,
        ).pack(pady=5)

    return cargar_resumen