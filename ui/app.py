import os
import sys
import tkinter as tk
from tkinter import ttk

from ui import formulario, resumen, tabla
from ui.theme import BG_PRIMARY, BG_TERTIARY, FG_MUTED, FG_PRIMARY, setup_ttk_theme


# ===============================
# 🔹 FIX PYINSTALLER (CLAVE)
# ===============================
def recurso_path(ruta_relativa):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)


GIF_PATH = recurso_path(os.path.join("assets", "banner.gif"))
MAX_GIF_HEIGHT = 80


# ===============================
# 🔹 BANNER SUPERIOR
# ===============================
def _insertar_gif_superior(parent):

    banner = tk.Frame(parent, bg=BG_TERTIARY, height=90)
    banner.pack(fill="x", pady=(0, 4))
    banner.pack_propagate(False)

    titulo = tk.Label(
        banner,
        text="♪♫•*¨*•.¸¸★*♪。☆*★* ☥  𝔐𝔲𝔰𝔲𝔟𝔦 HR░▒▓█  ☥ ☆*★*♪。☆*★*♪。¸¸.•*¨*•♫♪ ",
        bg=BG_TERTIARY,
        fg=FG_PRIMARY,
        font=("Segoe UI", 13, "bold"),
    )
    titulo.pack(side="left", padx=10, pady=6)

    # 🔹 Validar existencia del GIF
    if not os.path.exists(GIF_PATH):
        tk.Label(
            banner,
            text="(No se encontró banner.gif)",
            bg=BG_TERTIARY,
            fg=FG_MUTED,
            font=("Segoe UI", 9),
        ).pack(side="right", padx=10)
        return

    gif_label = tk.Label(banner, bg=BG_TERTIARY)
    gif_label.pack(side="right", padx=10)

    # ===============================
    # 🔹 CARGAR FRAMES GIF
    # ===============================
    frames_originales = []
    index = 0

    while True:
        try:
            frame = tk.PhotoImage(file=GIF_PATH, format=f"gif -index {index}")
        except tk.TclError:
            break
        frames_originales.append(frame)
        index += 1

    if not frames_originales:
        return

    # 🔹 Escalado automático
    alto_original = max(1, frames_originales[0].height())
    factor = max(1, -(-alto_original // MAX_GIF_HEIGHT))
    frames = [f.subsample(factor, factor) for f in frames_originales]

    # ===============================
    # 🔹 ANIMACIÓN
    # ===============================
    def animar(pos=0):
        gif_label.config(image=frames[pos])
        siguiente = (pos + 1) % len(frames)
        banner.after(90, lambda: animar(siguiente))

    # 🔹 evitar garbage collector
    banner._gif_frames = frames

    animar()


# ===============================
# 🔹 SECCIONES UI
# ===============================
def _crear_labelframe(parent, texto):

    seccion = ttk.LabelFrame(parent, text=texto, style="Dark.TLabelframe")
    seccion.pack(fill="x", pady=5)

    cuerpo = tk.Frame(seccion, bg=BG_PRIMARY)
    cuerpo.pack(fill="both", expand=True)

    return seccion, cuerpo


# ===============================
# 🔹 APP PRINCIPAL
# ===============================
def iniciar_app():

    root = tk.Tk()
    root.title("[̲̲̅̅I̲̲̅̅n̲̲̅̅v̲̲̅̅e̲̲̅̅n̲̲̅̅t̲̲̅̅a̲̲̅̅r̲̲̅̅i̲̲̅̅o̲̲̅̅]")
    root.geometry("1100x700")
    root.configure(bg=BG_PRIMARY)

    setup_ttk_theme()

    contenedor = tk.Frame(root, bg=BG_PRIMARY)
    contenedor.pack(fill="both", expand=True, padx=10, pady=10)

    # 🔹 Banner superior
    _insertar_gif_superior(contenedor)

    # 🔹 Secciones
    _, frame_top = _crear_labelframe(contenedor, "Agregar Polera      ══════·")

    seccion_tabla, frame_tabla = _crear_labelframe(contenedor, "Inventario            ══════·")
    seccion_tabla.pack_configure(fill="both", expand=True)

    _, frame_bottom = _crear_labelframe(contenedor, "Control de Stock       ════·")
    _, frame_resumen = _crear_labelframe(contenedor, "Resumen             ══════·")

    # 🔹 Inicializar módulos
    cargar_tabla = tabla.crear_tabla(frame_tabla)
    cargar_resumen = resumen.crear_resumen(frame_resumen)

    def actualizar_todo():
        cargar_tabla()
        cargar_resumen()

    formulario.crear_formulario_superior(frame_top, actualizar_todo)
    formulario.crear_controles(frame_bottom, actualizar_todo)

    # 🔹 Primera carga
    actualizar_todo()

    root.mainloop()