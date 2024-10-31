# jetque/src/animations/animation_label.py

import logging
from typing import Optional, Tuple

from PyQt6.QtCore import QSize
from PyQt6.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PyQt6.QtWidgets import QLabel

from src.overlays.active_overlay import ActiveOverlay
from .animation_icon import AnimationIcon  # Importing AnimationIcon from animation_icon.py

# Constants
DEFAULT_FONT_TYPE: str = "Arial"
DEFAULT_FONT_SIZE: int = 24
DEFAULT_FONT_COLOR: QColor = QColor("white")
DEFAULT_FONT_OUTLINE: str = "thin"  # Options: 'none', 'thin', 'thick'
DEFAULT_FONT_OUTLINE_COLOR: QColor = QColor("black")
DEFAULT_FONT_DROP_SHADOW: str = "none"  # Options: 'none', 'weak', 'strong'
DEFAULT_ICON_POSITION: str = "left"  # Options: 'left', 'right'
ICON_SPACING: int = 5


class AnimationLabel(QLabel):
    """
    A QLabel subclass that displays text with an optional icon, customizable font,
    outline, shadow, and other styling options.
    """

    def __init__(
            self,
            parent: Optional[ActiveOverlay] = None,
            text: str = "",
            icon_pixmap: Optional[QPixmap] = None,
            font_type: str = DEFAULT_FONT_TYPE,
            font_size: int = DEFAULT_FONT_SIZE,
            font_color: QColor = DEFAULT_FONT_COLOR,
            font_outline: str = DEFAULT_FONT_OUTLINE,
            font_outline_color: QColor = DEFAULT_FONT_OUTLINE_COLOR,
            font_drop_shadow: str = DEFAULT_FONT_DROP_SHADOW,
            font_italic: bool = False,
            font_bold: bool = False,
            font_underline: bool = False,
            icon_position: str = DEFAULT_ICON_POSITION,
    ) -> None:
        """
        Initialize the AnimationLabel.

        Args:
            parent (Optional[ActiveOverlay]): The parent widget.
            text (str): The display text.
            icon_pixmap (Optional[QPixmap]): The icon image.
            font_type (str): The font family.
            font_size (int): The font size.
            font_color (QColor): The font color.
            font_outline (str): Outline style ('none', 'thin', 'thick').
            font_outline_color (QColor): Color of the font outline.
            font_drop_shadow (str): Drop shadow style ('none', 'weak', 'strong').
            font_italic (bool): Italicize the font.
            font_bold (bool): Bold the font.
            font_underline (bool): Underline the font.
            icon_position (str): Position of the icon ('left' or 'right').
        """
        super().__init__(parent)
        self._font_type: str = font_type
        self._font_size: int = font_size
        self._font_color: QColor = font_color
        self._font_outline: str = font_outline.lower()
        self._font_outline_color: QColor = font_outline_color
        self._font_drop_shadow: str = font_drop_shadow.lower()
        self._font_italic: bool = font_italic
        self._font_bold: bool = font_bold
        self._font_underline: bool = font_underline
        self.icon_position: str = icon_position.lower()

        self._animation_icon: Optional[AnimationIcon] = None  # Updated type hint

        if icon_pixmap:
            self._animation_icon = AnimationIcon(
                parent=self,
                pixmap=icon_pixmap,
                font_size=self._font_size,
                position=self.icon_position,
            )
            logging.info("AnimationIcon initialized.")

        self.setFont(self._create_font())
        self.setStyleSheet("background-color: transparent;")
        self.set_text(text)

    def set_text(self, text: str) -> None:
        """
        Set the display text.

        Args:
            text (str): The new text to display.
        """
        self.setText(text)
        self.update()
        self.adjust_size()
        logging.info("Label text set to '%s'.", text)

    def set_font_type(self, font_type: str) -> None:
        """
        Set the font family.

        Args:
            font_type (str): The font family name.
        """
        self._font_type = font_type
        self.setFont(self._create_font())
        self.adjust_size()
        self.update()
        logging.info("Font type set to '%s'.", font_type)

    def set_font_size(self, font_size: int) -> None:
        """
        Set the font size.

        Args:
            font_size (int): The new font size.
        """
        self._font_size = font_size
        self.setFont(self._create_font())
        if self._animation_icon:
            self._animation_icon.set_font_size(self._font_size)
        self.adjust_size()
        self.update()
        logging.info("Font size set to %d.", font_size)

    def set_font_color(self, color: QColor) -> None:
        """
        Set the font color.

        Args:
            color (QColor): The new font color.
        """
        self._font_color = color
        self.update()
        logging.info("Font color set to %s.", color.name())

    def set_font_outline(self, outline: str) -> None:
        """
        Set the font outline style.

        Args:
            outline (str): 'none', 'thin', or 'thick'.
        """
        if outline.lower() in {"none", "thin", "thick"}:
            self._font_outline = outline.lower()
            self.update()
            logging.info("Font outline set to '%s'.", outline.lower())
        else:
            logging.warning("Invalid font outline '%s'. No changes made.", outline)

    def set_font_outline_color(self, color: QColor) -> None:
        """
        Set the font outline color.

        Args:
            color (QColor): The new outline color.
        """
        self._font_outline_color = color
        self.update()
        logging.info("Font outline color set to %s.", color.name())

    def set_font_drop_shadow(self, shadow: str) -> None:
        """
        Set the font drop shadow style.

        Args:
            shadow (str): 'none', 'weak', or 'strong'.
        """
        if shadow.lower() in {"none", "weak", "strong"}:
            self._font_drop_shadow = shadow.lower()
            self.update()
            logging.info("Font drop shadow set to '%s'.", shadow.lower())
        else:
            logging.warning("Invalid font drop shadow '%s'. No changes made.", shadow)

    def set_font_italic(self, italic: bool) -> None:
        """
        Set the font italic style.

        Args:
            italic (bool): True to italicize, False otherwise.
        """
        self._font_italic = italic
        self.setFont(self._create_font())
        self.update()
        logging.info("Font italic set to %s.", italic)

    def set_font_bold(self, bold: bool) -> None:
        """
        Set the font bold style.

        Args:
            bold (bool): True to bold, False otherwise.
        """
        self._font_bold = bold
        self.setFont(self._create_font())
        self.update()
        logging.info("Font bold set to %s.", bold)

    def set_font_underline(self, underline: bool) -> None:
        """
        Set the font underline style.

        Args:
            underline (bool): True to underline, False otherwise.
        """
        self._font_underline = underline
        self.setFont(self._create_font())
        self.update()
        logging.info("Font underline set to %s.", underline)

    def set_icon_pixmap(self, pixmap: Optional[QPixmap]) -> None:
        """
        Set or update the icon pixmap.

        Args:
            pixmap (Optional[QPixmap]): The new pixmap to set.
        """
        try:
            if self._animation_icon:
                self._animation_icon.set_pixmap(pixmap)
            else:
                if pixmap:
                    self._animation_icon = AnimationIcon(
                        parent=self,
                        pixmap=pixmap,
                        font_size=self._font_size,
                        position=self.icon_position,
                    )
                    logging.info("AnimationIcon added.")
            self.adjust_size()
            self.update()
        except Exception as e:
            logging.exception("Failed to set icon pixmap: %s", e)

    def set_icon_position(self, position: str) -> None:
        """
        Set the position of the icon relative to the text.

        Args:
            position (str): 'left' or 'right'.
        """
        try:
            if position.lower() in {"left", "right"}:
                self.icon_position = position.lower()
                if self._animation_icon:
                    self._animation_icon.set_position(self.icon_position)
                self.adjust_size()
                self.update()
                logging.info("Icon position set to '%s'.", self.icon_position)
            else:
                logging.warning("Invalid icon position '%s'. No changes made.", position)
        except Exception as e:
            logging.exception("Failed to set icon position: %s", e)

    def _calculate_size(self) -> Tuple[int, int]:
        """
        Calculate the total width and height required for the label.

        Returns:
            Tuple[int, int]: The total width and height.
        """
        fm: QFontMetrics = QFontMetrics(self.font())
        text_width: int = fm.horizontalAdvance(self.text())
        text_height: int = fm.height()

        icon_width: int = 0
        if self._animation_icon and not self._animation_icon.pixmap().isNull():
            icon_width = self._animation_icon.width() + ICON_SPACING

        total_width: int = text_width + icon_width
        total_height: int = text_height

        return total_width, total_height

    def adjust_size(self) -> None:
        """
        Adjust the size of the label to accommodate text and optional icon.
        """
        try:
            total_width, total_height = self._calculate_size()

            self.setFixedSize(total_width, total_height)

            if self._animation_icon:
                icon_y: int = 0
                if self.icon_position == "left":
                    self._animation_icon.move(0, icon_y)
                else:
                    self._animation_icon.move(total_width - self._animation_icon.width(), icon_y)

            logging.debug("Label size adjusted to %dx%d.", total_width, total_height)
        except Exception as e:
            logging.exception("Failed to adjust size: %s", e)

    def sizeHint(self) -> QSize:
        """
        Provide a recommended size for the label.

        Returns:
            QSize: The recommended size.
        """
        try:
            total_width, total_height = self._calculate_size()

            logging.debug("Size hint calculated as %dx%d.", total_width, total_height)
            return QSize(total_width, total_height)
        except Exception as e:
            logging.exception("Failed to provide size hint: %s", e)
            return QSize(0, 0)

    def _create_font(self) -> QFont:
        """
        Create a QFont object based on the current font settings.

        Returns:
            QFont: The configured font.
        """
        font: QFont = QFont(self._font_type, self._font_size)
        font.setItalic(self._font_italic)
        font.setBold(self._font_bold)
        font.setUnderline(self._font_underline)
        logging.debug(
            "Font created with type '%s', size %d.", self._font_type, self._font_size
        )
        return font

    def paintEvent(self, event) -> None:
        """
        Override the paintEvent to customize text rendering with optional outline and shadow.

        Args:
            event: The paint event.
        """
        try:
            painter: QPainter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            fm: QFontMetrics = QFontMetrics(self.font())

            text_x: int = 0
            if self._animation_icon and not self._animation_icon.pixmap().isNull():
                if self.icon_position == "left":
                    text_x = self._animation_icon.width() + ICON_SPACING

            text_y: int = (self.height() + fm.ascent() - fm.descent()) // 2

            # Draw drop shadow if enabled
            if self._font_drop_shadow != "none":
                shadow_color: QColor = QColor(0, 0, 0, 160)  # Semi-transparent black
                shadow_offset: int = 3 if self._font_drop_shadow == "strong" else 1
                painter.setPen(shadow_color)
                painter.drawText(text_x + shadow_offset, text_y + shadow_offset, self.text())
                logging.debug("Drop shadow drawn with offset %d.", shadow_offset)

            # Draw outline if enabled
            if self._font_outline in {"thin", "thick"}:
                outline_pen: QPen = QPen(self._font_outline_color)
                outline_pen.setWidth(1 if self._font_outline == "thin" else 2)
                painter.setPen(outline_pen)
                path: QPainterPath = QPainterPath()
                path.addText(text_x, text_y, self.font(), self.text())
                painter.drawPath(path)
                logging.debug("Text outline drawn with width %d.", outline_pen.width())

            # Draw main text
            painter.setPen(self._font_color)
            painter.setFont(self.font())
            painter.drawText(text_x, text_y, self.text())
            logging.debug("Main text drawn at (%d, %d).", text_x, text_y)

            painter.end()
        except Exception as e:
            logging.exception("Failed to paint event: %s", e)
