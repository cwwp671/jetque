# jetque/source/animations/anchor_editable_text_item.py

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFocusEvent, QKeyEvent


class AnchorEditableTextItem(QGraphicsTextItem):
    """Custom QGraphicsTextItem that allows editing of numeric values only."""
    textEdited = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.previous_text = self.toPlainText()
        self.setAcceptHoverEvents(True)

    def focusOutEvent(self, event: QFocusEvent):
        """Emit signal if text has changed after editing."""
        super().focusOutEvent(event)
        if self.toPlainText() != self.previous_text:
            self.textEdited.emit()
            self.previous_text = self.toPlainText()

    def keyPressEvent(self, event: QKeyEvent):
        """Allow only digits and navigation keys during editing."""
        key = event.key()
        if key in (
                Qt.Key.Key_Backspace, Qt.Key.Key_Delete, Qt.Key.Key_Left,
                Qt.Key.Key_Right, Qt.Key.Key_Home, Qt.Key.Key_End
        ):
            super().keyPressEvent(event)
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.clearFocus()
        elif event.text().isdigit():
            super().keyPressEvent(event)
        else:
            event.ignore()
