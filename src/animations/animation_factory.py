# src/animations/animation_factory.py

import logging
from typing import Any, Dict, Optional, Tuple

from PyQt6.QtCore import QEasingCurve, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from src.animations.animation import Animation
from src.animations.animation_label import AnimationLabel
from src.animations.dynamics import DirectionalAnimation, ParabolaAnimation, SwivelAnimation
from src.animations.statics import StationaryAnimation, PowAnimation

# Constants
TEMPORARY_WIDGET_WIDTH: float = 500.0  # Temporary width until specific overlays are passed
TEMPORARY_WIDGET_HEIGHT: float = 600.0  # Temporary height until specific overlays are passed


class AnimationFactory:
    """
    Factory class responsible for creating Animation instances based on configuration.
    """

    POSITION_MAP: Dict[str, QPointF] = {
        "Top-Left": QPointF(0.0, 0.0),
        "Top-Center": QPointF(TEMPORARY_WIDGET_WIDTH / 2.0, 0.0),
        "Top-Right": QPointF(TEMPORARY_WIDGET_WIDTH, 0.0),
        "Middle-Left": QPointF(0.0, TEMPORARY_WIDGET_HEIGHT / 2.0),
        "Middle-Center": QPointF(TEMPORARY_WIDGET_WIDTH / 2.0, TEMPORARY_WIDGET_HEIGHT / 2.0),
        "Middle-Right": QPointF(TEMPORARY_WIDGET_WIDTH, TEMPORARY_WIDGET_HEIGHT / 2.0),
        "Bottom-Left": QPointF(0.0, TEMPORARY_WIDGET_HEIGHT),
        "Bottom-Center": QPointF(TEMPORARY_WIDGET_WIDTH / 2.0, TEMPORARY_WIDGET_HEIGHT),
        "Bottom-Right": QPointF(TEMPORARY_WIDGET_WIDTH, TEMPORARY_WIDGET_HEIGHT)
    }

    DIRECTION_MAP: Dict[str, float] = {
        "Left": -1.0,
        "Right": 1.0,
        "Up": -1.0,
        "Down": 1.0
    }

    EASING_MAP: Dict[str, QEasingCurve.Type] = {
        "Linear": QEasingCurve.Type.Linear,
        "In-Quadratic": QEasingCurve.Type.InQuad,
        "Out-Quadratic": QEasingCurve.Type.OutQuad,
        "In-Out-Quadratic": QEasingCurve.Type.InOutQuad,
        "Out-In-Quadratic": QEasingCurve.Type.OutInQuad,
        "In-Cubic": QEasingCurve.Type.InCubic,
        "Out-Cubic": QEasingCurve.Type.OutCubic,
        "In-Out-Cubic": QEasingCurve.Type.InOutCubic,
        "Out-In-Cubic": QEasingCurve.Type.OutInCubic,
        "In-Quartic": QEasingCurve.Type.InQuart,
        "Out-Quartic": QEasingCurve.Type.OutQuart,
        "In-Out-Quartic": QEasingCurve.Type.InOutQuart,
        "Out-In-Quartic": QEasingCurve.Type.OutInQuart,
        "In-Quintic": QEasingCurve.Type.InQuint,
        "Out-Quintic": QEasingCurve.Type.OutQuint,
        "In-Out-Quintic": QEasingCurve.Type.InOutQuint,
        "Out-In-Quint": QEasingCurve.Type.OutInQuint,
        "In-Sinusoidal": QEasingCurve.Type.InSine,
        "Out-Sinusoidal": QEasingCurve.Type.OutSine,
        "In-Out-Sinusoidal": QEasingCurve.Type.InOutSine,
        "Out-In-Sinusoidal": QEasingCurve.Type.OutInSine,
        "In-Exponential": QEasingCurve.Type.InExpo,
        "Out-Exponential": QEasingCurve.Type.OutExpo,
        "In-Out-Exponential": QEasingCurve.Type.InOutExpo,
        "Out-In-Exponential": QEasingCurve.Type.OutInExpo,
        "In-Circular": QEasingCurve.Type.InCirc,
        "Out-Circular": QEasingCurve.Type.OutCirc,
        "In-Out-Circular": QEasingCurve.Type.InOutCirc,
        "Out-In-Circular": QEasingCurve.Type.OutInCirc,
        "In-Elastic": QEasingCurve.Type.InElastic,
        "Out-Elastic": QEasingCurve.Type.OutElastic,
        "In-Out-Elastic": QEasingCurve.Type.InOutElastic,
        "Out-In-Elastic": QEasingCurve.Type.OutInElastic,
        "In-Back": QEasingCurve.Type.InBack,
        "Out-Back": QEasingCurve.Type.OutBack,
        "In-Out-Back": QEasingCurve.Type.InOutBack,
        "Out-In-Back": QEasingCurve.Type.OutInBack,
        "In-Bounce": QEasingCurve.Type.InBounce,
        "Out-Bounce": QEasingCurve.Type.OutBounce,
        "In-Out-Bounce": QEasingCurve.Type.InOutBounce,
        "Out-In-Bounce": QEasingCurve.Type.OutInBounce
    }

    JIGGLE_MAP: Dict[str, float] = {
        "Low": 0.075,
        "Medium": 0.050,
        "High": 0.025
    }

    def build_animation(self, config: Dict[str, Any]) -> Optional[Animation]:
        """
        Builds an Animation instance based on the provided configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.

        Returns:
            Optional[Animation]: The created Animation instance or None if creation failed.
        """
        try:
            animation_type: str = config.get("type")
            sound: str = config.get("sound")
            icon: str = config.get("icon")
            text: str = config.get("text")
            duration: float = config.get("duration", 2.25)
            starting_position: QPointF = self.POSITION_MAP.get(
                config.get("starting_position", "Top-Left")
            )
            fade_in: bool = config.get("fade_in", False)
            fade_out: bool = config.get("fade_out", False)
            fade_in_percentage: float = config.get("fade_in_percentage", 0.0)
            fade_out_percentage: float = config.get("fade_out_percentage", 0.0)

            fade_in_easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("fade_in_easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )
            fade_out_easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("fade_out_easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )

            label: AnimationLabel = AnimationLabel(
                parent=self._get_parent_widget(),
                text=text,
                icon_pixmap=self._get_icon_pixmap(icon),
                font_type=config.get("font_type"),
                font_size=config.get("font_size"),
                font_color=config.get("font_color"),
                font_outline=config.get("font_outline"),
                font_outline_color=config.get("font_outline_color"),
                font_drop_shadow=config.get("font_drop_shadow"),
                font_italic=config.get("font_italic"),
                font_bold=config.get("font_bold"),
                font_underline=config.get("font_underline"),
                icon_position=config.get("icon_position")
            )

            logging.debug("Building animation of type: %s", animation_type)

            parent_type: str = self._get_animation_type_parent(animation_type)
            if parent_type == "Dynamic":
                return self._build_dynamic_animation(config, animation_type, sound, icon, text,
                                                     duration, starting_position, fade_in, fade_out,
                                                     fade_in_percentage, fade_out_percentage,
                                                     fade_in_easing_style, fade_out_easing_style, label)
            elif parent_type == "Static":
                return self._build_static_animation(config, animation_type, sound, icon, text,
                                                    duration, starting_position, fade_in, fade_out,
                                                    fade_in_percentage, fade_out_percentage,
                                                    fade_in_easing_style, fade_out_easing_style, label)
            else:
                logging.error("Unknown animation type: %s", animation_type)
                return None

        except Exception as e:
            logging.exception("Error in build_animation: %s", e)
            return None

    def _build_dynamic_animation(
            self,
            config: Dict[str, Any],
            animation_type: str,
            sound: str,
            icon: str,
            text: str,
            duration: float,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_percentage: float,
            fade_out_percentage: float,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel
    ) -> Optional[Animation]:
        """
        Builds a dynamic type Animation instance.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.
            animation_type (str): The type of animation.
            sound (str): Sound associated with the animation.
            icon (str): Icon associated with the animation.
            text (str): Text to display in the animation.
            duration (float): Duration of the animation.
            starting_position (QPointF): Starting position of the animation.
            fade_in (bool): Whether to fade in.
            fade_out (bool): Whether to fade out.
            fade_in_percentage (float): Fade in percentage.
            fade_out_percentage (float): Fade out percentage.
            fade_in_easing_style (QEasingCurve.Type): Easing style for fade in.
            fade_out_easing_style (QEasingCurve.Type): Easing style for fade out.
            label (AnimationLabel): Label associated with the animation.

        Returns:
            Optional[Animation]: The created dynamic Animation instance or None.
        """
        try:
            ending_position: QPointF = self.POSITION_MAP.get(
                config.get("ending_position", "Top-Left")
            )
            direction: Tuple[float, float] = (
                self.DIRECTION_MAP.get(config.get("horizontal_direction", "Right"), 1.0),
                self.DIRECTION_MAP.get(config.get("vertical_direction", "Down"), 1.0)
            )
            easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )

            if animation_type == "Directional":
                animation = DirectionalAnimation(
                    animation_type=animation_type,
                    sound=sound,
                    icon=icon,
                    text=text,
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_percentage=fade_in_percentage,
                    fade_out_percentage=fade_out_percentage,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    ending_position=ending_position,
                    direction=direction,
                    easing_style=easing_style
                )
            elif animation_type == "Parabola":
                vertex_position: QPointF = self._get_vertex_position()
                animation = ParabolaAnimation(
                    animation_type=animation_type,
                    sound=sound,
                    icon=icon,
                    text=text,
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_percentage=fade_in_percentage,
                    fade_out_percentage=fade_out_percentage,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    ending_position=ending_position,
                    direction=direction,
                    easing_style=easing_style,
                    vertex_position=vertex_position
                )
            elif animation_type == "Swivel":
                phase_1_percentage: float = config.get("phase_1_percentage", 0.50)
                phase_2_percentage: float = config.get("phase_2_percentage", 0.50)
                swivel_position: QPointF = self._get_swivel_position()
                animation = SwivelAnimation(
                    animation_type=animation_type,
                    sound=sound,
                    icon=icon,
                    text=text,
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_percentage=fade_in_percentage,
                    fade_out_percentage=fade_out_percentage,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    ending_position=ending_position,
                    direction=direction,
                    easing_style=easing_style,
                    phase_1_percentage=phase_1_percentage,
                    phase_2_percentage=phase_2_percentage,
                    swivel_position=swivel_position
                )
            else:
                logging.error("Unknown dynamic animation subtype: %s", animation_type)
                return None

            logging.debug("Animation built successfully: %s", animation)
            return animation

        except Exception as e:
            logging.exception("Error building dynamic animation: %s", e)
            return None

    def _build_static_animation(
            self,
            config: Dict[str, Any],
            animation_type: str,
            sound: str,
            icon: str,
            text: str,
            duration: float,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_percentage: float,
            fade_out_percentage: float,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel
    ) -> Optional[Animation]:
        """
        Builds a static type Animation instance.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.
            animation_type (str): The type of animation.
            sound (str): Sound associated with the animation.
            icon (str): Icon associated with the animation.
            text (str): Text to display in the animation.
            duration (float): Duration of the animation.
            starting_position (QPointF): Starting position of the animation.
            fade_in (bool): Whether to fade in.
            fade_out (bool): Whether to fade out.
            fade_in_percentage (float): Fade in percentage.
            fade_out_percentage (float): Fade out percentage.
            fade_in_easing_style (QEasingCurve.Type): Easing style for fade in.
            fade_out_easing_style (QEasingCurve.Type): Easing style for fade out.
            label (AnimationLabel): Label associated with the animation.

        Returns:
            Optional[Animation]: The created static Animation instance or None.
        """
        try:
            jiggle: bool = config.get("jiggle", False)
            jiggle_intensity: float = self.JIGGLE_MAP.get(config.get("jiggle_intensity", "Medium"), 0.050)

            if animation_type == "Stationary":
                animation = StationaryAnimation(
                    animation_type=animation_type,
                    sound=sound,
                    icon=icon,
                    text=text,
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_percentage=fade_in_percentage,
                    fade_out_percentage=fade_out_percentage,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    jiggle=jiggle,
                    jiggle_intensity=jiggle_intensity
                )
            elif animation_type == "Pow":
                scale_percentage: float = config.get("scale_percentage", 1.70)
                phase_1_percentage: float = config.get("phase_1_percentage", 0.50)
                phase_2_percentage: float = config.get("phase_2_percentage", 0.50)
                scale_easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                    config.get("scale_easing_style", "Linear"),
                    QEasingCurve.Type.Linear
                )
                animation = PowAnimation(
                    animation_type=animation_type,
                    sound=sound,
                    icon=icon,
                    text=text,
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_percentage=fade_in_percentage,
                    fade_out_percentage=fade_out_percentage,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    jiggle=jiggle,
                    jiggle_intensity=jiggle_intensity,
                    scale_percentage=scale_percentage,
                    phase_1_percentage=phase_1_percentage,
                    phase_2_percentage=phase_2_percentage,
                    scale_easing_style=scale_easing_style
                )
            else:
                logging.error("Unknown static animation subtype: %s", animation_type)
                return None

            logging.debug("Animation built successfully: %s", animation)
            return animation

        except Exception as e:
            logging.exception("Error building static animation: %s", e)
            return None

    @staticmethod
    def _get_animation_type_parent(animation_type: str) -> str:
        """
        Determines the parent category of the animation type.

        Args:
            animation_type (str): The type of animation.

        Returns:
            str: Parent category ("Dynamic", "Static", or "Unknown Parent Type").
        """
        dynamic_types = {"Directional", "Parabola", "Swivel"}
        static_types = {"Stationary", "Pow"}

        if animation_type in dynamic_types:
            return "Dynamic"
        elif animation_type in static_types:
            return "Static"
        else:
            return "Unknown Parent Type"

    @staticmethod
    def _get_icon_pixmap(icon: str) -> QPixmap:
        """
        Converts an icon file name to a QPixmap.

        Args:
            icon (str): The icon file name.

        Returns:
            QPixmap: The QPixmap object created from the icon.
        """
        try:
            pixmap = QPixmap(icon)
            if pixmap.isNull():
                logging.warning("Failed to load pixmap for icon: %s", icon)
            return pixmap
        except Exception as e:
            logging.exception("Error loading pixmap for icon '%s': %s", icon, e)
            return QPixmap()

    @staticmethod
    def _get_parent_widget() -> QWidget:
        """
        Retrieves the parent QWidget for the animation.

        Returns:
            QWidget: The parent QWidget.
        """
        # TODO: Implement logic to retrieve the appropriate parent QWidget
        return QWidget()

    @staticmethod
    def _get_swivel_position() -> QPointF:
        """
        Calculates the swivel position for the SwivelAnimation.

        Returns:
            QPointF: The swivel position.
        """
        # TODO: Implement logic to calculate swivel position based on what percentage of duration Phase 1 is
        return QPointF(0.0, 0.0)

    @staticmethod
    def _get_vertex_position() -> QPointF:
        """
        Calculates the vertex position for the ParabolaAnimation.

        Returns:
            QPointF: The vertex position.
        """
        # TODO: Implement logic to calculate vertex position based on starting and ending positions
        return QPointF(0.0, 0.0)
