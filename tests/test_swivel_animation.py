# tests/test_animation_object_swivel.py

import sys
import logging

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QFrame
from PyQt6.QtGui import QFont, QColor, QPen, QPixmap, QPainter
from PyQt6.QtCore import QPointF, QEasingCurve, QUrl, Qt
from PyQt6.QtMultimedia import QSoundEffect

from jetque.source.animations.animation_font import AnimationFont
from jetque.source.animations.animation_text import AnimationText
from jetque.source.animations.dynamics.swivel_animation import SwivelAnimation

# Constants
DEFAULT_WINDOW_WIDTH: int = 1920
DEFAULT_WINDOW_HEIGHT: int = 1080
DEFAULT_ANIMATION_DURATION: int = 10000  # milliseconds
DEFAULT_FONT_SIZE: int = 72

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def main():

    # Create an instance of QApplication, which is the core application object in PyQt6.
    # It manages application-wide resources and settings.
    app = QApplication(sys.argv)

    # Create an OpenGL widget to render graphics using OpenGL. This serves as the viewport
    # for the QGraphicsView, enabling hardware-accelerated rendering.
    opengl_widget = QOpenGLWidget()

    # Create a QGraphicsScene, which manages and stores all the 2D graphical items to be
    # displayed in the QGraphicsView.
    scene = QGraphicsScene()

    # Create a QGraphicsView to display the QGraphicsScene. The view provides the window
    # and user interaction functionality for the scene.
    view = QGraphicsView(scene)

    # Set the OpenGL widget as the viewport for the QGraphicsView. This allows the view
    # to use OpenGL for rendering, enabling smoother graphics and better performance.
    view.setViewport(opengl_widget)

    # Set window flags to remove the default window decorations (e.g., title bar, borders)
    # and to make the window always stay on top of other windows.
    view.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |  # Removes the window frame for a clean look.
        Qt.WindowType.WindowStaysOnTopHint |  # Keeps the window above other windows.
        Qt.WindowType.WindowTransparentForInput
    )

    # Remove the default frame around the QGraphicsView, creating a seamless appearance.
    view.setFrameShape(QFrame.Shape.NoFrame)

    # Enable a translucent background for the QGraphicsView. This allows the window to
    # appear semi-transparent if supported by the system.
    view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    # Make the QGraphicsView transparent to mouse events. This is useful if you want the
    # mouse events to pass through to underlying widgets or applications.
    # view.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    # Enable antialiasing for smoother rendering of edges and shapes.
    view.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    # Enable text antialiasing for smoother rendering of text.
    view.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

    # Set the viewport update mode to update the entire viewport, ensuring that
    # all graphics are re-rendered when needed. This may be necessary for OpenGL rendering.
    view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    # Disable the horizontal scroll bar to keep the view fixed and uncluttered.
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Disable the vertical scroll bar to keep the view fixed and uncluttered.
    view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    # Set the fixed size of the QGraphicsView window. Replace `DEFAULT_WINDOW_WIDTH` and
    # `DEFAULT_WINDOW_HEIGHT` with appropriate constants or variables.
    view.setFixedSize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    # Display the QGraphicsView window. This makes the window visible on the screen.
    view.show()

    # Trigger an update of the viewport, ensuring that all graphical content is refreshed.
    view.viewport().update()

    # Repaint the entire QGraphicsView, forcing a redraw of its contents.
    view.repaint()

    logging.debug(f"scene width: {scene.width()}, scene height: {scene.height()}")
    logging.debug(f"view width: {view.width()}, view height: {view.height()}")
    logging.debug(f"viewport width: {view.viewport().width()}, viewport height: {view.viewport().height()}")

    # Define the font for the AnimationTextItem
    text_font = AnimationFont(
        font_type="Helvetica",
        font_size=DEFAULT_FONT_SIZE,
        font_weight=QFont.Weight.Normal,
        font_capitalization=QFont.Capitalization.MixedCase,
        font_stretch=QFont.Stretch.Unstretched,
        font_letter_spacing=0.0,
        font_word_spacing=0.0,
        font_italic=False,
        font_kerning=True,
        font_overline=False,
        font_strikethrough=False,
        font_underline=False
    )

    # Define the outline/stroke for the AnimationTextItem
    text_outline_pen = QPen(
        QColor("black"),
        2,
        Qt.PenStyle.SolidLine,
        Qt.PenCapStyle.FlatCap,
        Qt.PenJoinStyle.BevelJoin
    )

    # Create an instance of AnimationTextItem with desired properties
    text_item = AnimationText(
        text_font=text_font,
        text_message="Swivel Animation Test",
        text_color=QColor("white"),
        outline=True,
        outline_pen=text_outline_pen,
        drop_shadow=True,
        drop_shadow_offset=QPointF(-3.5, 6.1),
        drop_shadow_blur_radius=7.0,
        drop_shadow_color=QColor("0, 0, 0, 191"),
        icon=True,
        icon_pixmap=QPixmap("C:/intellij-projects/jetque/jetque/resources/test_animation_icon.jpg"),
        icon_alignment="left",
        parent=None
    )

    # Add the AnimationTextItem to the scene
    scene.addItem(text_item)

    # Set up the sound effect (ensure the sound file exists or handle accordingly)
    sound = QSoundEffect()
    sound.setSource(QUrl.fromLocalFile("path/to/sound.wav"))  # Replace with a valid sound file path
    sound.setVolume(0.5)  # Volume: 0.0 to 1.0

    logging.debug(f"obj width: {text_item.boundingRect().width()}, obj height: {text_item.boundingRect().height()}")

    # Define animation parameters
    animation_type = "Swivel"
    duration = DEFAULT_ANIMATION_DURATION  # Total duration in milliseconds
    starting_position = QPointF(960, 540)
    fade_in = True
    fade_out = True
    fade_in_duration = int(float(duration) * 0.10)
    fade_out_duration = int(float(duration) * 0.10)
    fade_out_delay = duration - fade_out_duration
    fade_in_easing_style = QEasingCurve.Type.Linear
    fade_out_easing_style = QEasingCurve.Type.Linear
    ending_position = QPointF(1672, 229)
    easing_style = QEasingCurve.Type.Linear
    phase_1_duration = int(float(duration) / 2.00)
    phase_2_duration = duration - phase_1_duration
    swivel_position = QPointF(1192, 229)

    # Create an instance of SwivelAnimation
    swivel_animation = SwivelAnimation(
        animation_type=animation_type,
        sound=sound,
        duration=duration,
        starting_position=starting_position,
        fade_in=fade_in,
        fade_out=fade_out,
        fade_in_duration=fade_in_duration,
        fade_out_duration=fade_out_duration,
        fade_out_delay=fade_out_delay,
        fade_in_easing_style=fade_in_easing_style,
        fade_out_easing_style=fade_out_easing_style,
        animation_object=text_item,
        ending_position=ending_position,
        easing_style=easing_style,
        phase_1_duration=phase_1_duration,
        phase_2_duration=phase_2_duration,
        swivel_position=swivel_position
    )

    text_item.setParent(swivel_animation)

    # Start the animation
    swivel_animation.start()

    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
