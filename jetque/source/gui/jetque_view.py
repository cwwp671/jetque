# jetque/source/gui/jetque_view.py

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QRegion
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QGraphicsView, QFrame


class JetQueView(QGraphicsView):

    def __init__(self, scene, geometry, parent=None):
        super().__init__(scene, parent)
        logging.debug("Initializing.")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # Removes the window frame for a clean look.
            Qt.WindowType.WindowStaysOnTopHint |  # Keeps the window above other windows.
            Qt.WindowType.WindowTransparentForInput
        )

        # Create a widget to render graphics using OpenGL, which enables hardware acceleration.
        self.viewport_widget = QOpenGLWidget()

        # Allows the view to use OpenGL for rendering, enabling smoother graphics and better performance.
        self.setViewport(self.viewport_widget)

        # Remove the default frame around the view, creating a seamless appearance.
        self.setFrameShape(QFrame.Shape.NoFrame)  # Comment out for debugging purposes

        # Enable a translucent background for the view.
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Enable antialiasing.
        self.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Enable text antialiasing for smoother rendering of text.
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Set the viewport update mode to update the entire viewport instead of sections.
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

        # Disable the horizontal scroll bar that comes with a QGraphicsView.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Disable the vertical scroll bar that comes with a QGraphicsView.
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.available_geometry = geometry

        # Set the view size and position based on available screen space
        self.setGeometry(self.available_geometry)

        # Set the scene size and position based on available screen space
        self.setSceneRect(self.available_geometry.toRectF())

        # Display the view window. This makes the window visible on the screen.
        self.show()

        # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
        self.viewport().update()

        # Repaint the entire QGraphicsView, forcing a redraw of its contents.
        self.repaint()

    def configuration_mode(self):
        try:
            logging.debug("View switching to configuration mode.")

            # Remove Qt.WindowTransparentForInput to make the window receive input events
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint
            )

            self.show()

            self.update_mask()

            # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
            self.viewport().update()

            # Repaint the entire QGraphicsView, forcing a redraw of its contents.
            self.repaint()

        except Exception as e:
            logging.exception(f"Failed to switch to configuration mode with exception: {e}")

    def run_mode(self):
        try:
            logging.debug("Switching to active mode.")

            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |  # Removes the window frame for a clean look.
                Qt.WindowType.WindowStaysOnTopHint |  # Keeps the window above other windows.
                Qt.WindowType.WindowTransparentForInput
            )

            # Remove the default frame around the view, creating a seamless appearance.
            self.setFrameShape(QFrame.Shape.NoFrame)

            # Enable a translucent background for the view.
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            self.clearMask()

            self.show()
            # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
            self.viewport().update()

            # Repaint the entire QGraphicsView, forcing a redraw of its contents.
            self.repaint()

        except Exception as e:
            logging.exception(f"Failed to switch to active mode with exception: {e}")

    def update_mask(self):
        # Create a region that includes the circles and text items
        mask_region = QRegion()
        for anchor_point in self.scene().anchor_points:
            # Include the start circle
            start_circle_rect = self.mapFromScene(anchor_point.start_circle.sceneBoundingRect()).boundingRect()
            mask_region += QRegion(start_circle_rect)

            # Include the end circle
            end_circle_rect = self.mapFromScene(anchor_point.end_circle.sceneBoundingRect()).boundingRect()
            mask_region += QRegion(end_circle_rect)

            # Include the start text
            start_text_rect = self.mapFromScene(anchor_point.start_text.mapToScene(anchor_point.start_text.boundingRect())).boundingRect()
            mask_region += QRegion(start_text_rect)

            # Include the end text
            end_text_rect = self.mapFromScene(anchor_point.end_text.mapToScene(anchor_point.end_text.boundingRect())).boundingRect()
            mask_region += QRegion(end_text_rect)

        # Set the mask on the window
        self.setMask(mask_region)
