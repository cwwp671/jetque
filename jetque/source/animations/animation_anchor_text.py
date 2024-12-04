# jetque/source/animations/animation_anchor_text.py
import logging
import re
from typing import Optional

from PyQt6.QtCore import QRectF, Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QColor, QTextCursor, QTextCharFormat, QFont
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget,
    QGraphicsScene
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
            | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        )

        # Initialize the single QGraphicsTextItem
        self.text_item: QGraphicsTextItem = QGraphicsTextItem(self)
        self.text_item.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        self.text_item.setDefaultTextColor(QColor("black"))
        self.text_item.setAcceptHoverEvents(True)

        # Set up the initial text with formatting
        self._update_text()

        # Connect the text change signal
        self.text_item.document().contentsChanged.connect(self._on_content_changed)

        # Track editing state
        self.is_editing = False

    def _update_text(self) -> None:
        """Construct and set the formatted text for the text_item."""
        position_label = 'Start' if self.is_start else 'End'
        # Retrieve current position
        if self.parent_item:
            x = int(self.parent_item.x())
            y = int(self.parent_item.y())
        else:
            x, y = 0, 0

        # Construct HTML formatted text with dynamic x and y
        formatted_text = (
            f"{self.group_name} {position_label} "
            f"<span style='color:red;'>[{x}, </span>"
            f"<span style='color:green;'>{y}]</span>"
        )
        self.text_item.setHtml(formatted_text)

        # Recalculate and adjust the bounding rectangle with padding
        bounding = self.text_item.document().size()
        self.prepareGeometryChange()
        self.text_item.setPos(-bounding.width() / 2.0, -bounding.height() / 2.0)
        self.update()

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle encompassing the text item with padding.

        Returns:
            QRectF: The bounding rectangle.
        """
        size = self.text_item.document().size()
        return QRectF(-size.width() / 2.0,
                      -size.height() / 2.0,
                      size.width(),
                      size.height())

    def paint(
            self,
            painter,
            option: QStyleOptionGraphicsItem,
            widget: Optional[QWidget] = None,
    ) -> None:
        """No painting required; child items handle their own painting."""
        pass

    def update_position(self) -> None:
        """Update the position text based on the parent item's position."""
        self._update_text()

    def _on_content_changed(self) -> None:
        """Handle content changes by marking the item as edited."""
        if not self.is_editing:
            # logging.debug("Content changed when not in edit mode (moving).")
            self.prepareGeometryChange()
            self.contentChanged.emit()

    def keyPressEvent(self, event) -> None:
        """Handle key press events to manage editing behavior."""
        logging.debug("AnimationAnchorText keyPressEvent")
        if self.is_editing:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                # Commit changes when Enter is pressed
                self._commit_edit()
                return
            elif event.key() == Qt.Key.Key_Escape:
                # Cancel editing on Escape
                self.is_editing = False
                self._update_text()
                self.text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
                self.text_item.clearFocus()
                return
            else:
                # Allow other keys to be processed normally
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def _commit_edit(self) -> None:
        """Commit the edit by validating and updating the position."""
        self.is_editing = False
        text = self.text_item.toPlainText()

        # Extract x and y using regex with dynamic digit handling
        # Pattern: "{Group Name} {Start|End} [x, y]"
        pattern = rf"^{re.escape(self.group_name)}\s+(Start|End)\s+\[\s*(-?\d+)\s*,\s*(-?\d+)\s*]$"
        match = re.match(pattern, text)
        if match:
            _, x_str, y_str = match.groups()
            try:
                x = int(x_str)
                y = int(y_str)

                # Validate against scene dimensions
                scene = self.scene()
                if scene:
                    scene_rect = scene.sceneRect()
                    scene_width = int(scene_rect.width())
                    scene_height = int(scene_rect.height())
                else:
                    scene_width = 1920  # Default width
                    scene_height = 1080  # Default height

                logging.debug("Edit confirmed, emitting content change.")

                if x <= scene_width and y <= scene_height:
                    self.prepareGeometryChange()
                    self.contentChanged.emit()
                else:
                    self._update_text()
            except ValueError:
                # Invalid number entered; revert to previous position
                self._update_text()
        else:
            # Invalid format entered; revert to previous position
            self._update_text()

        self.text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.text_item.clearFocus()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press to initiate editing."""
        logging.debug("AnimationAnchorText Mouse Event")
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_editing = True
            self.text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
            self.text_item.setFocus(Qt.FocusReason.MouseFocusReason)
            # self.text_item.setFocus()
            logging.debug(f"Left Click registered. is_editing={self.is_editing}")
        super().mousePressEvent(event)
