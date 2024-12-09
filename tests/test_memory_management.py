import sys
import logging
from PyQt6.QtCore import QPropertyAnimation, QRectF, QTimer, QAbstractAnimation
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem
from PyQt6.QtCore import QParallelAnimationGroup, QPointF

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

class Animation(QParallelAnimationGroup):

    def __init__(self, text_item, parent=None):
        super().__init__(parent)
        self.text_item = text_item

        # Create property animations
        self.anim1 = QPropertyAnimation(self.text_item, b'pos')
        self.anim1.setDuration(1000)
        self.anim1.setStartValue(QPointF(0, 0))
        self.anim1.setEndValue(QPointF(200, 200))

        self.anim2 = QPropertyAnimation(self.text_item, b'opacity')
        self.anim2.setDuration(1000)
        self.anim2.setStartValue(1.0)
        self.anim2.setEndValue(0.0)

        self.addAnimation(self.anim1)
        self.addAnimation(self.anim2)
        logging.debug(f"Duration of Group: {self.duration()}")

class TestApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(QRectF(0, 0, 400, 400))
        self.view.show()

        self.current_scenario = 0  # Tracks current scenario for sequential execution

        # Initialize placeholders for current animation and text item
        self.current_animation = None
        self.current_text_item = None

    def create_test_case(self):
        """Set up variables for a single test case."""
        text_item = QGraphicsTextItem("Test Text")
        text_item.setFont(QFont("Arial", 14))
        text_item.setOpacity(1.0)
        text_item.setPos(0, 0)
        self.scene.addItem(text_item)

        animation = Animation(text_item)
        return animation, text_item

    @staticmethod
    def log_variable_state(name, obj):
        """Log whether an object is still accessible."""
        try:
            if obj is None:
                logging.debug(f"{name} is None")
            else:
                logging.debug(f"{name} is still accessible: {obj}")
        except Exception as e:
            logging.error(f"Error accessing {name}: {e}")

    def start_next_scenario(self):
        """Start the next scenario based on the current scenario index."""
        self.current_scenario += 1
        if self.current_scenario == 1:
            self.run_scenario_1()
        elif self.current_scenario == 2:
            self.run_scenario_2()
        elif self.current_scenario == 3:
            self.run_scenario_3()
        else:
            logging.debug("All scenarios completed. Test concluded.")
            # Optionally, exit the application after all scenarios
            QTimer.singleShot(1000, self.app.quit)

    def run_scenario_1(self):
        """Scenario 1: Delete animation first, then the text item."""
        logging.debug("Starting Scenario 1: Delete animation first.")
        animation, text_item = self.create_test_case()

        # Store references in instance variables
        self.current_animation = animation
        self.current_text_item = text_item

        # Connect signals to named slots
        self.current_animation.finished.connect(self.scenario_1_cleanup)
        self.current_animation.start()
        QTimer.singleShot(self.current_animation.duration(), self.stop_animation_scenario_1)

    def stop_animation_scenario_1(self):
        """Stop the animation in Scenario 1."""
        if self.current_animation:
            self.current_animation.stop()

    def scenario_1_cleanup(self):
        """Cleanup for Scenario 1."""
        self.log_variable_state("animation", self.current_animation)
        self.log_variable_state("text_item", self.current_text_item)

        try:
            if self.current_animation:
                self.current_animation.deleteLater()
                logging.debug("Animation deleted using deleteLater.")
        except Exception as e:
            logging.error(f"Error deleting animation: {e}")

        try:
            if self.current_text_item:
                self.current_text_item.deleteLater()
                logging.debug("Text item deleted using deleteLater.")
        except Exception as e:
            logging.error(f"Error deleting text item: {e}")

        # Disconnect the signal to remove the reference
        self.current_animation.finished.disconnect(self.scenario_1_cleanup)

        # Remove references
        self.current_animation = None
        self.current_text_item = None

        # Log the state after deletion, then move to the next scenario
        QTimer.singleShot(10000, self.log_and_proceed_scenario_1)

    def log_and_proceed_scenario_1(self):
        """Log variable states after cleanup for Scenario 1 and proceed."""
        logging.debug("Scenario 1 post-cleanup status:")
        self.log_variable_state("animation (post-cleanup)", self.current_animation)
        self.log_variable_state("text_item (post-cleanup)", self.current_text_item)

        # Start the next scenario
        self.start_next_scenario()

    def run_scenario_2(self):
        """Scenario 2: Delete text item first, then the animation."""
        logging.debug("Starting Scenario 2: Delete text item first.")
        animation, text_item = self.create_test_case()

        # Store references in instance variables
        self.current_animation = animation
        self.current_text_item = text_item

        # Connect signals to named slots
        self.current_animation.finished.connect(self.scenario_2_cleanup)
        self.current_animation.start()
        QTimer.singleShot(self.current_animation.duration(), self.stop_animation_scenario_2)

    def stop_animation_scenario_2(self):
        """Stop the animation in Scenario 2."""
        if self.current_animation:
            self.current_animation.stop()

    def scenario_2_cleanup(self):
        """Cleanup for Scenario 2."""
        self.log_variable_state("animation", self.current_animation)
        self.log_variable_state("text_item", self.current_text_item)

        try:
            if self.current_text_item:
                self.current_text_item.deleteLater()
                logging.debug("Text item deleted using deleteLater.")
        except Exception as e:
            logging.error(f"Error deleting text item: {e}")

        try:
            if self.current_animation:
                self.current_animation.deleteLater()
                logging.debug("Animation deleted using deleteLater.")
        except Exception as e:
            logging.error(f"Error deleting animation: {e}")

        # Disconnect the signal to remove the reference
        self.current_animation.finished.disconnect(self.scenario_2_cleanup)

        # Remove references
        self.current_animation = None
        self.current_text_item = None

        # Log the state after deletion, then move to the next scenario
        QTimer.singleShot(10000, self.log_and_proceed_scenario_2)

    def log_and_proceed_scenario_2(self):
        """Log variable states after cleanup for Scenario 2 and proceed."""
        logging.debug("Scenario 2 post-cleanup status:")
        self.log_variable_state("animation (post-cleanup)", self.current_animation)
        self.log_variable_state("text_item (post-cleanup)", self.current_text_item)

        # Start the next scenario
        self.start_next_scenario()

    def run_scenario_3(self):
        """Scenario 3: Use DeletionPolicy to let PyQt handle cleanup."""
        logging.debug("Starting Scenario 3: Using DeletionPolicy.DeleteWhenStopped.")
        animation, text_item = self.create_test_case()

        # Store references in instance variables
        self.current_animation = animation
        self.current_text_item = text_item

        # Connect signals to named slots
        self.current_animation.finished.connect(self.scenario_3_cleanup)
        self.current_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        QTimer.singleShot(self.current_animation.duration(), self.stop_animation_scenario_3)

    def stop_animation_scenario_3(self):
        """Stop the animation in Scenario 3."""
        if self.current_animation:
            self.current_animation.stop()

    def scenario_3_cleanup(self):
        """Cleanup for Scenario 3."""
        self.log_variable_state("animation", self.current_animation)
        self.log_variable_state("text_item", self.current_text_item)

        # No manual deletion; let PyQt handle everything
        logging.debug("No manual deletion; PyQt is handling cleanup for Scenario 3.")

        # Disconnect the signal to remove the reference
        self.current_animation.finished.disconnect(self.scenario_3_cleanup)

        # Remove references
        self.current_animation = None
        self.current_text_item = None

        # Log the state after deletion
        QTimer.singleShot(10000, self.log_and_proceed_scenario_3)

    def log_and_proceed_scenario_3(self):
        """Log variable states after cleanup for Scenario 3 and proceed."""
        logging.debug("Scenario 3 post-cleanup status:")
        self.log_variable_state("animation (post-cleanup)", self.current_animation)
        self.log_variable_state("text_item (post-cleanup)", self.current_text_item)

        # Start the next scenario
        self.start_next_scenario()

    def log_and_proceed(self, scenario_name, animation, text_item):
        """Log variable states after cleanup and proceed to the next scenario."""
        logging.debug(f"{scenario_name} post-cleanup status:")
        self.log_variable_state("animation (post-cleanup)", animation)
        self.log_variable_state("text_item (post-cleanup)", text_item)

        # Start the next scenario
        self.start_next_scenario()

    def run(self):
        """Start the first scenario."""
        self.start_next_scenario()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    test_app = TestApp()
    test_app.run()
