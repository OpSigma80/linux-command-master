"""
Interfaz PyQt6 (Proof of Concept v2) — reemplazo de la GUI Tkinter.

Objetivo: transparencia REAL de paneles con blur sobre el fondo de aurora,
imitando la estética de proyectos como "whydied".

Fix v2: el QGraphicsBlurEffect se aplica SOLO al fondo de los paneles
(un QFrame hijo), no al contenido. Así el texto y botones quedan nítidos
mientras el fondo detrás se ve difuminado (efecto vidrio esmerilado real).

Estado: Proof of Concept. NO integra todavía con app/core.
"""

import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPixmap, QColor, QPainter, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QGraphicsBlurEffect,
    QGraphicsDropShadowEffect,
    QFrame,
)


ASSETS = Path(__file__).parent / "assets"
BACKGROUND_PATH = ASSETS / "background.jpg"


class FrostedPanel(QFrame):
    """Panel con efecto 'vidrio esmerilado' real.

    Estructura:
        FrostedPanel (QFrame)
          └─ _blur_layer (QFrame)  ← fondo con rgba + blur, detrás de todo
          └─ _content (QWidget)     ← contenido NÍTIDO, encima del blur

    El blur SOLO se aplica al _blur_layer, nunca al contenido.
    """

    def __init__(
        self,
        parent=None,
        opacity: float = 0.55,
        radius: int = 12,
        border_alpha: int = 100,
        blur_radius: int = 15,
    ):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # --- Capa de fondo con blur ---
        self._blur_layer = QFrame(self)
        self._blur_layer.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        alpha = int(opacity * 255)
        self._blur_layer.setStyleSheet(
            f"""
            background-color: rgba(10, 15, 30, {alpha});
            border: 1px solid rgba(80, 130, 200, {border_alpha});
            border-radius: {radius}px;
            """
        )
        # El blur se aplica SOLO a esta capa de fondo
        blur = QGraphicsBlurEffect()
        blur.setBlurRadius(blur_radius)
        blur.setBlurHints(QGraphicsBlurEffect.BlurHint.QualityHint)
        self._blur_layer.setGraphicsEffect(blur)

        # --- Capa de contenido (nítida) ---
        self._content = QWidget(self)
        self._content.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(16, 14, 16, 14)
        self._content_layout.setSpacing(6)

    def content_layout(self) -> QVBoxLayout:
        return self._content_layout

    def set_content_layout(self, layout) -> None:
        self._content_layout = layout

    def resizeEvent(self, event) -> None:
        """Mantiene la capa de blur cubriendo el panel entero y el contenido
        encima con márgenes cómodos."""
        super().resizeEvent(event)
        self._blur_layer.setGeometry(0, 0, self.width(), self.height())
        self._content.setGeometry(0, 0, self.width(), self.height())


def add_text_shadow(widget: QWidget, blur: int = 6, offset: int = 2):
    """Añade sombra negra a un widget de texto para legibilidad universal."""
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setColor(QColor(0, 0, 0, 220))
    effect.setOffset(offset, offset)
    widget.setGraphicsEffect(effect)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Linux Command Master — PyQt6 PoC v2")
        self.resize(1100, 680)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        self._bg_pixmap = QPixmap(str(BACKGROUND_PATH))
        self._old_pos: QPoint | None = None

        central = QWidget(self)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        # ============ Barra superior ============
        top_bar = QFrame(central)
        top_bar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        top_bar.setFixedHeight(56)

        top_bar_bg = QFrame(top_bar)
        top_bar_bg.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        top_bar_bg.setStyleSheet(
            """
            background-color: rgba(10, 15, 30, 200);
            border: 1px solid rgba(80, 130, 200, 120);
            border-radius: 10px;
            """
        )
        top_bar_blur = QGraphicsBlurEffect()
        top_bar_blur.setBlurRadius(12)
        top_bar_bg.setGraphicsEffect(top_bar_blur)

        top_bar_content = QWidget(top_bar)
        top_bar_content.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground, True
        )
        top_layout = QHBoxLayout(top_bar_content)
        top_layout.setContentsMargins(14, 8, 14, 8)
        top_layout.setSpacing(8)

        self._btn_inicio = QPushButton("Inicio")
        self._btn_atras = QPushButton("← Atrás")
        self._btn_close = QPushButton("✕")
        self._btn_close.setFixedWidth(40)
        self._btn_close.clicked.connect(self.close)

        self._search = QLineEdit()
        self._search.setPlaceholderText(
            "Buscar comando (ej: docker, grep, permisos)..."
        )
        self._search.setMinimumHeight(32)

        top_layout.addWidget(self._btn_inicio)
        top_layout.addWidget(self._btn_atras)
        top_layout.addWidget(self._search, stretch=1)
        top_layout.addWidget(self._btn_close)

        # Guardar referencias para resize
        top_bar._bg = top_bar_bg
        top_bar._content = top_bar_content
        top_bar.resizeEvent = lambda e: (
            top_bar_bg.setGeometry(0, 0, top_bar.width(), top_bar.height()),
            top_bar_content.setGeometry(0, 0, top_bar.width(), top_bar.height()),
        )

        self._style_inputs(top_bar)

        main_layout.addWidget(top_bar)

        # ============ Cuerpo ============
        body_layout = QHBoxLayout()
        body_layout.setSpacing(14)

        # --- Sidebar ---
        sidebar = FrostedPanel(opacity=0.55, radius=12, blur_radius=15)
        sidebar.setFixedWidth(320)
        sl = sidebar.content_layout()

        sidebar_title = QLabel("Categorías")
        sidebar_title.setStyleSheet(
            "color: #4d9dff; font-size: 15pt; font-weight: bold; "
            "background: transparent;"
        )
        add_text_shadow(sidebar_title, blur=8, offset=2)
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
                "color: #ffffff; font-size: 10pt; "
                "padding: 4px 2px; background: transparent;"
            )
            add_text_shadow(item, blur=5, offset=1)
            sl.addWidget(item)

        sl.addStretch()

        # --- Panel de detalle ---
        detail = FrostedPanel(opacity=0.50, radius=12, blur_radius=18)

        dl = detail.content_layout()
        dl.setContentsMargins(32, 28, 32, 28)
        dl.setSpacing(10)

        title = QLabel("Linux Command Master")
        title.setStyleSheet(
            "color: #ffffff; font-size: 30pt; font-weight: bold; "
            "background: transparent;"
        )
        add_text_shadow(title, blur=12, offset=3)

        subtitle = QLabel(
            "Selecciona una categoría en el panel izquierdo "
            "o busca un comando arriba."
        )
        subtitle.setStyleSheet(
            "color: #e0e8f5; font-size: 12pt; background: transparent;"
        )
        subtitle.setWordWrap(True)
        add_text_shadow(subtitle, blur=6, offset=1)

        dl.addWidget(title)
        dl.addWidget(subtitle)
        dl.addSpacing(24)

        info = QLabel(
            "🎨  Proof of Concept de PyQt6\n\n"
            "•  Paneles con transparencia REAL (rgba)\n"
            "•  Blur del fondo (vidrio esmerilado)\n"
            "•  Bordes redondeados nativos\n"
            "•  Fondo de aurora visible detrás de todo\n"
            "•  Texto con sombra para legibilidad universal\n"
            "•  Blur separado del contenido — texto nítido"
        )
        info.setStyleSheet(
            "color: #c8d4e8; font-size: 11pt; line-height: 170%; "
            "background: transparent;"
        )
        info.setWordWrap(True)
        add_text_shadow(info, blur=5, offset=1)

        dl.addWidget(info)
        dl.addStretch()

        body_layout.addWidget(sidebar)
        body_layout.addWidget(detail, stretch=1)

        main_layout.addLayout(body_layout, stretch=1)

    def _style_inputs(self, parent: QWidget) -> None:
        parent.setStyleSheet(
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
            QPushButton:hover {
                background-color: rgba(111, 179, 255, 255);
            }
            QPushButton:pressed {
                background-color: rgba(50, 120, 220, 255);
            }
            QLineEdit {
                background-color: rgba(5, 10, 20, 220);
                color: #ffffff;
                border: 1px solid rgba(80, 130, 200, 140);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 10pt;
                selection-background-color: rgba(77, 157, 255, 180);
            }
            QLineEdit::placeholder {
                color: #8899aa;
            }
            """
        )

    def paintEvent(self, event) -> None:
        """Dibuja la imagen de fondo (aurora) cubriendo toda la ventana."""
        painter = QPainter(self)
        if not self._bg_pixmap.isNull():
            scaled = self._bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = (scaled.width() - self.width()) // 2
            y = (scaled.height() - self.height()) // 2
            painter.drawPixmap(-x, -y, scaled)
        else:
            painter.fillRect(self.rect(), QColor("#080810"))

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
