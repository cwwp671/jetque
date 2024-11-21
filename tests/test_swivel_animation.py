# test_animation_text_item.py

import sys
import logging
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QFrame
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtCore import QPointF, QEasingCurve, QUrl, Qt
from PyQt6.QtMultimedia import QSoundEffect

from src.animations.animation_text_item import AnimationTextItem
from src.animations.dynamics.swivel_animation import SwivelAnimation

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # Initialize the QApplication
    app = QApplication(sys.argv)

    # Create a QGraphicsScene
    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 1920, 1080)  # Optional: Set the scene size

    # Create a QGraphicsView to visualize the scene
    view = QGraphicsView(scene)
    # view.setWindowTitle("SwivelAnimation Test")
    view.setGeometry(100, 100, 1920, 1080)  # Optional: Set the window size and position
    view.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    view.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
    view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
    view.verticalScrollBar().setUpdatesEnabled(False)
    view.verticalScrollBar().setVisible(False)
    view.horizontalScrollBar().setUpdatesEnabled(False)
    view.horizontalScrollBar().setVisible(False)

    # Set the view background
    # view.setBackgroundBrush(QColor(Qt.GlobalColor.transparent))

    view.setFrameShape(QFrame.Shape.NoFrame)

    # Enable window transparency
    view.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    view.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    view.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    view.setWindowFlags(
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint
    )

    # Ensure the viewport is transparent
    view.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    view.viewport().setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    view.viewport().setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)

    # Define the font for the AnimationTextItem as Helvetica, size 48, bold
    font = QFont("Helvetica", 36, -1, False)

    # Create an instance of AnimationTextItem with desired properties
    text_item = AnimationTextItem(
        text_font=font,
        text_message="Swivel Animation Test",
        text_color=QColor("white"),
        outline=True,
        outline_thickness=2,
        outline_color=QColor("black"),
        outline_pen_style=Qt.PenStyle.SolidLine,
        outline_pen_cap_style=Qt.PenCapStyle.FlatCap,
        outline_pen_join_style=Qt.PenJoinStyle.BevelJoin,
        drop_shadow=True,
        drop_shadow_offset=QPointF(-3.5, 6.1),
        drop_shadow_blur_radius=7.0,
        drop_shadow_color=QColor("0, 0, 0, 191"),
        parent=None
    )

    # Add the AnimationTextItem to the scene
    scene.addItem(text_item)

    # Show the QGraphicsView window
    view.show()

    # Set up the sound effect (ensure the sound file exists or handle accordingly)
    sound = QSoundEffect()
    sound.setSource(QUrl.fromLocalFile("path/to/sound.wav"))  # Replace with a valid sound file path
    sound.setVolume(0.5)  # Volume: 0.0 to 1.0

    # Define animation parameters
    animation_type = "Swivel"
    duration = 10000  # Total duration in milliseconds
    starting_position = QPointF(960, 540)
    fade_in = True
    fade_out = True
    fade_in_duration = 1000
    fade_out_duration = 1000
    fade_out_delay = 9000
    fade_in_easing_style = QEasingCurve.Type.Linear
    fade_out_easing_style = QEasingCurve.Type.Linear
    ending_position = QPointF(1672, 229)
    easing_style = QEasingCurve.Type.Linear
    phase_1_duration = 5000
    phase_2_duration = 5000
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
        label=text_item,
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
