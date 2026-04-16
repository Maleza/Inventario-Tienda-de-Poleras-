from tkinter import ttk

BG_PRIMARY = "#111827"
BG_SECONDARY = "#1F2937"
BG_TERTIARY = "#0F172A"
BG_ACCENT = "#374151"
FG_PRIMARY = "#F9FAFB"
FG_MUTED = "#D1D5DB"
ACCENT = "#60A5FA"
DANGER = "#EF4444"
SUCCESS = "#22C55E"
WARNING = "#F87171"

_STYLE_READY = False


def setup_ttk_theme():
    global _STYLE_READY
    if _STYLE_READY:
        return

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Dark.TCombobox",
        fieldbackground=BG_SECONDARY,
        background=BG_SECONDARY,
        foreground=FG_PRIMARY,
        arrowcolor=FG_PRIMARY,
        bordercolor=BG_ACCENT,
        lightcolor=BG_ACCENT,
        darkcolor=BG_ACCENT,
        relief="flat",
        padding=4,
    )
    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", BG_SECONDARY)],
        background=[("readonly", BG_SECONDARY)],
        foreground=[("readonly", FG_PRIMARY)],
    )

    style.configure(
        "Dark.TLabelframe",
        background=BG_PRIMARY,
        foreground=FG_PRIMARY,
        bordercolor=BG_ACCENT,
    )
    style.configure("Dark.TLabelframe.Label", background=BG_PRIMARY, foreground=FG_PRIMARY)

    _STYLE_READY = True