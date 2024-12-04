# jetque/source/animations/animation_anchor_text.py

import re
from typing import Optional

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget
)


class AnimationAnchorText(QGraphicsObject):
    """Composite text item for displaying and editing position labels."""

    contentChanged = pyqtSignal()

    def __init__(
            self,
            group_name: str,
            is_start: bool = True,
            parent: Optional[QGraphicsItem] = None,
    ) -> None:
        """Initialize the anchor text item.

        Args:
            group_name (str): The name of the group.
            is_start (bool, optional): Flag indicating if this is a start or end point. Defaults to True.
            parent (Optional[QGraphicsItem], optional): Parent graphics item. Defaults to None.
        """
        super().__init__(parent)
        self.group_name: str = group_name
        self.is_start: bool = is_start
        self.parent_item: Optional[QGraphicsItem] = parent
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        position_label: str = 'Start' if self.is_start else 'End'
        text_font: QFont = QFont("Helvetica", 12, QFont.Weight.Bold, False)

        # Non-editable text item
        self.label_text_item: QGraphicsTextItem = QGraphicsTextItem(
            f"{self.group_name} {position_label}: ", self
        )
        self.label_text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.label_text_item.setFont(text_font)

        # Editable text item
        x = self.parent_item.x() if self.parent_item else 0
        y = self.parent_item.y() if self.parent_item else 0
        self.position_text_item: QGraphicsTextItem = QGraphicsTextItem(f"[{int(x)}, {int(y)}]", self)
        self.position_text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.position_text_item.setFont(text_font)

        # Connect the text change signal to the slot
        self.label_text_item.document().contentsChanged.connect(self._on_content_changed)
        self.position_text_item.document().contentsChanged.connect(self._on_position_text_changed)

        # Position the text items next to each other

        label_width = self.label_text_item.boundingRect().width()
        self.label_text_item.setPos(-(label_width / 2.0), 0)
        self.position_text_item.setPos(label_width - (label_width / 2.0), 0)

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle encompassing all child items.

        Returns:
            QRectF: The bounding rectangle.
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

    def update_position(self) -> None:
        """Update the position text based on the parent item's position."""
        if self.parent_item:
            self.prepareGeometryChange()
            x = self.parent_item.x()
            y = self.parent_item.y()
            self.position_text_item.setPlainText(f"[{int(x)}, {int(y)}]")

    def _on_content_changed(self) -> None:
        """Handle content changes by updating geometry."""
        self.prepareGeometryChange()
        self.contentChanged.emit()

    def _on_position_text_changed(self) -> None:
        """Handle changes in the position text and update the parent item's position."""
        self.prepareGeometryChange()
        text = self.position_text_item.toPlainText()
        match = re.match(r'\s*\[\s*([-\d.]+)\s*,\s*([-\d.]+)\s*]\s*', text)
        if match:
            x_str, y_str = match.groups()
            try:
                x = float(x_str)
                y = float(y_str)
                if self.parent_item:
                    self.parent_item.setPos(x, y)
            except ValueError:
                pass  # Invalid numbers entered
        else:
            pass  # Invalid format entered
