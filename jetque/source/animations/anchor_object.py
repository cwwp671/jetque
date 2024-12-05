# jetque/source/animations/anchor_object.py

from typing import Optional

from PyQt6.QtCore import QRectF, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QStyleOptionGraphicsItem,
    QWidget
)

from jetque.source.animations.anchor_circle_object import AnchorCircleObject
from jetque.source.animations.anchor_text_object import AnchorTextObject


class AnchorObject(QGraphicsObject):
    """Composite graphics object representing an animation anchor with start and end points."""

    positionChanged = pyqtSignal()

    def __init__(
            self, group_name: str, parent: Optional[QGraphicsItem] = None
    ) -> None:
        """Initialize an AnchorObject with start and end circles and texts.

        Args:
            group_name (str): The name of the group for labeling.
            parent (Optional[QGraphicsItem], optional): Parent graphics item. Defaults to None.
        """
        super().__init__(parent)
        self.group_name: str = group_name
        self.start_circle: AnchorCircleObject = AnchorCircleObject()
        self.end_circle: AnchorCircleObject = AnchorCircleObject()
        self.start_text: AnchorTextObject = AnchorTextObject(group_name, is_start=True, parent=self.start_circle)
        self.end_text: AnchorTextObject = AnchorTextObject(group_name, is_start=False, parent=self.end_circle)

        self.start_circle.setParentItem(self)
        self.end_circle.setParentItem(self)
        self.start_circle.setPos(0, 0)
        self.end_circle.setPos(200, 0)
        self.start_text.update_position()
        self.end_text.update_position()

        self.start_circle.positionChanged.connect(self.start_text.update_position)
        self.end_circle.positionChanged.connect(self.end_text.update_position)
        self.start_circle.positionChanged.connect(self._on_child_changed)
        self.end_circle.positionChanged.connect(self._on_child_changed)
        self.start_text.contentChanged.connect(self._on_child_changed)
        self.end_text.contentChanged.connect(self._on_child_changed)

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle of the composite item.

        Returns:
            QRectF: The bounding rectangle encompassing all child items.
        """
        return self.childrenBoundingRect()

    def paint(
            self,
            painter: QPainter,
            option: QStyleOptionGraphicsItem,
            widget: Optional[QWidget] = None,
    ) -> None:
        """No painting required; child items handle their own painting."""
        pass

    def _on_child_changed(self) -> None:
        """Emit positionChanged signal when a child item changes."""
        self.prepareGeometryChange()  # Notify the scene of geometry change
        self.positionChanged.emit()
