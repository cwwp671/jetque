# jetque/source/animations/animation_anchor_circle.py

from PyQt6.QtWidgets import QGraphicsObject
from PyQt6.QtGui import QBrush, QColor, QPen, QPainter
from PyQt6.QtCore import Qt, pyqtSignal, QRectF


class AnimationAnchorCircle(QGraphicsObject):
    positionChanged = pyqtSignal()

    def __init__(self, x=0.0, y=0.0, width=100.0, height=100.0, parent=None):
        super().__init__(parent)

        self.rect = QRectF(x, y, width, height)

        fill_color: QColor = QColor(212, 17, 89, 255)  # 'Razzmatazz' / '#D41159' for colorblind safety.
        outline_color: QColor = QColor(26, 133, 255, 255)  # 'Dodger Blue' / '#1A85FF' for colorblind safety.

        self.fill_brush = QBrush(fill_color)
        self.outline_pen = QPen(outline_color)

        # Enable the item to be movable and selectable
        self.setFlags(
            QGraphicsObject.GraphicsItemFlag.ItemIsMovable
            | QGraphicsObject.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges
        )

        # For better interaction
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return self.rect

    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(self.fill_brush)
        painter.setPen(self.outline_pen)
        painter.drawEllipse(self.rect)

    def itemChange(self, change, value):
        if change == QGraphicsObject.GraphicsItemChange.ItemPositionHasChanged:
            self.positionChanged.emit()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)
