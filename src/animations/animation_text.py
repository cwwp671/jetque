# src/animations/animation_text.py

import logging
from typing import Optional

from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPainterPath, QFontMetricsF
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsDropShadowEffect


class AnimationText(QGraphicsTextItem):
    """
    A customized QGraphicsTextItem that supports advanced font styling, such as outline and drop shadow.

    Attributes:
        drop_shadow (bool): Indicates if drop shadow effect is enabled.
        outline (bool): Indicates if outline effect is enabled.
        drop_shadow_effect (QGraphicsDropShadowEffect): The drop shadow effect applied to the text item.
        font_metrics_f (QFontMetricsF): The float font metrics of the text font.
        outline_pen (QPen): The pen used to draw the outline.
        bounding_rect_adjusted (QRectF): The float adjusted bounding rectangle accounting for the outline pen width.
    """

    def __init__(
            self,
            text_font: QFont = QFont("Helvetica", -1, -1, False),
            text_message: str = "Text Unassigned",
            text_color: QColor = QColor(Qt.GlobalColor.white),
            outline: bool = True,
            outline_pen: QPen = None,
            drop_shadow: bool = True,
            drop_shadow_offset: QPointF = QPointF(-3.5, 6.1),  # Using Photoshop default value
            drop_shadow_blur_radius: float = 7.0,  # Using Photoshop default value
            drop_shadow_color: QColor = QColor("0, 0, 0, 191"),  # Using Photoshop default value
            parent=None
    ) -> None:
        """
        Initializes the AnimationText with the provided parameters.

        Args:
            text_font (QFont): The font of the text.
            text_message (str): The text content.
            text_color (QColor): The color of the text.
            outline (bool): Whether to draw an outline around the text.
            outline_pen (int): The doubled thickness in pixels of the outline.
            drop_shadow (bool): Whether to apply a drop shadow effect.
            drop_shadow_offset (QPointF): The offset of the drop shadow.
            drop_shadow_blur_radius (float): The blur radius of the drop shadow.
            drop_shadow_color (QColor): The color of the drop shadow.
            parent: The parent widget.
        """
        super().__init__(parent)

        try:
            self.setFont(text_font)
            self.setPlainText(text_message)
            self.setDefaultTextColor(text_color)
            self.drop_shadow: bool = drop_shadow
            self.outline: bool = outline

            if self.drop_shadow:
                # Applies a drop shadow effect to the text item
                self.drop_shadow_effect = QGraphicsDropShadowEffect(parent=self)
                self.drop_shadow_effect.setOffset(drop_shadow_offset)
                self.drop_shadow_effect.setBlurRadius(drop_shadow_blur_radius)
                self.drop_shadow_effect.setColor(drop_shadow_color)
                self.setGraphicsEffect(self.drop_shadow_effect)

            if self.outline:
                # Sets up an Outline to paint around the text
                self.font_metrics_f: QFontMetricsF = QFontMetricsF(self.font())
                self.outline_pen: QPen = outline_pen
                self.bounding_rect_adjusted: QRectF = super().boundingRect().adjusted(
                    -self.outline_pen.widthF(),
                    -self.outline_pen.widthF(),
                    self.outline_pen.widthF(),
                    self.outline_pen.widthF()
                )

                self.outline_path: QPainterPath = QPainterPath()
                self.outline_path.addText(
                    QPointF(
                        self.outline_pen.widthF() + (
                                self.bounding_rect_adjusted.width()
                                - 2.0 * self.outline_pen.width()
                                - self.font_metrics_f.horizontalAdvance(self.toPlainText())
                        ) / 2.0,
                        self.outline_pen.widthF() + self.font_metrics_f.ascent()
                    ),
                    self.font(),
                    self.toPlainText()
                )

            logging.debug("AnimationText initialized with text: '%s'", self.toPlainText())

        except Exception as e:
            logging.exception("Failed to initialize AnimationText: %s", e)

    def paint(
            self,
            painter: QPainter,
            option,
            widget: Optional[object] = None
    ) -> None:
        """
        Override QGraphicsTextItem paint to draw text with or without an outline.

        Args:
            painter (QPainter): The painter used to draw the item.
            option: Style options for the item.
            widget (Optional[object], optional): The widget being painted on. Defaults to None.
        """
        try:
            if self.outline:
                painter.setPen(self.outline_pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.strokePath(self.outline_path, self.outline_pen)

                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(self.defaultTextColor())
                painter.fillPath(self.outline_path, painter.brush())
            else:
                super().paint(painter, option, widget)

        except Exception as e:
            logging.exception("Failed to paint AnimationText: %s", e)
