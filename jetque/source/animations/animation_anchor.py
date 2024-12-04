# jetque/source/animations/animation_anchor.py

from typing import Optional

from PyQt6.QtCore import QRectF, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QStyleOptionGraphicsItem,
    QWidget
)

from jetque.source.animations.animation_anchor_circle import AnimationAnchorCircle
from jetque.source.animations.animation_anchor_text import AnimationAnchorText


class AnimationAnchor(QGraphicsObject):
    """Composite graphics object representing an animation anchor with start and end points."""

    positionChanged = pyqtSignal()

    def __init__(
            self, group_name: str, parent: Optional[QGraphicsItem] = None
    ) -> None:
        """Initialize an AnimationAnchor with start and end circles and texts.

        Args:
            group_name (str): The name of the group for labeling.
            parent (Optional[QGraphicsItem], optional): Parent graphics item. Defaults to None.
        """
        super().__init__(parent)
        self.group_name: str = group_name
        self.start_circle: AnimationAnchorCircle = AnimationAnchorCircle()
        self.end_circle: AnimationAnchorCircle = AnimationAnchorCircle()
        self.start_text: AnimationAnchorText = AnimationAnchorText(group_name, is_start=True, parent=self.start_circle)
        self.end_text: AnimationAnchorText = AnimationAnchorText(group_name, is_start=False, parent=self.end_circle)

        self.start_circle.setParentItem(self)
        self.end_circle.setParentItem(self)
        self.start_circle.setPos(0, 0)
        self.end_circle.setPos(200, 0)
        self.start_text.setPos(0, -30)
        self.end_text.setPos(0, -30)

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
        start_rect = self.start_circle.mapToParent(
            self.start_circle.boundingRect()
        ).boundingRect()
        end_rect = self.end_circle.mapToParent(
            self.end_circle.boundingRect()
        ).boundingRect()
        return start_rect.united(end_rect)

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
