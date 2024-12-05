# jetque/source/animations/anchor_text_object.py

import logging
from typing import Optional

from PyQt6.QtCore import QRectF, pyqtSignal, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget
)

from jetque.source.animations.anchor_editable_text_item import AnchorEditableTextItem


class AnchorTextObject(QGraphicsObject):
    """Composite text item for displaying and editing position labels."""

    contentChanged = pyqtSignal()

    def __init__(
            self,
            group_name: str,
            is_start: bool = True,
            parent: Optional[QGraphicsItem] = None,
    ) -> None:
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

        self.setAcceptHoverEvents(True)

        # Initialize the text items
        self.prefix_item = QGraphicsTextItem(self)
        self.x_item = AnchorEditableTextItem(self)
        self.comma_item = QGraphicsTextItem(self)
        self.y_item = AnchorEditableTextItem(self)
        self.suffix_item = QGraphicsTextItem(self)

        self._setup_text_items()

        # Set up the initial text with formatting
        self._update_text()

        # Connect signals
        self.x_item.textEdited.connect(self._x_value_changed)
        self.y_item.textEdited.connect(self._y_value_changed)

    def _setup_text_items(self):
        font = QFont("Helvetica", 12, QFont.Weight.Bold)

        self.prefix_item.setFont(font)
        self.x_item.setFont(font)
        self.comma_item.setFont(font)
        self.y_item.setFont(font)
        self.suffix_item.setFont(font)

        self.x_item.setDefaultTextColor(Qt.GlobalColor.red)
        self.y_item.setDefaultTextColor(Qt.GlobalColor.green)

        # Non-editable items
        self.prefix_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.comma_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.suffix_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Editable items
        self.x_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.y_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

        self.x_item.setAcceptHoverEvents(True)
        self.y_item.setAcceptHoverEvents(True)

    def _update_text(self) -> None:
        """Update the text items with the current position."""
        position_label = 'Start' if self.is_start else 'End'
        if self.parent_item:
            x = int(self.parent_item.scenePos().x())
            y = int(self.parent_item.scenePos().y())
        else:
            x, y = 0, 0

        self.prefix_item.setPlainText(f"{self.group_name} {position_label} (")
        self.x_item.setPlainText(str(x))
        self.comma_item.setPlainText(",")
        self.y_item.setPlainText(str(y))
        self.suffix_item.setPlainText(")")

        # Position the items
        self._layout_items()

    def _layout_items(self):
        """Position the text items side by side."""
        self.prepareGeometryChange()

        x_offset = 0
        y_offset = 0

        # Position prefix_item
        self.prefix_item.setPos(x_offset, y_offset)
        x_offset += self.prefix_item.boundingRect().width()

        # Position x_item
        self.x_item.setPos(x_offset, y_offset)
        x_offset += self.x_item.boundingRect().width()

        # Position comma_item
        self.comma_item.setPos(x_offset, y_offset)
        x_offset += self.comma_item.boundingRect().width()

        # Position y_item
        self.y_item.setPos(x_offset, y_offset)
        x_offset += self.y_item.boundingRect().width()

        # Position suffix_item
        self.suffix_item.setPos(x_offset, y_offset)
        x_offset += self.suffix_item.boundingRect().width()

        # Store total width and height
        self.text_width = x_offset
        self.text_height = self.prefix_item.boundingRect().height()

        self.update()

    def boundingRect(self) -> QRectF:
        """Return the bounding rectangle encompassing all text items."""
        return self.childrenBoundingRect()

    def paint(
            self,
            painter,
            option: QStyleOptionGraphicsItem,
            widget: Optional[QWidget] = None,
    ) -> None:
        """No painting required; child items handle their own painting."""
        pass

    def update_position(self) -> None:
        """Update the position text based on the parent item's position and adjust if out of view."""
        self._update_text()

        # Default position: above the circle, centered horizontally
        circle_rect = self.parent_item.boundingRect()
        default_x = (circle_rect.width() - self.text_width) / 2
        default_y = -self.text_height - 5  # 5 pixels above the circle

        self.setPos(default_x, default_y)

        # Transform the text's bounding rect to scene coordinates
        text_scene_rect = self.mapToScene(self.boundingRect()).boundingRect()
        scene = self.scene()

        if scene is None:
            return

        # Get the view
        views = scene.views()
        if not views:
            return
        view = views[0]

        # Get the visible scene rect (the area currently visible in the view)
        visible_scene_rect = view.mapToScene(view.viewport().rect()).boundingRect()

        # Check if the text is within the visible scene
        if not visible_scene_rect.contains(text_scene_rect):
            # Try to reposition the text around the circle
            positions = [
                # Below the circle
                (default_x, circle_rect.height() + 5),
                # To the right of the circle
                (circle_rect.width() + 5, (circle_rect.height() - self.text_height) / 2),
                # To the left of the circle
                (-self.text_width - 5, (circle_rect.height() - self.text_height) / 2),
            ]

            for pos in positions:
                self.setPos(*pos)
                text_scene_rect = self.mapToScene(self.boundingRect()).boundingRect()
                if visible_scene_rect.contains(text_scene_rect):
                    break  # Found a position where text is fully visible
            else:
                # If none of the positions work, adjust to keep within visible scene bounds
                # Calculate the required adjustments
                dx = 0
                dy = 0
                if text_scene_rect.left() < visible_scene_rect.left():
                    dx = visible_scene_rect.left() - text_scene_rect.left()
                elif text_scene_rect.right() > visible_scene_rect.right():
                    dx = visible_scene_rect.right() - text_scene_rect.right()

                if text_scene_rect.top() < visible_scene_rect.top():
                    dy = visible_scene_rect.top() - text_scene_rect.top()
                elif text_scene_rect.bottom() > visible_scene_rect.bottom():
                    dy = visible_scene_rect.bottom() - text_scene_rect.bottom()

                # Adjust position accordingly
                current_pos = self.pos()
                self.setPos(current_pos.x() + dx, current_pos.y() + dy)

        self.prepareGeometryChange()
        self.update()

    def handle_new_coordinates(self, x: int, y: int):
        """Handle new coordinates after editing."""
        if self.parent_item:
            # Get scene dimensions
            scene = self.scene()
            if scene:
                views = scene.views()
                if views:
                    view = views[0]
                    min_x = 0
                    min_y = 0
                    max_x = view.width()
                    max_y = view.height()
                    logging.debug(f"max view width: {max_x}, height: {max_y}")
                    # Clamp x and y
                    clamped_x = min(max(x, min_x), max_x)
                    clamped_y = min(max(y, min_y), max_y)
                else:
                    # If no views, default to x and y as is
                    clamped_x, clamped_y = x, y
            else:
                # If scene not available, set x and y to 0
                clamped_x = clamped_y = 0
            self.parent_item.setPos(clamped_x, clamped_y)
            self.update_position()
            self.contentChanged.emit()
            logging.debug(f"Position updated to ({clamped_x}, {clamped_y})")

    def _x_value_changed(self):
        """Handle changes to the x value."""
        text = self.x_item.toPlainText()
        if text.isdigit():
            x = int(text)
            if self.parent_item:
                y = int(self.parent_item.scenePos().y())
                self.handle_new_coordinates(x, y)
        else:
            # Revert to previous value
            self.update_position()

    def _y_value_changed(self):
        """Handle changes to the y value."""
        text = self.y_item.toPlainText()
        if text.isdigit():
            y = int(text)
            if self.parent_item:
                x = int(self.parent_item.scenePos().x())
                self.handle_new_coordinates(x, y)
        else:
            # Revert to previous value
            self.update_position()
