# jetque/source/gui/jetque_view.py

import logging
from typing import Optional

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QRegion, QPainterPath, QPainterPathStroker
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QWidget
)


class JetQueView(QGraphicsView):
    """Custom QGraphicsView for JetQue, handling OpenGL rendering and interaction modes."""

    def __init__(
            self,
            scene: QGraphicsScene,
            geometry: QRect,
            parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize the JetQueView.

        Args:
            scene (QGraphicsScene): The graphics scene to display.
            geometry (QRect): The geometry of the available screen space.
            parent (Optional[QWidget], optional): The parent widget. Defaults to None.
        """
        super().__init__(scene, parent)
        logging.debug("Initializing.")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowTransparentForInput
        )

        # Create a widget to render graphics using OpenGL
        self.viewport_widget: QOpenGLWidget = QOpenGLWidget()
        self.setViewport(self.viewport_widget)

        # Remove the default frame around the view
        self.setFrameShape(QFrame.Shape.NoFrame)

        # Enable a translucent background and antialiasing
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Disable scroll bars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.available_geometry: QRect = geometry

        # Set geometry and scene rectangle
        self.setGeometry(self.available_geometry)
        self.setSceneRect(self.available_geometry.toRectF())

        self.show()
        self.viewport().update()
        self.repaint()

        self.padding = 5
        self.mask_path = QPainterPath()
        self.stroker = QPainterPathStroker()
        self.stroker.setWidth(self.padding * 2.0)

    def configuration_mode(self) -> None:
        """Switch the view to configuration mode, enabling user interaction within a mask."""
        try:
            logging.debug("View switching to configuration mode.")

            # Remove Qt.WindowTransparentForInput to make the window receive input events
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
            )

            self.show()
            self.update_mask()  # Use a mask to only allow anchors to be manipulated
            self.viewport().update()
            self.repaint()

        except Exception as e:
            logging.exception(f"Failed to switch to configuration mode with exception: {e}")

    def run_mode(self) -> None:
        """Switch the view to run mode, disabling user interaction."""
        try:
            logging.debug("Switching to active mode.")

            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint
                | Qt.WindowType.WindowStaysOnTopHint
                | Qt.WindowType.WindowTransparentForInput
            )

            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            self.clearMask()
            self.show()
            self.viewport().update()
            self.repaint()

        except Exception as e:
            logging.exception(f"Failed to switch to active mode with exception: {e}")

    def update_mask(self) -> None:
        # Update the window mask to include anchor points and texts.
        mask_region = QRegion()

        for anchor_point in self.scene().anchor_points:
            # Include the start circle
            start_circle_rect = self.mapFromScene(
                anchor_point.start_circle.sceneBoundingRect()
            ).boundingRect().adjusted(-5, -5, 5, 5)
            mask_region += QRegion(start_circle_rect, QRegion.RegionType.Ellipse)

            # Include the end circle
            end_circle_rect = self.mapFromScene(
                anchor_point.end_circle.sceneBoundingRect()
            ).boundingRect().adjusted(-5, -5, 5, 5)
            mask_region += QRegion(end_circle_rect, QRegion.RegionType.Ellipse)

            # Include the start text
            start_text_scene_rect = anchor_point.start_text.mapToScene(
                anchor_point.start_text.boundingRect().adjusted(-5, -5, 5, 5)
            )
            start_text_rect = self.mapFromScene(start_text_scene_rect).boundingRect().adjusted(-5, -5, 5, 5)
            mask_region += QRegion(start_text_rect, QRegion.RegionType.Rectangle)

            # Include the end text
            end_text_scene_rect = anchor_point.end_text.mapToScene(
                anchor_point.end_text.boundingRect().adjusted(-5, -5, 5, 5)
            )
            end_text_rect = self.mapFromScene(end_text_scene_rect).boundingRect().adjusted(-5, -5, 5, 5)
            mask_region += QRegion(end_text_rect, QRegion.RegionType.Rectangle)

        # Set the mask on the window
        self.setMask(mask_region)
