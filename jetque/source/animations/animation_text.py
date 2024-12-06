# src/animations/animation_text.py

import logging
from typing import Optional

from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPainterPath, QFontMetricsF, QPixmap
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsDropShadowEffect, QGraphicsPixmapItem


class AnimationText(QGraphicsTextItem):
    """
    A customized QGraphicsTextItem that supports advanced font styling, such as outline and drop shadow.

    Attributes:
        drop_shadow (bool): Indicates if drop shadow effect is enabled.
        outline (bool): Indicates if outline effect is enabled.
        text_drop_shadow_effect (QGraphicsDropShadowEffect): The drop shadow effect applied to the text item.
        font_metrics_f (QFontMetricsF): The float font metrics of the text font.
        outline_pen (QPen): The pen used to draw the outline.
        TODO ADD MISSING ATTRIBUTES.
    """

    def __init__(
            self,
            text_font: QFont = QFont("Helvetica"),
            text_message: str = "Default Message",
            text_color: QColor = QColor(Qt.GlobalColor.white),
            outline: bool = False,
            outline_pen: QPen = QPen(Qt.GlobalColor.black, 2.0),
            drop_shadow: bool = False,
            drop_shadow_offset: QPointF = QPointF(-3.5, 6.1),
            drop_shadow_blur_radius: float = 7.0,
            drop_shadow_color: QColor = QColor(0, 0, 0, 191),
            icon: bool = False,
            icon_pixmap: QPixmap = None,
            icon_alignment: str = "left",  # String instead of bool incase more options are created
            icon_padding: float = 0.0,
            parent=None
    ) -> None:
        """
        Initializes the AnimationText with the provided parameters.

        Args:
            text_font (QFont): The font of the text.
            text_message (str): The text content.
            text_color (QColor): The color of the text.
            outline (bool): Whether to draw an outline around the text.
            outline_pen (QPen): The pen type used to draw the outline.
            drop_shadow (bool): Whether to apply a drop shadow effect.
            drop_shadow_offset (QPointF): The offset of the drop shadow.
            drop_shadow_blur_radius (float): The blur radius of the drop shadow.
            drop_shadow_color (QColor): The color of the drop shadow.
            parent: The parent widget.
            TODO ADD MISSING ARGUMENTS.
        """
        super().__init__(parent=None)

        try:
            self.setParent(parent)
            self.setFont(text_font)
            self.setPlainText(text_message)
            self.setDefaultTextColor(text_color)
            self.drop_shadow: bool = drop_shadow
            self.outline: bool = outline
            self.icon: bool = icon
            self.icon_alignment: str = icon_alignment
            self.icon_padding: float = icon_padding
            self.font_metrics_f: QFontMetricsF = QFontMetricsF(self.font())
            self.outline_pen: QPen = outline_pen
            self.outline_path: QPainterPath = QPainterPath()
            self.text_drop_shadow_effect = QGraphicsDropShadowEffect(self)
            self.animation_icon: QGraphicsPixmapItem = QGraphicsPixmapItem(self)

            # Applies a drop shadow effect to the text item.
            if self.drop_shadow:
                self.text_drop_shadow_effect.setOffset(drop_shadow_offset)
                self.text_drop_shadow_effect.setBlurRadius(drop_shadow_blur_radius)
                self.text_drop_shadow_effect.setColor(drop_shadow_color)
                self.setGraphicsEffect(self.text_drop_shadow_effect)

            # Applies an outline to paint around the text.
            if self.outline:
                outline_rect: QRectF = super().boundingRect().adjusted(
                    -self.outline_pen.widthF(),
                    -self.outline_pen.widthF(),
                    self.outline_pen.widthF(),
                    self.outline_pen.widthF()
                )

                self.outline_path.addText(
                    QPointF(
                        self.outline_pen.widthF() + (
                                outline_rect.width()
                                - 2.0 * self.outline_pen.width()
                                - self.font_metrics_f.horizontalAdvance(self.toPlainText())
                        ) / 2.0,
                        self.outline_pen.widthF() + self.font_metrics_f.ascent()
                    ),
                    self.font(),
                    self.toPlainText()
                )

            # Applies an icon to the text
            if self.icon:
                self.animation_icon.setPixmap(icon_pixmap)
                pixmap_width_f: float = self.animation_icon.pixmap().size().toSizeF().width()
                pixmap_height_f: float = self.animation_icon.pixmap().size().toSizeF().height()
                scale_factor: float = ((self.font_metrics_f.ascent() + self.font_metrics_f.descent())
                                       / max(pixmap_width_f, pixmap_height_f))

                self.animation_icon.setScale(scale_factor)
                pixmap_scaled_width_f: float = pixmap_width_f * scale_factor

                if self.icon_alignment.lower() == "left":
                    self.animation_icon.setPos(-pixmap_scaled_width_f, 0.0)
                elif self.icon_alignment.lower() == "right":
                    self.animation_icon.setPos(pixmap_scaled_width_f, 0.0)

            logging.debug("AnimationText initialized with text: '%s'", self.toPlainText())

        except Exception as e:
            logging.exception("Failed to initialize AnimationText: %s", e)

    def boundingRect(self) -> QRectF:

        bounding_rect: QRectF = super().boundingRect()

        if self.outline:
            bounding_rect.adjust(
                -self.outline_pen.widthF(),
                -self.outline_pen.widthF(),
                self.outline_pen.widthF(),
                self.outline_pen.widthF()
            )

        if self.icon:
            bounding_rect = bounding_rect.united(self.animation_icon.boundingRect())

        return bounding_rect

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
