# jetque/src/animations/animation_icon.py

import logging
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel

from src.animations.animation_label import AnimationLabel  # If needed for type hints

# Constants
DEFAULT_FONT_SIZE: int = 24
DEFAULT_ICON_POSITION: str = "left"  # Options: 'left', 'right'


class AnimationIcon(QLabel):
    """
    A QLabel subclass that handles the display and positioning of an icon
    relative to the text in AnimationLabel.
    """

    def __init__(
            self,
            parent: Optional[AnimationLabel] = None,
            pixmap: Optional[QPixmap] = None,
            font_size: int = DEFAULT_FONT_SIZE,
            position: str = DEFAULT_ICON_POSITION,
    ) -> None:
        """
        Initialize the AnimationIcon.

        Args:
            parent (Optional[AnimationLabel]): The parent AnimationLabel.
            pixmap (Optional[QPixmap]): The icon image.
            font_size (int): The font size to scale the icon.
            position (str): Position of the icon ('left' or 'right').
        """
        super().__init__(parent)
        self._pixmap = pixmap
        self.position = position.lower()
        self.font_size = font_size

        self.setScaledContents(True)
        self.update_icon()

    def set_pixmap(self, pixmap: Optional[QPixmap]) -> None:
        """
        Set the pixmap for the icon.

        Args:
            pixmap (Optional[QPixmap]): The new pixmap to set.
        """
        try:
            self._pixmap = pixmap
            self.update_icon()
            logging.info("Icon pixmap updated.")
        except Exception as e:
            logging.exception("Failed to set pixmap: %s", e)

    def set_font_size(self, font_size: int) -> None:
        """
        Update the font size, which affects the icon size.

        Args:
            font_size (int): The new font size.
        """
        try:
            self.font_size = font_size
            self.update_icon()
            logging.info("Icon font size updated to %d.", font_size)
        except Exception as e:
            logging.exception("Failed to set font size: %s", e)

    def set_position(self, position: str) -> None:
        """
        Set the position of the icon relative to the text.

        Args:
            position (str): 'left' or 'right'.
        """
        try:
            if position.lower() in {"left", "right"}:
                self.position = position.lower()
                self.update_parent_layout()
                logging.info("Icon position set to '%s'.", self.position)
            else:
                logging.warning(
                    "Invalid icon position '%s'. Defaulting to 'left'.", position
                )
                self.position = "left"
                self.update_parent_layout()
        except Exception as e:
            logging.exception("Failed to set icon position: %s", e)

    def update_icon(self) -> None:
        """
        Update the icon's pixmap and size based on the current font size.
        """
        if self._pixmap:
            icon_height = self.font_size
            icon_width = icon_height  # Width equals height
            self.setFixedSize(icon_width, icon_height)

            scaled_pixmap = self._pixmap.scaled(
                icon_width,
                icon_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(scaled_pixmap)
            logging.debug("Icon scaled to %dx%d.", icon_width, icon_height)
        else:
            self.setFixedSize(0, 0)
            self.setPixmap(QPixmap())
            logging.debug("No pixmap set for icon.")

    def update_parent_layout(self) -> None:
        """
        Trigger the parent AnimationLabel to update its layout.
        """
        parent = self.parent()
        if isinstance(parent, AnimationLabel):
            parent.adjust_size()
            parent.update()
