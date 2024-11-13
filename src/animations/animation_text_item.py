# src/animations/animation_text_item.py

import logging
from typing import Optional

from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPainterPath, QFontMetrics
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsDropShadowEffect

# Constants
DEFAULT_TEXT_MESSAGE: str = "No Text Assigned"
DEFAULT_TEXT_COLOR: str = "Black"
DEFAULT_OUTLINE_COLOR: str = "Black"
DEFAULT_OUTLINE_STRENGTH: int = 1
DEFAULT_DROP_SHADOW_BLUR_RADIUS: float = 5.0
DEFAULT_DROP_SHADOW_OFFSET: QPointF = QPointF(2.0, 2.0)


class AnimationTextItem(QGraphicsTextItem):
    """
    A customized QGraphicsTextItem that supports advanced font styling.

    Attributes:
        outline_color (Optional[QColor]): The color of the text outline.
        outline_strength (Optional[int]): The strength of the text outline.
        drop_shadow_effect (Optional[QGraphicsDropShadowEffect]): The drop shadow effect applied to the text.
        drop_shadow_blur_radius (Optional[float]): The blur radius of the drop shadow.
        drop_shadow_offset (Optional[QPointF]): The offset of the drop shadow.
    """

    def __init__(
            self,
            font: QFont,
            text_message: str = DEFAULT_TEXT_MESSAGE,
            text_color: str = DEFAULT_TEXT_COLOR,
            text_outline_color: Optional[str] = None,
            text_outline_strength: Optional[int] = None,
            text_drop_shadow_offset: Optional[QPointF] = None,
            text_drop_shadow_blur_radius: Optional[float] = None
    ) -> None:
        """
        Initializes the AnimationTextItem with the provided parameters.

        Args:
            font (QFont): The font to be used for the text.
            text_message (str, optional): The text message to display. Defaults to DEFAULT_TEXT_MESSAGE.
            text_color (str, optional): The color of the text. Defaults to DEFAULT_TEXT_COLOR.
            text_outline_color (Optional[str], optional): The color of the text outline.
            text_outline_strength (Optional[int], optional): The strength of the text outline.
            text_drop_shadow_offset (Optional[QPointF], optional): The offset of the drop shadow.
            text_drop_shadow_blur_radius (Optional[float], optional): The blur radius of the drop shadow.
        """
        super().__init__()

        try:
            self.setFont(font)
            self.setPlainText(text_message)
            self.setDefaultTextColor(QColor(text_color))

            self.outline_color: Optional[QColor] = None
            self.outline_strength: Optional[int] = None
            self.drop_shadow_effect: Optional[QGraphicsDropShadowEffect] = None
            self.drop_shadow_blur_radius: Optional[float] = None
            self.drop_shadow_offset: Optional[QPointF] = None

            if text_outline_strength is not None:
                self.set_outline_strength(text_outline_strength)

                if text_outline_color is not None:
                    self.set_outline_color(text_outline_color)

            if text_drop_shadow_blur_radius is not None:
                self.set_drop_shadow_blur_radius(text_drop_shadow_blur_radius)

                if text_drop_shadow_offset is not None:
                    self.set_drop_shadow_offset(text_drop_shadow_offset)

                self._apply_drop_shadow()

            logging.debug("AnimationTextItem initialized with text: '%s'", self.toPlainText())

        except Exception as e:
            logging.exception("Failed to initialize AnimationTextItem: %s", e)

    def bounding_rect(self) -> QRectF:
        """
        Overrides the boundingRect to include padding for the outline.

        Returns:
            QRectF: The adjusted bounding rectangle.
        """
        try:
            base_rect = super().boundingRect()
            outline_thickness = self.outline_strength if self.outline_strength else DEFAULT_OUTLINE_STRENGTH
            padding = outline_thickness * 2.0
            return base_rect.adjusted(-padding, -padding, padding, padding)
        except Exception as e:
            logging.exception("Failed to calculate bounding rectangle: %s", e)
            return super().boundingRect()

    def paint(
            self,
            painter: QPainter,
            option,
            widget: Optional[object] = None
    ) -> None:
        """
        Paints the text item with outline and antialiasing.

        Args:
            painter (QPainter): The painter used to draw the item.
            option: Style options for the item.
            widget (Optional[object], optional): The widget being painted on. Defaults to None.
        """
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

            painter.setOpacity(self.opacity())
            font_metrics = QFontMetrics(self.font())
            ascent = font_metrics.ascent()

            outline_thickness = self.outline_strength if self.outline_strength else DEFAULT_OUTLINE_STRENGTH
            padding = outline_thickness * 2.0
            rect = self.bounding_rect()

            text_width = font_metrics.horizontalAdvance(self.toPlainText())
            x = padding + (rect.width() - 2.0 * padding - text_width) / 2.0
            y = padding + ascent

            path = QPainterPath()
            path.addText(x, y, self.font(), self.toPlainText())

            pen_color = self.outline_color if self.outline_color else QColor(DEFAULT_OUTLINE_COLOR)
            pen = QPen(pen_color)
            pen.setWidthF(outline_thickness)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.strokePath(path, pen)

            logging.debug(
                "Painted outline with strength: %d and color: %s",
                outline_thickness,
                pen.color().name()
            )

            fill_color = QColor(self.defaultTextColor())
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(fill_color)

            painter.fillPath(path, painter.brush())

        except Exception as e:
            logging.exception("Failed to paint AnimationTextItem: %s", e)

    def set_outline_strength(self, outline_strength: int) -> None:
        """
        Sets the strength of the text outline.

        Args:
            outline_strength (int): The new outline strength.
        """
        self.outline_strength = outline_strength
        self.update()
        logging.debug("Outline strength set to: %d", self.outline_strength)

    def set_outline_color(self, outline_color: str) -> None:
        """
        Sets the color of the text outline.

        Args:
            outline_color (str): The new outline color.
        """
        self.outline_color = QColor(outline_color)
        self.update()
        logging.debug("Outline color set to: %s", self.outline_color.name())

    def set_drop_shadow_blur_radius(self, blur_radius: float) -> None:
        """
        Sets the blur radius of the drop shadow.

        Args:
            blur_radius (float): The new blur radius.
        """
        self.drop_shadow_blur_radius = blur_radius
        self.update()
        logging.debug("Drop shadow blur radius set to: %.2f", self.drop_shadow_blur_radius)

    def set_drop_shadow_offset(self, offset: QPointF) -> None:
        """
        Sets the offset of the drop shadow.

        Args:
            offset (QPointF): The new drop shadow offset.
        """
        self.drop_shadow_offset = offset
        self.update()
        logging.debug(
            "Drop shadow offset set to: (%.2f, %.2f)",
            self.drop_shadow_offset.x(),
            self.drop_shadow_offset.y()
        )

    def _apply_drop_shadow(self) -> None:
        """
        Applies the drop shadow effect to the text item.
        """
        try:
            if self.drop_shadow_blur_radius is None:
                self.drop_shadow_blur_radius = DEFAULT_DROP_SHADOW_BLUR_RADIUS
            if self.drop_shadow_offset is None:
                self.drop_shadow_offset = DEFAULT_DROP_SHADOW_OFFSET

            self.drop_shadow_effect = QGraphicsDropShadowEffect()
            self.drop_shadow_effect.setBlurRadius(self.drop_shadow_blur_radius)
            self.drop_shadow_effect.setOffset(self.drop_shadow_offset)
            self.setGraphicsEffect(self.drop_shadow_effect)

            logging.debug(
                "Drop shadow applied with blur radius: %.2f and offset: (%.2f, %.2f)",
                self.drop_shadow_blur_radius,
                self.drop_shadow_offset.x(),
                self.drop_shadow_offset.y()
            )

        except Exception as e:
            logging.exception("Failed to apply drop shadow: %s", e)
