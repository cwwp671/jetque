# jetque/source/animations/animation_anchor_text.py

import re

from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsObject
from PyQt6.QtCore import QRectF, Qt, pyqtSignal


class AnimationAnchorText(QGraphicsObject):
    contentChanged = pyqtSignal()

    def __init__(self, group_name, is_start=True, parent=None):
        super().__init__(parent)
        self.group_name = group_name
        self.is_start = is_start
        self.parent_item = parent

        # Determine 'Start' or 'End' based on the is_start flag
        position_label = 'Start' if self.is_start else 'End'

        # Non-editable text item
        self.label_text_item = QGraphicsTextItem(f"{self.group_name} {position_label}: ", self)
        self.label_text_item.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Editable text item
        x = self.parent_item.x() if self.parent_item else 0
        y = self.parent_item.y() if self.parent_item else 0
        self.position_text_item = QGraphicsTextItem(f"[{x}, {y}]", self)
        self.position_text_item.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

        # Connect the text change signal to the slot
        self.position_text_item.document().contentsChanged.connect(self.on_position_text_changed)

        # Position the text items next to each other
        self.label_text_item.setPos(0, 0)
        label_width = self.label_text_item.boundingRect().width()
        self.position_text_item.setPos(label_width, 0)
        rect = self.label_text_item.boundingRect()

    def boundingRect(self) -> QRectF:
        pos_rect = self.position_text_item.boundingRect()
        pos_rect.translate(self.position_text_item.pos())
        return rect.united(pos_rect)

    def update_position(self):
        if self.parent_item:
            x = self.parent_item.x()
            y = self.parent_item.y()
            self.position_text_item.setPlainText(f"[{x}, {y}]")

    def paint(self, painter: QPainter, option, widget=None):
        # No painting required; child items handle their own painting
        pass

    def on_content_changed(self):
        # Prepare for geometry change due to text size change
        self.prepareGeometryChange()
        self.contentChanged.emit()

    def on_position_text_changed(self):
        text = self.position_text_item.toPlainText()
        # Regular expression to parse the [x, y] format
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
