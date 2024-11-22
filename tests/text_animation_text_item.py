# test_animation_text_item.py

import sys
import logging
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import QPointF
from src.animations.animation_text import AnimationText

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
    scene.setSceneRect(0, 0, 800, 600)  # Optional: Set the scene size

    # Set the scene background color to #D3D3D3 (Light Gray)
    scene.setBackgroundBrush(QColor("#D3D3D3"))

    # Create a QGraphicsView to visualize the scene
    view = QGraphicsView(scene)
    view.setWindowTitle("AnimationTextItem Test")
    view.setGeometry(100, 100, 800, 600)  # Optional: Set the window size and position

    # Set the view's background color to match the scene (optional but ensures consistency)
    view.setStyleSheet("background-color: #D3D3D3;")

    # Define the font for the AnimationTextItem as Helvetica, size 24, bold
    font = QFont("Helvetica", 48, QFont.Weight.Bold)

    # Create an instance of AnimationTextItem with desired properties
    text_item = AnimationText(
        text_font=font,
        text_message="AnimationTextItem Test",
        text_color="White",            # Text color set to White
        outline_color="Black",    # Text outline color set to Black
        outline_thickness=2,
        drop_shadow_offset=QPointF(3, 3),
        drop_shadow_blur_radius=4.0
    )

    # Optionally, set the position of the text item within the scene
    text_item.setPos(0, 200)

    # Add the AnimationTextItem to the scene
    scene.addItem(text_item)

    # Show the QGraphicsView window
    view.show()

    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
