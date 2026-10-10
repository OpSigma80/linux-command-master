"""
Interfaz PyQt6 (Proof of Concept v4) — reemplazo de la GUI Tkinter.

Vidrio esmerilado real sin QGraphicsEffect: el fondo se desenfoca una vez
con Pillow y cada panel pinta el trozo borroso que tiene debajo, con un
tinte translúcido encima. El texto se dibuja nítido.

v4: imagen espejada para que el pingüino quede a la derecha, columna libre
a la derecha para verlo, paneles más translúcidos y degradado oscuro a la
izquierda para legibilidad.

Estado: Proof of Concept. NO integra todavía con app/core.
"""

import sys
from pathlib import Path

from PIL import Image, ImageFilter, ImageOps
from PyQt6.QtCore import QPoint, QRectF, Qt
from PyQt6.QtGui import (
    QColor,
    QFont,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


ASSETS = Path(__file__).parent / "assets"
BACKGROUND_PATH = ASSETS / "background.jpg"

# --- Ajustes rápidos de diseño ---
MIRROR_BACKGROUND = True   # True: el pingüino pasa de la izquierda a la derecha
BLUR_RADIUS = 10           # menos = fondo más reconocible
FREE_RIGHT_COLUMN = 260    # px libres a la derecha para ver el pingüino
LEFT_DARKEN_ALPHA = 150    # 0-255, oscurece el lado izquierdo (legibilidad)


def _cover(img: Image.Image, w: int, h: int) -> Image.Image:
    """Escala y recorta la imagen para cubrir w x h (como background-size: cover)."""
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


class BackgroundWidget(QWidget):
    """Dibuja el fondo nítido y guarda una versión desenfocada para los paneles."""

    def __init__(
        self,
        image_path: Path,
        blur_radius: int = 10,
        mirror: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        if Path(image_path).exists():
            src = Image.open(image_path).convert("RGB")
        else:
            src = Image.new("RGB", (16, 16), (8, 8, 16))
        self._src = ImageOps.mirror(src) if mirror else src
        self._blur_radius = blur_radius
        self._sharp = QPixmap()
        self._blurred = QPixmap()

    def resizeEvent(self, event) -> None:
        w, h = max(1, self.width()), max(1, self.height())
        base = _cover(self._src, w, h)
        self._sharp = _to_pixmap(base)

        # Se desenfoca a 1/4 de tamaño (mucho más rápido) y se reescala suave.
        small = base.resize((max(1, w // 4), max(1, h // 4)), Image.LANCZOS)
        small = small.filter(ImageFilter.GaussianBlur(max(1, self._blur_radius // 4)))
        self._blurred = _to_pixmap(small).scaled(
            w,
            h,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        for panel in self.findChildren(FrostedPanel):
            panel.update()
        super().resizeEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._sharp)

        # Degradado oscuro: fuerte a la izquierda, transparente hacia la derecha.
        grad = QLinearGradient(0, 0, self.width(), 0)
        grad.setColorAt(0.0, QColor(4, 6, 14, LEFT_DARKEN_ALPHA))
        grad.setColorAt(0.65, QColor(4, 6, 14, 0))
        painter.fillRect(self.rect(), grad)

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

        painter.setPen(QPen(QColor(80, 130, 200, 110), 1))
        painter.drawPath(path)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Linux Command Master — PyQt6 PoC v4")
        self.resize(1100, 680)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)

        self._old_pos: QPoint | None = None

        bg = BackgroundWidget(
            BACKGROUND_PATH, blur_radius=BLUR_RADIUS, mirror=MIRROR_BACKGROUND
        )
        self.setCentralWidget(bg)

        main_layout = QVBoxLayout(bg)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # ============ Barra superior ============
        top_bar = FrostedPanel(
            bg,
            tint=QColor(8, 14, 28, 150),
            radius=10,
            margins=(14, 8, 14, 8),
            horizontal=True,
        )
        top_bar.setFixedHeight(56)
        tl = top_bar.content_layout()

        self._btn_inicio = QPushButton("Inicio")
        self._btn_atras = QPushButton("← Atrás")
        self._btn_close = QPushButton("✕")
        self._btn_close.setFixedWidth(40)
        self._btn_close.clicked.connect(self.close)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Buscar comando (ej: docker, grep, permisos)...")
        self._search.setMinimumHeight(32)

        tl.addWidget(self._btn_inicio)
        tl.addWidget(self._btn_atras)
        tl.addWidget(self._search, stretch=1)
        tl.addWidget(self._btn_close)

        main_layout.addWidget(top_bar)

        # ============ Cuerpo ============
        body_layout = QHBoxLayout()
        body_layout.setSpacing(14)

        # --- Sidebar ---
        sidebar = FrostedPanel(bg, tint=QColor(8, 14, 28, 125))
        sidebar.setFixedWidth(300)
        sl = sidebar.content_layout()

        sidebar_title = QLabel("Categorías")
        sidebar_title.setStyleSheet(
            "color: #6fb3ff; font-size: 15pt; font-weight: bold; background: transparent;"
        )
        sl.addWidget(sidebar_title)
        sl.addSpacing(6)

        for cat in [
            "Navegación y Gestión de Archivos",
            "Lectura y Manipulación de Texto",
            "Búsqueda",
            "Permisos, Usuarios e Identidad",
            "Procesos y Rendimiento",
            "Redes",
            "Compresión y Archivos",
            "Información del Sistema",
        ]:
            item = QLabel(f"▸  {cat}")
            item.setStyleSheet(
                "color: #ffffff; font-size: 10pt; padding: 4px 2px; background: transparent;"
            )
            sl.addWidget(item)

        sl.addStretch()

        # --- Panel de detalle ---
        detail = FrostedPanel(bg, tint=QColor(8, 14, 28, 110), margins=(32, 28, 32, 28))
        dl = detail.content_layout()
        dl.setSpacing(10)

        title = QLabel("Linux Command Master")
        title.setStyleSheet(
            "color: #ffffff; font-size: 30pt; font-weight: bold; background: transparent;"
        )

        subtitle = QLabel(
            "Selecciona una categoría en el panel izquierdo o busca un comando arriba."
        )
        subtitle.setStyleSheet("color: #e0e8f5; font-size: 12pt; background: transparent;")
        subtitle.setWordWrap(True)

        dl.addWidget(title)
        dl.addWidget(subtitle)
        dl.addSpacing(24)

        info = QLabel(
            "Proof of Concept de PyQt6\n\n"
            "•  Paneles de cristal esmerilado (fondo desenfocado con Pillow)\n"
            "•  Sin QGraphicsEffect: texto siempre nítido\n"
            "•  Bordes redondeados\n"
            "•  Fondo de aurora visible detrás de todo"
        )
        info.setStyleSheet("color: #d0dcf0; font-size: 11pt; background: transparent;")
        info.setWordWrap(True)

        dl.addWidget(info)
        dl.addStretch()

        body_layout.addWidget(sidebar)
        body_layout.addWidget(detail, stretch=1)
        body_layout.addSpacing(FREE_RIGHT_COLUMN)  # zona libre: se ve el pingüino
        main_layout.addLayout(body_layout, stretch=1)

        self._apply_styles()

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
            QLineEdit {
                background-color: rgba(5, 10, 20, 220);
                color: #ffffff;
                border: 1px solid rgba(80, 130, 200, 140);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 10pt;
                selection-background-color: rgba(77, 157, 255, 180);
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
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()