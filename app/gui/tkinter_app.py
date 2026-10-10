"""
Interfaz Tkinter (Fase 5, sección 32 del brief).

Reusa EXCLUSIVAMENTE app/core (search.py, navigation.py) para datos.
Este módulo solo construye widgets y responde a eventos — cero lógica
de negocio propia (Regla 34: DATA -> SERVICES -> INTERFACES).
"""

import tkinter as tk
from tkinter import ttk

from app.core import navigation, search
from app.data.models import Command, Risk

RISK_COLORS = {
    Risk.SEGURO: "#ffffff",   # blanco — mismo color que el texto normal, sin badge especial
    Risk.PRECAUCION: "#ffd400",  # amarillo fuerte, alta visibilidad sobre negro
    Risk.PELIGROSO: "#ff1f1f",   # rojo intenso
}

# Paleta pedida: negro profundo, blanco, azul, amarillo, rojo — sin grises
# intermedios ni verdes. Contraste alto y directo, estilo consola clásica.
BG = "#000000"       # negro puro, sin matices
PANEL_BG = "#0a0a0a"  # negro casi puro, apenas diferenciado para separar paneles
FG = "#ffffff"        # blanco puro
ACCENT = "#1e6fff"    # azul fuerte y saturado
MUTED = "#c9c9c9"     # blanco atenuado (no gris azulado) para texto secundario


class LinuxCommandMasterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Linux Command Master")
        self.geometry("1100x680")
        self.minsize(900, 560)
        self.configure(bg=BG)

        self._history: list[Command] = []  # para el botón "Atrás"
        self._current: Command | None = None

        self._build_style()
        self._build_layout()
        self._populate_tree()
        self._show_welcome()

    # ------------------------------------------------------------------ #
    # Construcción de la interfaz
    # ------------------------------------------------------------------ #
    def _build_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL_BG, foreground=FG,
                         fieldbackground=PANEL_BG, borderwidth=0, rowheight=26,
                         font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", "#111")])
        style.configure("Treeview.Heading", background=BG, foreground=FG, borderwidth=0)
        style.configure("TEntry", fieldbackground=PANEL_BG, foreground=FG,
                         insertcolor=FG, borderwidth=0)
        style.configure("TButton", background=ACCENT, foreground="#111",
                         borderwidth=0, focusthickness=0, padding=6, font=("Segoe UI", 9, "bold"))
        style.map("TButton", background=[("active", "#4d8dff")])
        style.configure("Muted.TButton", background=PANEL_BG, foreground=FG, padding=6)
        style.map("Muted.TButton", background=[("active", "#2a2a2a")])

        # Botones con color fijo — así el rojo y el azul están SIEMPRE
        # visibles en pantalla, sin depender de qué comando esté mostrado.
        style.configure("Primary.TButton", background=ACCENT, foreground="#ffffff",
                         borderwidth=0, focusthickness=0, padding=6, font=("Segoe UI", 9, "bold"))
        style.map("Primary.TButton", background=[("active", "#4d8dff")])

        style.configure("Danger.TButton", background=RISK_COLORS[Risk.PELIGROSO],
                         foreground="#ffffff", borderwidth=0, focusthickness=0,
                         padding=6, font=("Segoe UI", 9, "bold"))
        style.map("Danger.TButton", background=[("active", "#ff5252")])

    def _build_layout(self) -> None:
        # --- Barra superior: búsqueda + navegación ---
        top = tk.Frame(self, bg=BG, pady=8, padx=10)
        top.pack(side="top", fill="x")

        ttk.Button(top, text="Inicio", style="Primary.TButton",
                   command=self._show_welcome).pack(side="left", padx=(0, 4))
        ttk.Button(top, text="← Atrás", style="Danger.TButton",
                   command=self._go_back).pack(side="left", padx=(0, 12))

        self.search_var = tk.StringVar()
        self._search_trace_id = self.search_var.trace_add("write", self._on_search_change)
        search_entry = ttk.Entry(top, textvariable=self.search_var, font=("Segoe UI", 11))
        search_entry.pack(side="left", fill="x", expand=True, ipady=4)
        search_entry.insert(0, "")
        self._search_placeholder(search_entry)

        # --- Cuerpo: sidebar (árbol) + panel de detalle ---
        body = tk.Frame(self, bg=BG)
        body.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

        # Sidebar con scroll
        sidebar = tk.Frame(body, bg=PANEL_BG, width=340)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        self.tree = ttk.Treeview(sidebar, show="tree")
        vscroll = ttk.Scrollbar(sidebar, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Panel de detalle (scrollable)
        detail_container = tk.Frame(body, bg=BG)
        detail_container.pack(side="left", fill="both", expand=True, padx=(10, 0))

        canvas = tk.Canvas(detail_container, bg=BG, highlightthickness=0)
        detail_scroll = ttk.Scrollbar(detail_container, orient="vertical", command=canvas.yview)
        self.detail_frame = tk.Frame(canvas, bg=BG)

        self.detail_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.detail_frame, anchor="nw", width=680)
        canvas.configure(yscrollcommand=detail_scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        detail_scroll.pack(side="right", fill="y")

        self._build_tux_mascot()

    def _build_tux_mascot(self) -> None:
        """Muestra a Tux (la mascota de Linux) usando la imagen real en vez
        de un dibujo hecho a mano — se ve muchísimo mejor. Carga
        app/gui/assets/tux.png desde disco (descargada una sola vez, ver
        README) y la redimensiona con Pillow. Si el archivo no existe o
        Pillow no está instalado, la app sigue funcionando normal, solo
        sin el ícono decorativo — nunca debe romper el uso real de la
        herramienta por un detalle puramente estético."""
        try:
            from pathlib import Path
            from PIL import Image, ImageTk
        except ImportError:
            return  # Pillow no instalado — se omite el ícono, sin romper la app

        asset_path = Path(__file__).parent / "assets" / "tux.png"
        if not asset_path.exists():
            return  # imagen no descargada todavía — se omite el ícono

        try:
            img = Image.open(asset_path).convert("RGBA")
            target_h = 140
            ratio = target_h / img.height
            img = img.resize((int(img.width * ratio), target_h), Image.LANCZOS)
            self._tux_photo = ImageTk.PhotoImage(img)  # guardar referencia:
            # si no se guarda en self, Python la recolecta como basura y la
            # imagen desaparece de la ventana aunque el código sea correcto.
        except Exception:
            return  # archivo corrupto u otro problema — se omite el ícono

        tux_label = tk.Label(self, image=self._tux_photo, bg=BG, borderwidth=0)
        tux_label.place(relx=1.0, rely=1.0, anchor="se", x=-14, y=-10)

    def _search_placeholder(self, entry: ttk.Entry) -> None:
        entry.insert(0, "Buscar comando (ej: docker, grep, permisos)...")
        entry.config(foreground=MUTED)
        entry.bind("<FocusIn>", self._on_search_focus_in)
        entry.bind("<FocusOut>", self._on_search_focus_out)
        self._search_entry = entry
        self._search_is_placeholder = True

    def _on_search_focus_in(self, _event=None) -> None:
        if self._search_is_placeholder:
            self._search_entry.delete(0, "end")
            self._search_entry.config(foreground=FG)
            self._search_is_placeholder = False

    def _on_search_focus_out(self, _event=None) -> None:
        if not self.winfo_exists():
            return
        if not self.search_var.get().strip():
            self._search_is_placeholder = True
            self._search_entry.insert(0, "Buscar comando (ej: docker, grep, permisos)...")
            self._search_entry.config(foreground=MUTED)

    # ------------------------------------------------------------------ #
    # Árbol de navegación (categoría -> subcategoría -> comando)
    # ------------------------------------------------------------------ #
    def _populate_tree(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self._tree_item_to_command: dict[str, Command] = {}

        # Tags de color para las filas de comandos según su riesgo —
        # en vez de un emoji inline, coloreamos el texto completo de la
        # fila, igual que hace 'ls --color' o 'git status' en terminal.
        self.tree.tag_configure("risk_precaucion", foreground=RISK_COLORS[Risk.PRECAUCION])
        self.tree.tag_configure("risk_peligroso", foreground=RISK_COLORS[Risk.PELIGROSO])

        for cat in navigation.get_all_categories():
            cat_node = self.tree.insert("", "end", text=cat.name, open=False)
            for sub_info in navigation.get_subcategories(cat.id):
                if sub_info.command_count == 0:
                    continue
                sub_node = self.tree.insert(
                    cat_node, "end",
                    text=f"{sub_info.subcategory.name} ({sub_info.command_count})",
                    open=False,
                )
                for cmd in navigation.get_commands(cat.id, sub_info.subcategory.id):
                    tags = ()
                    if cmd.risk == Risk.PRECAUCION:
                        tags = ("risk_precaucion",)
                    elif cmd.risk == Risk.PELIGROSO:
                        tags = ("risk_peligroso",)
                    leaf = self.tree.insert(sub_node, "end", text=cmd.name, tags=tags)
                    self._tree_item_to_command[leaf] = cmd

    def _on_tree_select(self, _event=None) -> None:
        selected = self.tree.selection()
        if not selected:
            return
        cmd = self._tree_item_to_command.get(selected[0])
        if cmd:
            self._show_command(cmd, push_history=True)

    # ------------------------------------------------------------------ #
    # Búsqueda incremental
    # ------------------------------------------------------------------ #
    def _on_search_change(self, *_args) -> None:
        if getattr(self, "_search_is_placeholder", False):
            return
        query = self.search_var.get().strip()
        try:
            if not query:
                self._show_welcome()
                return
            results = search.search(query, limit=30)
            self._show_search_results(query, results)
        except (AttributeError, tk.TclError):
            # La ventana se está cerrando y Tk disparó este evento en medio
            # de la destrucción de widgets (ej: la barra de búsqueda pierde
            # el foco al cerrarse). No afecta el uso normal de la app.
            pass

    def _show_search_results(self, query: str, results) -> None:
        self._clear_detail()
        tk.Label(self.detail_frame, text=f"Resultados para: '{query}'",
                 font=("Segoe UI", 14, "bold"), bg=BG, fg=FG,
                 anchor="w").pack(fill="x", pady=(4, 10))

        if not results:
            tk.Label(self.detail_frame, text="Sin resultados.", bg=BG, fg=MUTED).pack(anchor="w")
            return

        for r in results:
            row = tk.Frame(self.detail_frame, bg=PANEL_BG, pady=6, padx=10)
            row.pack(fill="x", pady=3)
            btn = tk.Label(
                row, text=f"{r.command.name}", bg=PANEL_BG, fg=ACCENT,
                font=("Segoe UI", 11, "bold"), cursor="hand2", anchor="w",
            )
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, c=r.command: self._show_command(c, push_history=True))
            tk.Label(row, text=r.command.description, bg=PANEL_BG, fg=MUTED,
                     wraplength=620, justify="left", anchor="w").pack(fill="x")

    # ------------------------------------------------------------------ #
    # Panel de detalle de un comando
    # ------------------------------------------------------------------ #
    def _clear_detail(self) -> None:
        for w in self.detail_frame.winfo_children():
            w.destroy()

    def _show_welcome(self) -> None:
        self._current = None
        self._clear_detail()
        tk.Label(self.detail_frame, text="Linux Command Master",
                 font=("Segoe UI", 20, "bold"), bg=BG, fg=FG).pack(anchor="w", pady=(20, 6))
        tk.Label(
            self.detail_frame,
            text="Selecciona una categoría en el panel izquierdo o busca un comando arriba.",
            font=("Segoe UI", 11), bg=BG, fg=MUTED, wraplength=620, justify="left",
        ).pack(anchor="w")

    def _show_command(self, cmd: Command, push_history: bool) -> None:
        if push_history and self._current and self._current.id != cmd.id:
            self._history.append(self._current)
        self._current = cmd
        self._clear_detail()

        # Título + nivel
        header = tk.Frame(self.detail_frame, bg=BG)
        header.pack(fill="x", pady=(6, 2))
        tk.Label(header, text=cmd.name, font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=FG).pack(side="left")
        tk.Label(header, text=f"  {cmd.level.value}", font=("Segoe UI", 10),
                 bg=BG, fg=MUTED).pack(side="left")

        # Indicador de riesgo
        if cmd.risk != Risk.SEGURO:
            risk_lbl = tk.Label(
                self.detail_frame, text=f"[{cmd.risk.value}]", font=("Segoe UI", 10, "bold"),
                bg=BG, fg=RISK_COLORS[cmd.risk],
            )
            risk_lbl.pack(anchor="w", pady=(0, 6))

        self._section(self.detail_frame, "Descripción", cmd.description)
        self._section_code(self.detail_frame, "Sintaxis", cmd.syntax, copyable=True)

        if cmd.examples:
            self._section_title(self.detail_frame, "Ejemplos")
            for ex in cmd.examples:
                self._section_code(self.detail_frame, None, ex, copyable=True)

        if cmd.when_to_use:
            self._section(self.detail_frame, "Cuándo usar", cmd.when_to_use)

        if cmd.options:
            self._section_title(self.detail_frame, "Opciones importantes")
            for opt in cmd.options:
                tk.Label(self.detail_frame, text=f"  •  {opt}", bg=BG, fg=FG,
                         font=("Segoe UI", 10), anchor="w").pack(fill="x")

        if cmd.risk != Risk.SEGURO and cmd.precautions:
            self._section(self.detail_frame, "Precaución", cmd.precautions,
                          fg=RISK_COLORS[cmd.risk])

        if cmd.replaces:
            self._section(self.detail_frame, "Modernización",
                          f"Reemplaza al comando más antiguo: {cmd.replaces}")
        if cmd.replaced_by:
            self._section(self.detail_frame, "Modernización",
                          f"Se recomienda usar en su lugar: {cmd.replaced_by}")

        related = search.related_commands(cmd.id)
        if related:
            self._section_title(self.detail_frame, "Comandos relacionados")
            rel_frame = tk.Frame(self.detail_frame, bg=BG)
            rel_frame.pack(fill="x", pady=(0, 10))
            for r in related:
                chip = tk.Label(
                    rel_frame, text=r.name, bg=PANEL_BG, fg=ACCENT,
                    font=("Segoe UI", 9, "bold"), padx=10, pady=4, cursor="hand2",
                )
                chip.pack(side="left", padx=(0, 6), pady=2)
                chip.bind("<Button-1>", lambda e, c=r: self._show_command(c, push_history=True))

        if cmd.tags:
            tags_txt = "  ".join(f"#{t}" for t in cmd.tags)
            tk.Label(self.detail_frame, text=tags_txt, bg=BG, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 20))

    def _section_title(self, parent, title: str) -> None:
        tk.Label(parent, text=title, font=("Segoe UI", 11, "bold"),
                 bg=BG, fg=ACCENT, anchor="w").pack(fill="x", pady=(12, 2))

    def _section(self, parent, title: str, text: str, fg: str = FG) -> None:
        self._section_title(parent, title)
        tk.Label(parent, text=text, font=("Segoe UI", 10), bg=BG, fg=fg,
                 wraplength=620, justify="left", anchor="w").pack(fill="x")

    def _section_code(self, parent, title: str | None, code: str, copyable: bool = False) -> None:
        if title:
            self._section_title(parent, title)
        row = tk.Frame(parent, bg=PANEL_BG)
        row.pack(fill="x", pady=2)

        # El botón de copiar (ancho fijo) se empaqueta PRIMERO para que
        # reserve su espacio en la fila; si se empaqueta después de un
        # widget con expand=True, ese widget se come todo el ancho y el
        # botón queda aplastado a 0px, invisible y sin poder recibir clics.
        if copyable:
            copy_btn = tk.Label(row, text="Copiar", bg=PANEL_BG, fg=ACCENT,
                                 font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10)
            copy_btn.pack(side="right", fill="y")
            copy_btn.bind("<Button-1>", lambda e, c=code: self._copy_to_clipboard(e.widget, c))
            copy_btn.bind("<Enter>", lambda e: copy_btn.config(bg="#2a2a2a"))
            copy_btn.bind("<Leave>", lambda e: copy_btn.config(bg=PANEL_BG))

        tk.Label(row, text=f"$ {code}", font=("Consolas", 10), bg=PANEL_BG, fg="#ffd400",
                 wraplength=560, justify="left", anchor="w", padx=8, pady=6).pack(
            side="left", fill="x", expand=True
        )

    def _copy_to_clipboard(self, widget: tk.Label, text: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # fuerza que el portapapeles se actualice de inmediato

        original_text = widget.cget("text")
        original_fg = widget.cget("fg")
        widget.config(text="✓ Copiado", fg="#ffd400")
        widget.after(1200, lambda: widget.config(text=original_text, fg=original_fg))

    # ------------------------------------------------------------------ #
    def destroy(self) -> None:
        # Desregistrar el trace del StringVar ANTES de destruir la ventana.
        # Si no se hace, Tcl puede disparar _on_search_change durante el
        # cierre (ej: al perder el foco la barra de búsqueda), intentando
        # actualizar widgets que ya no existen.
        try:
            self.search_var.trace_remove("write", self._search_trace_id)
        except Exception:
            pass
        super().destroy()

    def _go_back(self) -> None:
        if self._history:
            prev = self._history.pop()
            self._show_command(prev, push_history=False)
        else:
            self._show_welcome()


def main() -> None:
    app = LinuxCommandMasterApp()
    app.mainloop()


if __name__ == "__main__":
    main()