"""
Interfaz PyQt6 (v7, funcional) — reemplazo de la GUI Tkinter.

Conectada a app/core (navigation, search, i18n):
  - Menú de categorías desplegable (animado) con subcategorías y scroll
  - Buscador con resultados mientras escribes
  - Ficha de comando con formato propio (riesgo en color, bloques de código)
  - Botón de idioma (recorre los idiomas de Lang)
  - Inicio / Atrás con historial

Look: cristal esmerilado con Pillow, viñeta, grano de película, fade-in.
"""

import os
import random
import sys
import traceback
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps
from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
)
from PyQt6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)

from app.core import i18n, navigation, search
from app.core.i18n import Lang
from app.data.models import Risk


ASSETS = Path(__file__).parent / "assets"
BACKGROUND_PATH = ASSETS / "background.jpg"

# --- Ajustes rápidos de diseño ---
MIRROR_BACKGROUND = True
BLUR_RADIUS = 10
FREE_RIGHT_COLUMN = 360
LEFT_DARKEN_ALPHA = 140
VIGNETTE_ALPHA = 200
EDGE_BARS_ALPHA = 150
GRAIN_ALPHA = 16
GRAIN_ANIMATED = True
ACCENT = "#ffb070"

RISK_COLORS = {
    Risk.SEGURO: "#6fd08c",
    Risk.PRECAUCION: "#ffb070",
    Risk.PELIGROSO: "#ff6b5e",
}

# --- Textos propios de la interfaz (por código de idioma) ---
STRINGS = {
    "es": {
        "home": "Inicio",
        "back": "← Atrás",
        "search": "Buscar comando (ej: docker, grep, permisos)...",
        "categories": "Categorías",
        "welcome_sub": "Selecciona una categoría en el panel izquierdo o busca un comando arriba.",
        "welcome_info": "Despliega una categoría para ver sus subcategorías y comandos.",
        "results_for": "Resultados para",
        "no_results": "Sin resultados.",
        "no_commands": "No hay comandos en esta sección.",
        "commands": "comandos",
        "related": "Relacionados",
        "error": "No se pudo mostrar esta vista",
        "description": "Descripción",
        "syntax": "Sintaxis",
        "examples": "Ejemplos",
        "when_to_use": "Cuándo usarlo",
        "options": "Opciones importantes",
        "precautions": "Precauciones",
        "replaces": "Reemplaza a",
        "replaced_by": "Reemplazado por",
        "deprecated": "Obsoleto",
    },
    "en": {
        "home": "Home",
        "back": "← Back",
        "search": "Search command (e.g. docker, grep, permissions)...",
        "categories": "Categories",
        "welcome_sub": "Pick a category on the left panel or search for a command above.",
        "welcome_info": "Expand a category to see its subcategories and commands.",
        "results_for": "Results for",
        "no_results": "No results.",
        "no_commands": "There are no commands in this section.",
        "commands": "commands",
        "related": "Related",
        "error": "This view could not be displayed",
        "description": "Description",
        "syntax": "Syntax",
        "examples": "Examples",
        "when_to_use": "When to use it",
        "options": "Key options",
        "precautions": "Precautions",
        "replaces": "Replaces",
        "replaced_by": "Replaced by",
        "deprecated": "Deprecated",
    },
}

SCROLL_QSS = """
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QScrollBar:vertical { background: transparent; width: 8px; margin: 2px; }
QScrollBar::handle:vertical { background: rgba(255,255,255,60); border-radius: 4px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: rgba(255,255,255,110); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
"""


# ===================== Utilidades de imagen =====================

def _cover(img: Image.Image, w: int, h: int) -> Image.Image:
    scale = max(w / img.width, h / img.height)
    nw, nh = int(img.width * scale) + 1, int(img.height * scale) + 1
    img = img.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return img.crop((left, top, left + w, top + h))


def _to_pixmap(img: Image.Image) -> QPixmap:
    img = img.convert("RGBA")
    qimg = QImage(
        img.tobytes("raw", "RGBA"),
        img.width,
        img.height,
        QImage.Format.Format_RGBA8888,
    ).copy()
    return QPixmap.fromImage(qimg)


def _grade(pm: QPixmap) -> QPixmap:
    """Gradación cinematográfica: viñeta + lado izquierdo oscuro + bandas arriba/abajo."""
    out = QPixmap(pm)
    w, h = out.width(), out.height()
    p = QPainter(out)

    vignette = QRadialGradient(w / 2, h / 2, max(w, h) * 0.75)
    vignette.setColorAt(0.45, QColor(0, 0, 0, 0))
    vignette.setColorAt(1.0, QColor(0, 0, 0, VIGNETTE_ALPHA))
    p.fillRect(out.rect(), vignette)

    left = QLinearGradient(0, 0, w, 0)
    left.setColorAt(0.0, QColor(4, 6, 14, LEFT_DARKEN_ALPHA))
    left.setColorAt(0.65, QColor(4, 6, 14, 0))
    p.fillRect(out.rect(), left)

    bars = QLinearGradient(0, 0, 0, h)
    bars.setColorAt(0.0, QColor(0, 0, 0, EDGE_BARS_ALPHA))
    bars.setColorAt(0.14, QColor(0, 0, 0, 0))
    bars.setColorAt(0.86, QColor(0, 0, 0, 0))
    bars.setColorAt(1.0, QColor(0, 0, 0, EDGE_BARS_ALPHA + 20))
    p.fillRect(out.rect(), bars)

    p.end()
    return out


# ===================== Utilidades de datos =====================

def _empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, set, frozenset, dict)):
        return len(value) == 0
    return False


def _safe(fn, fallback=""):
    try:
        return fn()
    except Exception:
        return fallback


# ===================== Widgets visuales =====================

class GrainOverlay(QWidget):
    """Grano de película sobre toda la ventana (transparente al ratón)."""

    def __init__(self, parent: QWidget, alpha: int = 16, animated: bool = True):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        size = 256
        noise = Image.frombytes("L", (size, size), os.urandom(size * size))
        alpha_ch = Image.new("L", (size, size), max(0, min(255, alpha)))
        self._tile = _to_pixmap(Image.merge("RGBA", (noise, noise, noise, alpha_ch)))
        self._offset = QPoint(0, 0)
        self._timer = QTimer(self)
        if animated and alpha > 0:
            self._timer.timeout.connect(self._tick)
            self._timer.start(90)

    def _tick(self) -> None:
        self._offset = QPoint(random.randint(0, 255), random.randint(0, 255))
        self.update()

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawTiledPixmap(self.rect(), self._tile, self._offset)


class BackgroundWidget(QWidget):
    """Fondo con gradación + versión desenfocada para los paneles de cristal."""

    def __init__(self, image_path: Path, blur_radius: int = 10, mirror: bool = False, parent=None):
        super().__init__(parent)
        if Path(image_path).exists():
            src = Image.open(image_path).convert("RGB")
        else:
            src = Image.new("RGB", (16, 16), (8, 8, 16))
        self._src = ImageOps.mirror(src) if mirror else src
        self._blur_radius = blur_radius
        self._sharp = QPixmap()
        self._blurred = QPixmap()
        self._grain = GrainOverlay(self, GRAIN_ALPHA, GRAIN_ANIMATED)

    def resizeEvent(self, event) -> None:
        w, h = max(1, self.width()), max(1, self.height())
        base = _cover(self._src, w, h)
        self._sharp = _grade(_to_pixmap(base))

        small = base.resize((max(1, w // 4), max(1, h // 4)), Image.LANCZOS)
        small = small.filter(ImageFilter.GaussianBlur(max(1, self._blur_radius // 4)))
        blurred = _to_pixmap(small).scaled(
            w,
            h,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self._blurred = _grade(blurred)

        self._grain.setGeometry(self.rect())
        self._grain.raise_()
        for panel in self.findChildren(FrostedPanel):
            panel.update()
        super().resizeEvent(event)

    def paintEvent(self, event) -> None:
        QPainter(self).drawPixmap(0, 0, self._sharp)

    def blurred(self) -> QPixmap:
        return self._blurred


class FrostedPanel(QWidget):
    """Panel de cristal esmerilado. Los hijos se dibujan nítidos encima."""

    def __init__(
        self,
        background: BackgroundWidget,
        tint: QColor = QColor(8, 14, 28, 120),
        radius: int = 12,
        margins: tuple = (16, 14, 16, 14),
        horizontal: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self._bg = background
        self._tint = tint
        self._radius = radius
        self._layout = QHBoxLayout(self) if horizontal else QVBoxLayout(self)
        self._layout.setContentsMargins(*margins)
        self._layout.setSpacing(8 if horizontal else 6)

    def content_layout(self):
        return self._layout

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)

        painter.save()
        painter.setClipPath(path)
        origin = self.mapTo(self._bg, QPoint(0, 0))
        painter.drawPixmap(
            0, 0, self._bg.blurred(), origin.x(), origin.y(), self.width(), self.height()
        )
        painter.fillRect(self.rect(), self._tint)
        painter.restore()

        painter.setPen(QPen(QColor(255, 255, 255, 38), 1))
        painter.drawPath(path)


# ===================== Ventana principal =====================

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Linux Command Master")
        self.resize(1280, 720)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        self._old_pos: QPoint | None = None
        self._langs = list(Lang)
        self._lang = self._default_lang()
        self._state: tuple | None = None
        self._history: list = []
        self._anims: dict = {}

        bg = BackgroundWidget(BACKGROUND_PATH, blur_radius=BLUR_RADIUS, mirror=MIRROR_BACKGROUND)
        self.setCentralWidget(bg)

        main_layout = QVBoxLayout(bg)
        main_layout.setContentsMargins(20, 20, 20, 8)
        main_layout.setSpacing(14)

        # ============ Barra superior ============
        top_bar = FrostedPanel(
            bg, tint=QColor(8, 14, 28, 150), radius=10, margins=(14, 8, 14, 8), horizontal=True
        )
        top_bar.setFixedHeight(56)
        tl = top_bar.content_layout()

        self._btn_home = QPushButton()
        self._btn_back = QPushButton()
        self._btn_lang = QPushButton()
        self._btn_lang.setObjectName("lang")
        self._btn_lang.setFixedWidth(56)
        self._btn_close = QPushButton("×")
        self._btn_close.setObjectName("close")
        self._btn_close.setFixedWidth(40)

        for b in (self._btn_home, self._btn_back, self._btn_lang, self._btn_close):
            b.setCursor(Qt.CursorShape.PointingHandCursor)

        self._search = QLineEdit()
        self._search.setMinimumHeight(32)
        self._search.setClearButtonEnabled(True)

        tl.addWidget(self._btn_home)
        tl.addWidget(self._btn_back)
        tl.addWidget(self._search, stretch=1)
        tl.addWidget(self._btn_lang)
        tl.addWidget(self._btn_close)
        main_layout.addWidget(top_bar)

        # ============ Cuerpo ============
        body = QHBoxLayout()
        body.setSpacing(14)

        # --- Sidebar (categorías con scroll) ---
        sidebar = FrostedPanel(bg, tint=QColor(8, 14, 28, 125), margins=(12, 14, 8, 12))
        sidebar.setFixedWidth(300)
        sl = sidebar.content_layout()

        self._sidebar_title = QLabel()
        self._sidebar_title.setStyleSheet(
            f"color: {ACCENT}; font-size: 15pt; font-weight: bold; "
            "background: transparent; padding-left: 4px;"
        )
        sl.addWidget(self._sidebar_title)

        sb_scroll = QScrollArea()
        sb_scroll.setWidgetResizable(True)
        sb_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        sb_scroll.setFrameShape(QFrame.Shape.NoFrame)
        sb_scroll.setStyleSheet(SCROLL_QSS)
        sb_scroll.viewport().setAutoFillBackground(False)
        sb_inner = QWidget()
        sb_inner.setAutoFillBackground(False)
        self._sb_layout = QVBoxLayout(sb_inner)
        self._sb_layout.setContentsMargins(0, 0, 4, 0)
        self._sb_layout.setSpacing(2)
        sb_scroll.setWidget(sb_inner)
        sl.addWidget(sb_scroll, stretch=1)

        # --- Panel de detalle (con scroll) ---
        detail = FrostedPanel(bg, tint=QColor(8, 14, 28, 110), margins=(10, 10, 6, 10))
        dl = detail.content_layout()

        self._detail_scroll = QScrollArea()
        self._detail_scroll.setWidgetResizable(True)
        self._detail_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._detail_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._detail_scroll.setStyleSheet(SCROLL_QSS)
        self._detail_scroll.viewport().setAutoFillBackground(False)
        d_inner = QWidget()
        d_inner.setAutoFillBackground(False)
        self._dl = QVBoxLayout(d_inner)
        self._dl.setContentsMargins(26, 20, 22, 20)
        self._dl.setSpacing(10)
        self._detail_scroll.setWidget(d_inner)
        dl.addWidget(self._detail_scroll)

        body.addWidget(sidebar)
        body.addWidget(detail, stretch=1)
        body.addSpacing(FREE_RIGHT_COLUMN)
        main_layout.addLayout(body, stretch=1)

        grip = QSizeGrip(self)
        grip.setStyleSheet("background: transparent;")
        main_layout.addWidget(grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)

        self._apply_styles()

        # ============ Conexiones ============
        self._btn_close.clicked.connect(self.close)
        self._btn_home.clicked.connect(lambda _=False: self._go(("home",)))
        self._btn_back.clicked.connect(lambda _=False: self._back())
        self._btn_lang.clicked.connect(lambda _=False: self._next_lang())

        self._search_timer = QTimer(self)
        self._search_timer.setSingleShot(True)
        self._search_timer.setInterval(250)
        self._search_timer.timeout.connect(self._run_search)
        self._search.textChanged.connect(lambda _t: self._search_timer.start())

        self._retranslate()
        self._build_sidebar()
        self._go(("home",))

    # ---------- Idioma ----------

    def _default_lang(self):
        for lang in Lang:
            if str(lang.value).lower().startswith("es"):
                return lang
        return next(iter(Lang))

    def _code(self) -> str:
        code = str(self._lang.value).lower()[:2]
        return code if code in STRINGS else "es"

    def _tr(self, key: str) -> str:
        return STRINGS[self._code()].get(key, key)

    def _next_lang(self) -> None:
        idx = self._langs.index(self._lang)
        self._lang = self._langs[(idx + 1) % len(self._langs)]
        self._retranslate()
        self._build_sidebar()
        if self._state:
            self._render(self._state)

    def _retranslate(self) -> None:
        self._btn_home.setText(self._tr("home"))
        self._btn_back.setText(self._tr("back"))
        self._btn_lang.setText(str(self._lang.value).upper()[:3])
        self._search.setPlaceholderText(self._tr("search"))
        self._sidebar_title.setText(self._tr("categories"))

    # ---------- Sidebar ----------

    @staticmethod
    def _clear_layout(layout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def _build_sidebar(self) -> None:
        self._clear_layout(self._sb_layout)
        self._anims.clear()
        lang = self._lang

        for cat in navigation.get_all_categories():
            name = _safe(lambda c=cat: i18n.t_category_name(c.id, lang), str(cat.id))
            subs = _safe(lambda c=cat: navigation.get_subcategories(c.id), [])

            btn = QPushButton(f"▸  {name}")
            btn.setObjectName("cat")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            box = QWidget()
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(0, 0, 0, 0)
            box_layout.setSpacing(0)
            for info in subs:
                sid = info.subcategory.id
                sname = _safe(
                    lambda c=cat, s=sid: i18n.t_subcategory_name(c.id, s, lang), str(sid)
                )
                sbtn = QPushButton(sname)
                sbtn.setObjectName("subitem")
                sbtn.setCursor(Qt.CursorShape.PointingHandCursor)
                sbtn.clicked.connect(
                    lambda _=False, c=cat.id, s=sid: self._go(("sub", c, s))
                )
                box_layout.addWidget(sbtn)
            box.setMaximumHeight(0)
            box.setProperty("open", False)

            btn.clicked.connect(
                lambda _=False, b=btn, bx=box, c=cat.id, n=name, has=bool(subs):
                self._on_category(b, bx, c, n, has)
            )
            self._sb_layout.addWidget(btn)
            self._sb_layout.addWidget(box)

        self._sb_layout.addStretch()

    def _on_category(self, btn, box, cat_id, name, has_subs) -> None:
        if has_subs:
            opening = not box.property("open")
            box.setProperty("open", opening)
            btn.setText(("▾" if opening else "▸") + f"  {name}")
            target = box.layout().sizeHint().height() if opening else 0
            anim = QPropertyAnimation(box, b"maximumHeight", self)
            anim.setDuration(230)
            anim.setStartValue(box.maximumHeight())
            anim.setEndValue(target)
            anim.setEasingCurve(QEasingCurve.Type.OutCubic)
            anim.start()
            self._anims[id(box)] = anim
        self._go(("cat", cat_id))

    # ---------- Navegación e historial ----------

    def _go(self, state: tuple, push: bool = True) -> None:
        if push and self._state is not None and state != self._state:
            self._history.append(self._state)
        self._state = state
        self._btn_back.setEnabled(bool(self._history))
        self._render(state)

    def _back(self) -> None:
        if self._history:
            state = self._history.pop()
            self._go(state, push=False)

    # ---------- Búsqueda ----------

    def _run_search(self) -> None:
        query = self._search.text().strip()
        in_search = bool(self._state) and self._state[0] == "search"
        if not query:
            if in_search:
                self._go(("home",), push=False)
            return
        self._go(("search", query), push=not in_search)

    # ---------- Renderizado del panel de detalle ----------

    def _render(self, state: tuple) -> None:
        self._clear_layout(self._dl)
        try:
            kind = state[0]
            if kind == "home":
                self._view_home()
            elif kind == "cat":
                self._view_category(state[1])
            elif kind == "sub":
                self._view_subcategory(state[1], state[2])
            elif kind == "cmd":
                self._view_command(state[1])
            elif kind == "search":
                self._view_search(state[1])
        except Exception:
            self._clear_layout(self._dl)
            self._add_title(self._tr("error"))
            self._add_text(traceback.format_exc(), mono=True, color="#ff9a8a")
            traceback.print_exc()
        self._dl.addStretch()
        self._detail_scroll.verticalScrollBar().setValue(0)

    # ---------- Piezas reutilizables del detalle ----------

    def _add_title(self, text: str, sub: str | None = None) -> None:
        title = QLabel(text.upper())
        font = QFont("DejaVu Sans", 19)
        font.setWeight(QFont.Weight.Light)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 4)
        title.setFont(font)
        title.setWordWrap(True)
        title.setStyleSheet("color: #f6eee2; background: transparent;")
        self._dl.addWidget(title)

        line = QFrame()
        line.setFixedSize(220, 2)
        line.setStyleSheet(
            "border: none; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(255,176,112,230), stop:1 rgba(255,176,112,0));"
        )
        self._dl.addWidget(line)

        if sub:
            self._add_text(sub, color="#d9e1ee", size="11pt")

    def _add_text(self, text: str, mono: bool = False, color: str = "#c9d4e6", size: str = "10.5pt") -> QLabel:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        if mono:
            style = (
                f"color: {color}; font-size: 10pt; font-family: 'DejaVu Sans Mono', monospace; "
                "background: rgba(0,0,0,110); border-radius: 8px; padding: 10px;"
            )
        else:
            style = f"color: {color}; font-size: {size}; background: transparent;"
        label.setStyleSheet(style)
        self._dl.addWidget(label)
        return label

    def _add_header(self, label: str) -> None:
        head = QLabel(label.upper())
        head_font = QFont("DejaVu Sans", 9)
        head_font.setBold(True)
        head_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        head.setFont(head_font)
        head.setStyleSheet(f"color: {ACCENT}; background: transparent; margin-top: 8px;")
        self._dl.addWidget(head)

    def _add_box(self, text: str, color: str) -> None:
        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        label.setStyleSheet(
            "color: #f3e9e4; font-size: 10.5pt; background: rgba(0,0,0,90); "
            f"border-left: 3px solid {color}; border-radius: 6px; padding: 10px 12px;"
        )
        self._dl.addWidget(label)

    @staticmethod
    def _badge(text: str, bg: str, dark: bool) -> QLabel:
        label = QLabel(text)
        fg = "#0a0a0a" if dark else "#e6edf8"
        label.setStyleSheet(
            f"color: {fg}; background: {bg}; border-radius: 9px; "
            "padding: 3px 11px; font-size: 9pt; font-weight: bold;"
        )
        return label

    def _add_command_buttons(self, commands) -> None:
        lang = self._lang
        for cmd in commands:
            cid = str(getattr(cmd, "id", ""))
            tc = _safe(lambda c=cmd: i18n.t_command(c, lang), cmd)
            desc = getattr(tc, "description", None) or getattr(cmd, "description", "") or ""
            desc = str(desc).replace("\n", " ")
            text = f"{cid}   —   {desc}" if desc else cid
            if len(text) > 110:
                text = text[:107] + "…"
            btn = QPushButton(text)
            btn.setObjectName("item")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            color = RISK_COLORS.get(getattr(cmd, "risk", None))
            if color:
                btn.setStyleSheet(f"QPushButton#item {{ border-left: 3px solid {color}; }}")
            btn.clicked.connect(lambda _=False, i=cid: self._go(("cmd", i)))
            self._dl.addWidget(btn)

    # ---------- Vistas ----------

    def _view_home(self) -> None:
        count = len(navigation.get_all_categories())
        self._add_title("Linux Command Master", self._tr("welcome_sub"))
        self._dl.addSpacing(14)
        self._add_text(f"{count} {self._tr('categories').lower()}\n\n{self._tr('welcome_info')}")

    def _view_category(self, cat_id: str) -> None:
        lang = self._lang
        name = _safe(lambda: i18n.t_category_name(cat_id, lang), str(cat_id))
        desc = _safe(lambda: i18n.t_category_description(cat_id, lang), "")
        commands = _safe(lambda: navigation.get_commands(cat_id), [])
        self._add_title(name, desc or None)
        self._dl.addSpacing(8)
        if commands:
            self._add_text(f"{len(commands)} {self._tr('commands')}", color="#9fb0c8", size="9.5pt")
            self._add_command_buttons(commands)
        else:
            self._add_text(self._tr("no_commands"))

    def _view_subcategory(self, cat_id: str, sub_id: str) -> None:
        lang = self._lang
        name = _safe(lambda: i18n.t_subcategory_name(cat_id, sub_id, lang), str(sub_id))
        cat_name = _safe(lambda: i18n.t_category_name(cat_id, lang), str(cat_id))
        commands = _safe(lambda: navigation.get_commands(cat_id, sub_id), [])
        self._add_title(name, cat_name)
        self._dl.addSpacing(8)
        if commands:
            self._add_text(f"{len(commands)} {self._tr('commands')}", color="#9fb0c8", size="9.5pt")
            self._add_command_buttons(commands)
        else:
            self._add_text(self._tr("no_commands"))

    def _view_search(self, query: str) -> None:
        results = search.search(query, limit=30)
        commands = []
        for r in results:
            cmd = getattr(r, "command", None)
            if cmd is None:
                cid = getattr(r, "command_id", None) or getattr(r, "id", None)
                cmd = search.get_command(cid) if cid else r
            commands.append(cmd)
        self._add_title(f"{self._tr('results_for')} “{query}”")
        self._dl.addSpacing(8)
        if commands:
            self._add_command_buttons(commands)
        else:
            self._add_text(self._tr("no_results"))

    def _view_command(self, command_id: str) -> None:
        lang = self._lang
        cmd = search.get_command(command_id)
        if cmd is None:
            self._add_title(str(command_id), self._tr("no_results"))
            return

        tc = _safe(lambda: i18n.t_command(cmd, lang), cmd)

        def val(name):
            v = getattr(tc, name, None)
            return v if not _empty(v) else getattr(cmd, name, None)

        # --- Título e insignias (riesgo, nivel, obsoleto) ---
        self._add_title(str(val("name") or cmd.id))

        risk_color = RISK_COLORS.get(cmd.risk, "#cccccc")
        risk_text = _safe(lambda: i18n.t_risk(cmd.risk, lang), str(cmd.risk.value))
        level_text = _safe(lambda: i18n.t_level(cmd.level, lang), str(cmd.level.value))

        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 4, 0, 4)
        row_layout.setSpacing(8)
        row_layout.addWidget(self._badge(risk_text, risk_color, dark=True))
        row_layout.addWidget(self._badge(level_text, "rgba(255,255,255,40)", dark=False))
        if cmd.deprecated:
            row_layout.addWidget(self._badge(self._tr("deprecated"), "#ff6b5e", dark=True))
        row_layout.addStretch()
        self._dl.addWidget(row)

        # --- Descripción y sintaxis ---
        description = val("description")
        if description:
            self._add_text(str(description), color="#e0e8f5", size="11pt")

        syntax = val("syntax")
        if syntax:
            self._add_header(self._tr("syntax"))
            self._add_text(str(syntax), mono=True)

        # --- Ejemplos (un bloque por ejemplo) ---
        examples = val("examples")
        if examples:
            self._add_header(self._tr("examples"))
            for example in examples:
                self._add_text(str(example), mono=True)

        # --- Cuándo usarlo ---
        when = val("when_to_use")
        if when:
            self._add_header(self._tr("when_to_use"))
            self._add_text(str(when))

        # --- Opciones importantes ---
        options = val("options")
        if options:
            self._add_header(self._tr("options"))
            self._add_text("\n".join(str(o) for o in options), mono=True)

        # --- Precauciones (recuadro con el color del riesgo) ---
        precautions = val("precautions")
        if precautions:
            self._add_header(self._tr("precautions"))
            self._add_box(str(precautions), risk_color)

        # --- Reemplaza a / Reemplazado por ---
        if cmd.replaces:
            self._add_header(self._tr("replaces"))
            self._add_text(str(cmd.replaces), mono=True)
        if cmd.replaced_by:
            self._add_header(self._tr("replaced_by"))
            target = str(cmd.replaced_by)
            if search.get_command(target) is not None:
                btn = QPushButton(target)
                btn.setObjectName("item")
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _=False, i=target: self._go(("cmd", i)))
                self._dl.addWidget(btn)
            else:
                self._add_text(target, mono=True)

        # --- Comandos relacionados ---
        related = [r for r in (cmd.related or []) if search.get_command(str(r)) is not None]
        if related:
            self._add_header(self._tr("related"))
            for rid in related:
                rid = str(rid)
                btn = QPushButton(rid)
                btn.setObjectName("item")
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _=False, i=rid: self._go(("cmd", i)))
                self._dl.addWidget(btn)

        # --- Etiquetas como píldoras ---
        tags = val("tags")
        if tags:
            self._dl.addSpacing(6)
            tag_row = QWidget()
            tag_layout = QHBoxLayout(tag_row)
            tag_layout.setContentsMargins(0, 0, 0, 0)
            tag_layout.setSpacing(6)
            for tag in tags:
                text = _safe(lambda t=tag: i18n.t_tag(t, lang), str(tag))
                chip = QLabel(f"#{text}")
                chip.setStyleSheet(
                    "color: #c9d4e6; background: rgba(255,255,255,22); "
                    "border-radius: 9px; padding: 2px 9px; font-size: 9pt;"
                )
                tag_layout.addWidget(chip)
            tag_layout.addStretch()
            self._dl.addWidget(tag_row)

    # ---------- Estilos y ventana sin marco ----------

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(77, 157, 255, 240);
                color: #0a0a0a;
                border: none;
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 10pt;
                font-weight: bold;
                min-height: 22px;
            }
            QPushButton:hover { background-color: rgba(111, 179, 255, 255); }
            QPushButton:pressed { background-color: rgba(50, 120, 220, 255); }
            QPushButton:disabled { background-color: rgba(77, 157, 255, 80); color: rgba(10,10,10,110); }
            QPushButton#close { font-size: 14pt; padding: 2px 0; }
            QPushButton#lang { padding: 8px 0; }
            QPushButton#cat {
                background-color: transparent;
                color: #ffffff;
                text-align: left;
                padding: 7px 10px;
                font-size: 10pt;
                font-weight: normal;
                border-radius: 6px;
                min-height: 18px;
            }
            QPushButton#cat:hover { background-color: rgba(255, 255, 255, 30); }
            QPushButton#cat:pressed { background-color: rgba(255, 176, 112, 60); }
            QPushButton#subitem {
                background-color: transparent;
                color: #d9e1ee;
                text-align: left;
                padding: 5px 10px 5px 28px;
                font-size: 9.5pt;
                font-weight: normal;
                border-radius: 6px;
                min-height: 16px;
            }
            QPushButton#subitem:hover { background-color: rgba(255, 255, 255, 28); color: #ffffff; }
            QPushButton#item {
                background-color: rgba(255, 255, 255, 14);
                color: #ffffff;
                text-align: left;
                padding: 10px 14px;
                font-size: 10pt;
                font-weight: normal;
                border-radius: 8px;
                min-height: 18px;
            }
            QPushButton#item:hover { background-color: rgba(255, 255, 255, 36); }
            QLineEdit {
                background-color: rgba(5, 10, 20, 220);
                color: #ffffff;
                border: 1px solid rgba(255, 255, 255, 45);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 10pt;
                selection-background-color: rgba(255, 176, 112, 150);
            }
            """
        )

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event) -> None:
        if self._old_pos is not None:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.pos() + delta)
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event) -> None:
        self._old_pos = None


def main() -> None:
    # Evita que una excepción dentro de un slot aborte toda la aplicación
    sys.excepthook = lambda *args: traceback.print_exception(*args)

    app = QApplication(sys.argv)
    app.setFont(QFont("DejaVu Sans", 10))
    window = MainWindow()

    window.setWindowOpacity(0.0)
    window.show()
    fade = QPropertyAnimation(window, b"windowOpacity")
    fade.setDuration(900)
    fade.setStartValue(0.0)
    fade.setEndValue(1.0)
    fade.setEasingCurve(QEasingCurve.Type.OutCubic)
    fade.start()
    window._fade = fade

    sys.exit(app.exec())


if __name__ == "__main__":
    main()