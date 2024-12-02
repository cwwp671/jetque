# jetque/source/gui/jetque_view.py
import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QGraphicsView, QFrame

DEFAULT_VIEW_WIDTH: int = 1920
DEFAULT_VIEW_HEIGHT: int = 1080

class JetQueView(QGraphicsView):

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        logging.debug("JetQueView: Initializing.")
        self.is_active: bool = True

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
        self.setFrameShape(QFrame.Shape.NoFrame)

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

        # TEMPORARY fixed size for the view
        self.resize(DEFAULT_VIEW_WIDTH, DEFAULT_VIEW_HEIGHT)

        self.setSceneRect(0.00, 0.00, self.width(), self.height())

        # Display the view window. This makes the window visible on the screen.
        self.show()

        # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
        self.viewport().update()

        # Repaint the entire QGraphicsView, forcing a redraw of its contents.
        self.repaint()

    def view_configuration_on(self):
        try:
            logging.debug("JetQueView: Switching to Configuration Mode.")
            self.is_active = False

            self.setWindowFlags(
                Qt.WindowType.Window |
                Qt.WindowType.WindowStaysOnTopHint
                # Add other necessary flags for Configuration Mode
            )

            self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
            self.setFrameShape(QFrame.Shape.Box)

            self.show()
            # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
            self.viewport().update()

            # Repaint the entire QGraphicsView, forcing a redraw of its contents.
            self.repaint()
            self.setFocus()
        except Exception as e:
            logging.exception(f"JetQueView: Failed to switch to Configuration Mode with exception: {e}")

    def view_active_on(self):
        try:
            logging.debug("JetQueView: Switching to Active Mode.")
            self.is_active = True

            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |  # Removes the window frame for a clean look.
                Qt.WindowType.WindowStaysOnTopHint |  # Keeps the window above other windows.
                Qt.WindowType.WindowTransparentForInput
            )

            # Remove the default frame around the view, creating a seamless appearance.
            self.setFrameShape(QFrame.Shape.NoFrame)

            # Enable a translucent background for the view.
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

            self.show()
            # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
            self.viewport().update()

            # Repaint the entire QGraphicsView, forcing a redraw of its contents.
            self.repaint()
            self.setFocus()
        except Exception as e:
            logging.exception(f"JetQueView: Failed to switch to Active Mode with exception: {e}")

