# src/animations/animation_controller.py

import logging
from typing import Any, Dict, List

from PyQt6.QtCore import QObject, QTimer, pyqtSlot
from PyQt6.QtWidgets import QWidget

from src.animations.animation import Animation
from src.animations.animation_factory import AnimationFactory


class AnimationController(QObject):
    """
    Controller class responsible for managing all animations within the application.

    Attributes:
        dynamic_animations (Dict[str, List[Animation]]):
            Dictionary containing lists of active dynamic animations categorized by type.
        static_animations (Dict[str, List[Animation]]):
            Dictionary containing lists of active static animations categorized by type.
        detect_intersections_timer (QTimer):
            Timer to periodically detect intersections between animations.
    """

    def __init__(self, parent: QWidget, config: Dict[str, Any]) -> None:
        """
        Initializes the AnimationController with the given parent widget and configuration.

        Args:
            parent (QWidget): The parent widget for the controller.
            config (Dict[str, Any]): Configuration dictionary for animations.
        """
        super().__init__(parent)
        self.dynamic_animations: Dict[str, List[Animation]] = {
            "directional_animations": [],
            "parabola_animations": [],
            "swivel_animations": []
        }
        self.static_animations: Dict[str, List[Animation]] = {
            "stationary_animations": [],
            "pow_animations": []
        }
        self.config = config
        self.animation_factory = AnimationFactory()
        self.detect_intersections_timer = QTimer(self)
        self.detect_intersections_timer.setInterval(1000)  # Interval in milliseconds
        self.detect_intersections_timer.timeout.connect(self._detect_intersections)
        self.detect_intersections_timer.start()
        logging.debug("AnimationController initialized with config: %s", config)

    def setup_animation(self, animation_creation_attributes: Dict[str, Any]) -> None:
        """
        Sets up an animation based on the provided creation attributes.

        Args:
            animation_creation_attributes (Dict[str, Any]): Attributes for creating the animation.
        """
        try:
            animation = self.animation_factory.build_animation(animation_creation_attributes)
            if animation:
                self.start_animation(animation)
                logging.info("Animation setup and started: %s", animation)
            else:
                logging.warning("Failed to build animation with attributes: %s", animation_creation_attributes)
        except Exception as e:
            logging.exception("Error in setup_animation: %s", e)

    def start_animation(self, animation: Animation) -> None:
        """
        Starts the given animation and adds it to the appropriate active animations list.

        Args:
            animation (Animation): The animation instance to start.
        """
        try:
            animation.play()
            animation.finished.connect(lambda: self.handle_animation_finished(animation))
            animation_type = type(animation).__name__.lower()
            if isinstance(animation, Animation):
                if hasattr(self.dynamic_animations, animation_type + '_animations'):
                    self.dynamic_animations[animation_type + '_animations'].append(animation)
                elif hasattr(self.static_animations, animation_type + '_animations'):
                    self.static_animations[animation_type + '_animations'].append(animation)
                logging.info("Animation started: %s", animation)
            else:
                logging.warning("Attempted to start invalid animation type: %s", type(animation))
        except Exception as e:
            logging.exception("Error in start_animation: %s", e)

    def stop_animation(self, animation: Animation) -> None:
        """
        Stops the given animation and removes it from the active animations list.

        Args:
            animation (Animation): The animation instance to stop.
        """
        try:
            animation.stop()
            self.clean_up_animation(animation)
            logging.info("Animation stopped: %s", animation)
        except Exception as e:
            logging.exception("Error in stop_animation: %s", e)

    def clean_up_animation(self, animation: Animation) -> None:
        """
        Cleans up the animation by removing it from active lists and deleting it safely.

        Args:
            animation (Animation): The animation instance to clean up.
        """
        try:
            animation_type = type(animation).__name__.lower()
            removed = False
            if animation in self.dynamic_animations.get(f"{animation_type}_animations", []):
                self.dynamic_animations[f"{animation_type}_animations"].remove(animation)
                removed = True
            elif animation in self.static_animations.get(f"{animation_type}_animations", []):
                self.static_animations[f"{animation_type}_animations"].remove(animation)
                removed = True
            if removed:
                animation.deleteLater()
                logging.debug("Animation cleaned up and deleted: %s", animation)
            else:
                logging.warning("Attempted to clean up animation not found in active lists: %s", animation)
        except Exception as e:
            logging.exception("Error in clean_up_animation: %s", e)

    @pyqtSlot()
    def handle_animation_finished(self, animation: Animation) -> None:
        """
        Handles the cleanup process when an animation finishes.

        Args:
            animation (Animation): The animation instance that has finished.
        """
        try:
            self.clean_up_animation(animation)
            logging.debug("Handled animation finished: %s", animation)
        except Exception as e:
            logging.exception("Error in handle_animation_finished: %s", e)

    @staticmethod
    def _handle_intersection(animation1: Animation, animation2: Animation) -> None:
        """
        Handles the intersection between two animations.

        Args:
            animation1 (Animation): The first intersecting animation.
            animation2 (Animation): The second intersecting animation.
        """
        try:
            # TODO: Intersection handling logic based on animation type
            logging.info("Handling intersection between %s and %s", animation1, animation2)
        except Exception as e:
            logging.exception("Error in handle_intersection: %s", e)

    @staticmethod
    def _detect_intersections() -> None:
        """
        Detects intersections between active animations and handles them accordingly.
        """
        try:
            # TODO: Check animations of the same type for intersections
            logging.debug("Intersection detection completed.")
        except Exception as e:
            logging.exception("Error in detect_intersections: %s", e)

    @staticmethod
    def _are_intersecting(label1: QObject, label2: QObject) -> bool:
        """
        Determines if two animation labels are intersecting based on their geometry.

        Args:
            label1 (QObject): The first animation label.
            label2 (QObject): The second animation label.

        Returns:
            bool: True if the labels are intersecting, False otherwise.
        """
        try:
            rect1 = label1.geometry()
            rect2 = label2.geometry()
            intersecting = rect1.intersects(rect2)
            logging.debug("Intersection check between %s and %s: %s", label1, label2, intersecting)
            return intersecting
        except Exception as e:
            logging.exception("Error in are_intersecting: %s", e)
            return False
