import logging
from typing import Optional

from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QFont, QPen
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QGraphicsSimpleTextItem, QGraphicsItem


class JQGraphicsSimpleTextItem(QGraphicsSimpleTextItem):
    """
    A custom QGraphicsSimpleTextItem with limited text capabilities.

    Attributes:
        outline (bool): Flag to enable or disable outline effect.
        color (QColor): Color of the text to display.
        outline_pen (QPen): Pen used for the text outline.
        drop_shadow (bool): Flag to enable or disable drop shadow effect.
        drop_shadow_effect (QGraphicsDropShadowEffect): Effect for the text drop shadow.
        collision_rect (QRectF): Rectangle used for collision detection.
        _bounding_rect (QRectF): Cached bounding rectangle of the item.
    """

    def __init__(
            self,
            font: QFont = QFont("Helvetica"),
            text: str = "No Message Set",
            color: QColor = QColor(Qt.GlobalColor.white),
            outline: bool = True,
            outline_pen: QPen = QPen(Qt.GlobalColor.black, 2.0),
            drop_shadow: bool = True,
            drop_shadow_offset: QPointF = QPointF(3.5, 6.1),
            drop_shadow_blur_radius: float = 7.0,
            drop_shadow_color: QColor = QColor(0, 0, 0, 191),
            parent: Optional[QGraphicsItem] = None
    ) -> None:
        """
        Initialize the JQGraphicsSimpleTextItem with specified properties.

        Args:
            font (QFont, optional): Font used for the text.
            text (str, optional): The text to display.
            color (QColor, optional): Text color.
            outline (bool, optional): Enable outline effect.
            outline_pen (QPen, optional): Pen for the outline.
            drop_shadow (bool, optional): Enable drop shadow effect.
            drop_shadow_offset (QPointF, optional): Offset for the drop shadow.
            drop_shadow_blur_radius (float, optional): Blur radius for the drop shadow.
            drop_shadow_color (QColor, optional): Color of the drop shadow.
            parent (Optional[QGraphicsItem], optional): Parent QGraphicsItem.
        """
        super().__init__(parent)

        try:
            self.setFont(font)
            self.setText(text)
            self.color: QColor = color
            self.outline: bool = outline
            self.outline_pen: QPen = outline_pen
            self.drop_shadow: bool = drop_shadow
            self.drop_shadow_effect: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect()
            self.collision_rect: QRectF = QRectF()
            self._bounding_rect: QRectF = QRectF()

            if self.outline:
                # Apply outline effect
                self.setPen(self.outline_pen)

            # Apply fill effect
            self.setBrush(self.color)

            if self.drop_shadow:
                # Apply drop shadow effect
                self.drop_shadow_effect.setOffset(drop_shadow_offset)
                self.drop_shadow_effect.setBlurRadius(drop_shadow_blur_radius)
                self.drop_shadow_effect.setColor(drop_shadow_color)
                self.prepareGeometryChange()  # Call before boundingRect changes
                self.setGraphicsEffect(self.drop_shadow_effect)

            self.prepareGeometryChange()  # Call before boundingRect changes
            self._bounding_rect = self._calculate_bounding_rect()

            # Set the origin point to the center for transformations (excludes drop shadow)
            self.setTransformOriginPoint(self.collision_rect.width() / 2.0, self.collision_rect.height() / 2.0)
        except Exception as e:
            logging.exception("Failed to initialize JQGraphicsSimpleTextItem: %s", e)

    def boundingRect(self) -> QRectF:
        """
        Override the boundingRect method to provide the custom bounding rectangle.

        Returns:
            QRectF: The bounding rectangle of the item.
        """
        return self._bounding_rect

    def _calculate_bounding_rect(self) -> QRectF:
        """
        Calculate and cache the bounding rectangle considering outline and drop shadow.

        Returns:
            QRectF: The calculated bounding rectangle.
        """
        try:
            temporary_rect: QRectF = super().boundingRect()

            if self.outline:
                # Adjust bounding rect to accommodate the outline width
                extra: float = self.outline_pen.widthF() / 2.0
                temporary_rect = temporary_rect.adjusted(-extra, -extra, extra, extra)
                self.collision_rect = temporary_rect

            if self.drop_shadow:
                # Adjust bounding rect to accommodate the drop shadow offset
                extra_x: float = abs(self.drop_shadow_effect.xOffset())
                extra_y: float = abs(self.drop_shadow_effect.yOffset())
                temporary_rect = temporary_rect.adjusted(-extra_x, -extra_y, extra_x, extra_y)

            # Unite with children's bounding rects to ensure proper collision detection
            return temporary_rect.united(self.childrenBoundingRect())

        except Exception as e:
            logging.exception("Failed to calculate boundingRect: %s", e)
            return super().boundingRect()
