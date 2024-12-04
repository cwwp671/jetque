# jetque/source/animations/animation_anchor_circle.py

from typing import Any, Optional

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QBrush, QPen, QPainter
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsSceneHoverEvent,
    QGraphicsSceneMouseEvent,
    QStyleOptionGraphicsItem,
    QWidget,
)


class AnimationAnchorCircle(QGraphicsObject):
    """Interactive circle item for animation anchors."""

    positionChanged = pyqtSignal()

    def __init__(
            self,
            x: float = 0.0,
            y: float = 0.0,
            width: float = 40.0,
            height: float = 40.0,
            parent: Optional[QGraphicsItem] = None,
    ) -> None:
        """Initialize the anchor circle.

        Args:
            x (float, optional): X position. Defaults to 0.0.
            y (float, optional): Y position. Defaults to 0.0.
            width (float, optional): Width of the circle. Defaults to 100.0.
            height (float, optional): Height of the circle. Defaults to 100.0.
            parent (Optional[QGraphicsItem], optional): Parent graphics item. Defaults to None.
        """
        super().__init__(parent)
        self.rect: QRectF = QRectF(x, y, width, height)

        fill_color: QColor = QColor(212, 17, 89, 255)  # Colorblind friendly 'Razzmatazz' / '#D41159'
        outline_color: QColor = QColor(26, 133, 255, 255)  # Colorblind friendly 'Dodger Blue' / '#1A85FF'

        self.fill_brush: QBrush = QBrush(fill_color)
        self.outline_pen: QPen = QPen(outline_color)
        self.outline_pen.setWidthF(2.0)

        self.extra = self.outline_pen.widthF() + (self.outline_pen.widthF() / 2.0)

        # Enable the item to be movable and selectable
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        # For better interaction
        self.setAcceptHoverEvents(True)

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the circle.

        Returns:
            QRectF: The bounding rectangle.
        """
        return self.rect.adjusted(-self.extra, -self.extra, self.extra, self.extra)

    def paint(
            self,
            painter: QPainter,
            option: QStyleOptionGraphicsItem,
            widget: Optional[QWidget] = None,
    ) -> None:
        """Paint the circle item.

        Args:
            painter (QPainter): The painter object.
            option (QStyleOptionGraphicsItem): Style options.
            widget (Optional[QWidget], optional): The widget being painted on. Defaults to None.
        """
        painter.setBrush(self.fill_brush)
        painter.setPen(self.outline_pen)
        painter.drawEllipse(self.rect)

    def itemChange(self, change: 'QGraphicsItem.GraphicsItemChange', value: Any) -> Any:
        """Handle item state changes.

        Args:
            change (QGraphicsItem.GraphicsItemChange): The type of change.
            value: The value associated with the change.

        Returns:
            Any: The result of the change.
        """
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            self.positionChanged.emit()
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handle hover enter events.

        Args:
            event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Handle hover leave events.

        Args:
            event (QGraphicsSceneHoverEvent): The hover event.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Handle mouse press events.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse event.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """Handle mouse release events.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse event.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().mouseReleaseEvent(event)
