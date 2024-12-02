# src/animations/animation_point_f.py

from PyQt6.QtCore import QPointF


class AnimationPointF(QPointF):
    """
    AnimationPointF extends QPointF by adding a key_value attribute.

    Attributes:
        key_value (float): An additional value associated with the point.
    """

    key_value: float

    def __init__(self, x: float = 0.0, y: float = 0.0, key_value: float = 0.0) -> None:
        """
        Initialize an AnimationPointF instance.

        Args:
            x (float): The x-coordinate of the point. Defaults to 0.0.
            y (float): The y-coordinate of the point. Defaults to 0.0.
            key_value (float): The key value associated with the point. Defaults to DEFAULT_KEY_VALUE.
        """
        super().__init__(x, y)
        self.key_value = key_value
