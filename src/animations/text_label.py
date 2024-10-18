# jetque/src/animations/text_label.py

import logging
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel

class TextLabel(QLabel):
    """Class responsible for creating and managing the label text."""

    def __init__(self, parent, config):
        super().__init__(parent)
        self.hide()
        self.setText(config['text'].get('content', ''))
        font_name = config['text'].get('font', 'Arial')
        font_size = config['text'].get('size', 18)
        font = QFont()
        font.setFamily(font_name)
        font.setPointSize(font_size)
        self.setFont(font)
        self.setStyleSheet(f"color: {config['text'].get('color', 'white')}")
        self.adjustSize()
        # self._center_in_window()
        logging.debug("TextLabel initialized and centered.")

    def _center_in_window(self):
        """Center the text in the parent window."""
        parent_width = self.parentWidget().width()
        parent_height = self.parentWidget().height()
        label_width = self.width()
        label_height = self.height()

        x = (parent_width - label_width) // 2
        y = (parent_height - label_height) // 2

        self.move(x, y)
        logging.debug(f"Window Width: {parent_width}, Window Height: {parent_height}")
        logging.debug(f"Width: {label_width}, Height: {label_height}. Centered at ({x}, {y})")
        logging.debug(f"Centered at ({x}, {y})")

    def set_position_centered(self, x, y):
        """Set the label position based on its center."""
        label_width = self.width()
        label_height = self.height()

        self.move(int(x - label_width / 2), int(y - label_height / 2))
        # logging.debug(
        #    f"TextLabel moved to centered position ({int(x - label_width / 2)}, "
        #    f"{int(y - label_height / 2)})"
        #)

    def set_position(self, x, y):
        """Set the label position based on the top-left corner."""
        self.move(int(x), int(y))
        # logging.debug(f"TextLabel moved to top-left position ({int(x)}, {int(y)})")

    def set_position_top_right(self, x, y):
        """Set the label position based on the top-right corner."""
        label_width = self.width()

        self.move(int(x - label_width), int(y))
        #logging.debug(
        #    f"TextLabel moved to top-right position ({int(x - label_width)}, {int(y)})"
        #)
