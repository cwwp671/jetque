# test_animation_text_item.py

import sys
import logging
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QPointF, QEasingCurve, QUrl, QAbstractAnimation
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

    # Set the scene background color to #D3D3D3 (Light Gray)
    scene.setBackgroundBrush(QColor("#D3D3D3"))

    # Create a QGraphicsView to visualize the scene
    view = QGraphicsView(scene)
    view.setWindowTitle("SwivelAnimation Test")
    view.setGeometry(100, 100, 1920, 1080)  # Optional: Set the window size and position

    # Set the view's background color to match the scene (optional but ensures consistency)
    view.setStyleSheet("background-color: #D3D3D3;")

    # Define the font for the AnimationTextItem as Helvetica, size 48, bold
    font = QFont("Helvetica", 16, QFont.Weight.Bold)

    # Create an instance of AnimationTextItem with desired properties
    text_item = AnimationTextItem(
        font=font,
        text_message="Swivel Animation Test",
        text_color="White",            # Text color set to White
        text_outline_color="Black",    # Text outline color set to Black
        text_outline_strength=2,
        text_drop_shadow_offset=QPointF(3, 3),
        text_drop_shadow_blur_radius=4.0
    )

    # Add the AnimationTextItem to the scene
    scene.addItem(text_item)

    # Show the QGraphicsView window
    view.show()

    # Set up the sound effect (ensure the sound file exists or handle accordingly)
    sound = QSoundEffect()
    sound.setSource(QUrl.fromLocalFile("path/to/sound.wav"))  # Replace with a valid sound file path
    sound.setVolume(0.5)  # Volume: 0.0 to 1.0
    logging.debug(f"Text Height:{text_item.bounding_rect().height()}")
    # Define animation parameters
    animation_type = "Swivel"
    duration = 10000  # Total duration in milliseconds
    starting_position = QPointF(960, 540)
    fade_in = True
    fade_out = True
    fade_in_duration = 1000
    fade_out_duration = 5000
    fade_out_delay = 5000
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

    # Start the animation
    swivel_animation.start()

    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
