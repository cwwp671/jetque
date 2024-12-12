import logging
import math
from typing import Optional

from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QColor, QPixmap, QImage, QPainter, QPen
from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QGraphicsPixmapItem,
    QGraphicsItem,
)


class JQGraphicsPixmapItem(QGraphicsPixmapItem):
    """
    Custom QGraphicsPixmapItem with optional outline and drop shadow effects.

    Attributes:
        file_path (str): Path to the image file.
        outline (bool): Whether to add an outline to the image.
        outline_pen (QPen): Pen used for the outline.
        drop_shadow (bool): Whether to add a drop shadow.
        drop_shadow_offset (QPointF): Offset of the drop shadow.
        drop_shadow_blur_radius (float): Blur radius of the drop shadow.
        drop_shadow_color (QColor): Color of the drop shadow.
        alignment (str): If the item is on the left or right of the Parent graphics item.
        drop_shadow_effect (QGraphicsDropShadowEffect): Drop shadow effect applied.
        collision_rect (QRectF): Collision rectangle (not including drop shadow).
        _bounding_rect (QRectF): Cached bounding rectangle including drop shadow.
        original_pixmap (QPixmap): The originally loaded (or outlined) pixmap before scaling.
    """

    def __init__(
            self,
            file_path: str,
            outline: bool = False,
            outline_pen: QPen = QPen(Qt.GlobalColor.black, 2.0),
            drop_shadow: bool = False,
            drop_shadow_offset: QPointF = QPointF(3.5, 6.1),
            drop_shadow_blur_radius: float = 7.0,
            drop_shadow_color: QColor = QColor(0, 0, 0, 191),
            alignment: str = "left",
            parent: Optional[QGraphicsItem] = None,
    ) -> None:
        super().__init__(parent)

        self.file_path: str = file_path
        self.outline: bool = outline
        self.outline_pen: QPen = outline_pen
        self.drop_shadow: bool = drop_shadow
        self.drop_shadow_offset: QPointF = drop_shadow_offset
        self.drop_shadow_blur_radius: float = drop_shadow_blur_radius
        self.drop_shadow_color: QColor = drop_shadow_color
        self.alignment: str = alignment
        self.drop_shadow_effect: QGraphicsDropShadowEffect = QGraphicsDropShadowEffect()
        self.collision_rect: QRectF = QRectF()
        self._bounding_rect: QRectF = QRectF()
        self.original_pixmap: QPixmap = QPixmap()

        try:
            # Load the pixmap with optional outline
            if self.outline:
                pixmap = self._add_outline_to_image()
            else:
                pixmap = QPixmap(self.file_path)

            self.original_pixmap = pixmap
            self.setPixmap(self.original_pixmap)

            # Apply drop shadow effect if requested
            if self.drop_shadow:
                self.drop_shadow_effect.setOffset(self.drop_shadow_offset)
                self.drop_shadow_effect.setBlurRadius(self.drop_shadow_blur_radius)
                self.drop_shadow_effect.setColor(self.drop_shadow_color)
                self.setGraphicsEffect(self.drop_shadow_effect)

            self.prepareGeometryChange()
            self._bounding_rect = self.calculate_bounding_rect()

            # Set the origin point to the center for transformations
            self.setTransformOriginPoint(
                self.collision_rect.width() / 2.0,
                self.collision_rect.height() / 2.0,
                )

        except Exception as e:
            logging.exception("Failed to initialize JQGraphicsPixmapItem: %s", e)

    def boundingRect(self) -> QRectF:
        return self._bounding_rect

    def setParentItem(self, parent: Optional[QGraphicsItem]) -> None:
        super().setParentItem(parent)
        self._scale_and_position_pixmap_item()

    def calculate_bounding_rect(self) -> QRectF:
        try:
            # Start with the base bounding rect from the current pixmap
            temporary_rect: QRectF = super().boundingRect()

            # The collision_rect should be the pixmap plus optional outline
            if self.outline:
                # Adjust bounding rect to accommodate the outline width
                extra: float = self.outline_pen.widthF() / 2.0
                temporary_rect = temporary_rect.adjusted(-extra, -extra, extra, extra)

            self.collision_rect = temporary_rect

            # Adjust for drop shadow if any
            if self.drop_shadow:
                extra_x: float = abs(self.drop_shadow_effect.xOffset())
                extra_y: float = abs(self.drop_shadow_effect.yOffset())
                temporary_rect = temporary_rect.adjusted(-extra_x, -extra_y, extra_x, extra_y)

            # Combine with children's bounding rect if needed
            return temporary_rect.united(self.childrenBoundingRect())

        except Exception as e:
            logging.exception("Failed to calculate boundingRect: %s", e)
            return super().boundingRect()

    def _add_outline_to_image(self) -> QPixmap:
        original_image: QImage = QImage(self.file_path)

        if original_image.format() != QImage.Format.Format_ARGB32_Premultiplied:
            original_image = original_image.convertToFormat(QImage.Format.Format_ARGB32_Premultiplied)

        local_pen: QPen = QPen(self.outline_pen)
        local_pen.setWidthF(local_pen.widthF() * 2.0)
        pen_width: float = local_pen.widthF()
        half_pen_width: float = pen_width / 2.0
        padding: int = math.ceil(half_pen_width)
        under_padding: float = (1.0 - (padding - half_pen_width)) / 2.0
        if under_padding.is_integer():
            under_padding = 0.0

        new_width: int = original_image.width() + 2 * padding
        new_height: int = original_image.height() + 2 * padding

        new_image: QImage = QImage(new_width, new_height, QImage.Format.Format_ARGB32_Premultiplied)
        new_image.fill(Qt.GlobalColor.transparent)

        painter: QPainter = QPainter(new_image)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setPen(local_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            rect: QRectF = QRectF(
                padding - under_padding,
                padding - under_padding,
                original_image.width(),
                original_image.height(),
                )

            painter.drawRect(rect)
            painter.drawImage(QPointF(padding, padding), original_image)
        except Exception as e:
            logging.exception("Failed to add outline to image: %s", e)
        finally:
            painter.end()

        outlined_pixmap: QPixmap = QPixmap.fromImage(new_image)
        return outlined_pixmap

    def _scale_and_position_pixmap_item(self) -> None:
        """
        Scale and position the pixmap item relative to the text item by physically resizing the pixmap.
        """
        try:
            if not self.parentItem():
                return

            # Get the parent's collision rect (e.g., text rect)
            text_rect: QRectF = self.parentItem().collision_rect
            text_height: float = text_rect.height()

            # Get original pixmap size from our stored original_pixmap
            orig_height: float = float(self.original_pixmap.height())
            if orig_height == 0:
                return

            # Calculate scale factor
            scale_factor: float = text_height / orig_height

            # Scale the original pixmap physically
            scaled_width = int(self.original_pixmap.width() * scale_factor)
            scaled_height = int(self.original_pixmap.height() * scale_factor)
            scaled_pixmap = self.original_pixmap.scaled(
                scaled_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Set the newly scaled pixmap
            self.prepareGeometryChange()
            self.setPixmap(scaled_pixmap)

            # Recalculate bounding and collision rects
            self._bounding_rect = self.calculate_bounding_rect()

            # Update transform origin point
            self.setTransformOriginPoint(
                self.collision_rect.width() / 2.0,
                self.collision_rect.height() / 2.0,
                )

            # Position the pixmap relative to the text
            scaled_pixmap_width: float = self.collision_rect.width()
            x_padding: float = 5.0

            if self.alignment.lower() == "left":
                # Position x to the left of the text
                x_position = text_rect.x() - scaled_pixmap_width - x_padding
            else:
                # Position x to the right of the text
                x_position = text_rect.x() + text_rect.width() + x_padding

            # Position y with the text
            y_position = text_rect.y()

            # Set the position of the pixmap
            self.setPos(x_position, y_position)

        except Exception as e:
            logging.exception("Failed to scale and position pixmap item: %s", e)
