import tkinter as tk
from tkinter import ttk

from servicios import inventario_servicios
from ui import state
from ui.theme import (
    ACCENT,
    BG_ACCENT,
    BG_PRIMARY,
    BG_SECONDARY,
    BG_TERTIARY,
    DANGER,
    FG_MUTED,
    FG_PRIMARY,
    setup_ttk_theme,
)


def _estilizar_frame(frame, bg=BG_PRIMARY):
    frame.config(bg=bg)


def _crear_label(parent, text, bold=False, color=FG_MUTED):
    return tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=("Segoe UI", 10, "bold" if bold else "normal"),
    )


def _crear_entry(parent, variable, width=20):
    return tk.Entry(
        parent,
        textvariable=variable,
        width=width,
        bg=BG_SECONDARY,
        fg=FG_PRIMARY,
        insertbackground=FG_PRIMARY,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BG_ACCENT,
        highlightcolor=ACCENT,
    )


def _crear_boton(parent, text, command, color=ACCENT, fg="#0B1220", width=None):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=color,
        activeforeground=fg,
        relief="flat",
        bd=0,
        padx=10,
        pady=5,
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        width=width,
    )


# ===============================
# 🔹 FORMULARIO SUPERIOR (AGREGAR)
# ===============================
def crear_formulario_superior(frame, actualizar_todo):
    setup_ttk_theme()
    _estilizar_frame(frame, BG_TERTIARY)
    frame.config(padx=10, pady=10)

    nombre_var = tk.StringVar()
    categoria_var = tk.StringVar(value="Musica")
    ubicacion_var = tk.StringVar(value="local")
    cantidad_var = tk.IntVar(value=1)
    talla_var = tk.StringVar(value="M")

    _crear_label(frame, "Nombre").grid(row=0, column=0, padx=5)
    _crear_entry(frame, nombre_var, width=25).grid(row=0, column=1, padx=5)

    _crear_label(frame, "Categoría").grid(row=0, column=2, padx=5)
    combo_categoria_form = ttk.Combobox(
        frame,
        textvariable=categoria_var,
        values=["Musica", "Animacion"],
        state="readonly",
        width=12,
        style="Dark.TCombobox",
    )
    combo_categoria_form.grid(row=0, column=3, padx=5)

    _crear_label(frame, "Talla").grid(row=0, column=4, padx=5)
    ttk.Combobox(
        frame,
        textvariable=talla_var,
        values=["9/10", "11/12", "16", "S", "M", "L", "XL", "XXL"],
        state="readonly",
        width=6,
        style="Dark.TCombobox",
    ).grid(row=0, column=5, padx=5)

    _crear_label(frame, "Ubicación").grid(row=0, column=6, padx=5)
    ttk.Combobox(
        frame,
        textvariable=ubicacion_var,
        values=["local", "bodega"],
        state="readonly",
        width=10,
        style="Dark.TCombobox",
    ).grid(row=0, column=7, padx=5)

    _crear_label(frame, "Cantidad").grid(row=0, column=8, padx=5)
    _crear_entry(frame, cantidad_var, width=5).grid(row=0, column=9, padx=5)

    def agregar():
        if not nombre_var.get() or cantidad_var.get() <= 0:
            return

        inventario_servicios.agregar_stock(
            nombre_var.get(),
            categoria_var.get(),
            talla_var.get(),
            ubicacion_var.get(),
            cantidad_var.get(),
        )

        nombre_var.set("")
        cantidad_var.set(1)
        actualizar_todo()

    def eliminar():
        if state.modelo_seleccionado:
            inventario_servicios.eliminar_modelo(state.modelo_seleccionado)
            actualizar_todo()

    def cambiar_categoria_form(event=None):
        state.categoria_actual = categoria_var.get()
        state.modelo_seleccionado = None
        state.talla_seleccionada = None
        actualizar_todo()

    combo_categoria_form.bind("<<ComboboxSelected>>", cambiar_categoria_form)

    _crear_boton(frame, "Agregar Polera", agregar).grid(row=0, column=10, padx=(10, 5))
    _crear_boton(frame, "Eliminar Polera", eliminar, color=DANGER, fg=FG_PRIMARY).grid(
        row=0, column=11, padx=5
    )


# ===============================
# 🔹 CONTROLES INFERIORES (+ / -)
# ===============================
def crear_controles(frame, actualizar_todo):
    setup_ttk_theme()
    _estilizar_frame(frame, BG_PRIMARY)
    frame.config(padx=10, pady=10)

    cantidad = tk.IntVar(value=1)
    ubicacion_var = tk.StringVar(value="local")
    busqueda_var = tk.StringVar()
    categoria_tabla_var = tk.StringVar(value=state.categoria_actual)

    fila = tk.Frame(frame, bg=BG_PRIMARY)
    fila.pack(fill="x")

    _crear_label(fila, "Buscar:").pack(side="left", padx=5)
    _crear_entry(fila, busqueda_var, width=20).pack(side="left", padx=5)

    _crear_boton(
        fila,
        text="Limpiar",
        command=lambda: busqueda_var.set(""),
        color=BG_ACCENT,
        fg=FG_PRIMARY,
        width=8,
    ).pack(side="left", padx=2)

    def filtrar(*args):
        state.busqueda_modelo = busqueda_var.get()
        actualizar_todo()

    busqueda_var.trace_add("write", filtrar)

    _crear_label(fila, "Categoría:").pack(side="left", padx=(10, 5))

    combo_categoria = ttk.Combobox(
        fila,
        textvariable=categoria_tabla_var,
        values=["Musica", "Animacion"],
        state="readonly",
        width=12,
        style="Dark.TCombobox",
    )
    combo_categoria.pack(side="left", padx=5)

    def cambiar_categoria(event=None):
        state.categoria_actual = categoria_tabla_var.get()
        state.modelo_seleccionado = None
        state.talla_seleccionada = None
        actualizar_todo()

    combo_categoria.bind("<<ComboboxSelected>>", cambiar_categoria)

    label = tk.Label(
        fila,
        text="Selecciona celda",
        bg=BG_PRIMARY,
        fg=ACCENT,
        font=("Segoe UI", 10, "bold"),
    )
    label.pack(side="left", padx=10)

    ttk.Combobox(
        fila,
        textvariable=ubicacion_var,
        values=["local", "bodega"],
        state="readonly",
        width=10,
        style="Dark.TCombobox",
    ).pack(side="left", padx=5)

    def cambiar_stock(valor):
        if not state.modelo_seleccionado:
            return

        inventario_servicios.agregar_stock(
            state.modelo_seleccionado,
            state.categoria_actual,
            state.talla_seleccionada,
            ubicacion_var.get(),
            valor,
        )
        actualizar_todo()

    _crear_boton(
        fila,
        text="-",
        command=lambda: cambiar_stock(-cantidad.get()),
        color=BG_ACCENT,
        fg=FG_PRIMARY,
        width=4,
    ).pack(side="left", padx=5)

    _crear_entry(fila, cantidad, width=5).pack(side="left", padx=5)

    _crear_boton(
        fila,
        text="+",
        command=lambda: cambiar_stock(cantidad.get()),
        color=BG_ACCENT,
        fg=FG_PRIMARY,
        width=4,
    ).pack(side="left", padx=5)

    def actualizar_label():
        if state.modelo_seleccionado:
            label.config(text=f"{state.modelo_seleccionado} - {state.talla_seleccionada}")
        frame.after(300, actualizar_label)

    actualizar_label()