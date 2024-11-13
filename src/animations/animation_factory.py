# src/animations/animation_factory.py

import logging
from typing import Any, Dict, Optional, List

from PyQt6.QtCore import QEasingCurve, QPointF, QUrl, QObject
from PyQt6.QtGui import QPixmap, QFontDatabase, QFont
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QWidget

from src.animations.animation import Animation
from src.animations.OLD_animation_label import AnimationLabel
from src.animations.animation_point_f import AnimationPointF
from src.animations.dynamics.directional_animation import DirectionalAnimation
from src.animations.dynamics.parabola_animation import ParabolaAnimation
from src.animations.dynamics.swivel_animation import SwivelAnimation
from src.animations.statics.stationary_animation import StationaryAnimation
from src.animations.statics.pow_animation import PowAnimation

# Constants
DEFAULT_FRAMERATE: int = 60
TEMPORARY_WIDGET_WIDTH: float = 500.0  # Temporary width until specific overlays are passed
TEMPORARY_WIDGET_HEIGHT: float = 600.0  # Temporary height until specific overlays are passed


class AnimationFactory(QObject):
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

    JIGGLE_MAP: Dict[str, int] = {
        "Low": 75,
        "Medium": 50,
        "High": 25
    }

    CAPITALIZATION_MAP: Dict[str, QFont.Capitalization] = {
        "MixedCase": QFont.Capitalization.MixedCase,
        "AllLowercase": QFont.Capitalization.AllLowercase,
        "AllUppercase": QFont.Capitalization.AllUppercase,
        "Capitalize": QFont.Capitalization.Capitalize,
        "SmallCaps": QFont.Capitalization.SmallCaps
    }

    STRETCH_MAP: Dict[str, QFont.Stretch] = {
        "Unstretched": QFont.Stretch.Unstreched,
        "AnyStretch": QFont.Stretch.AnyStretch,
        "UltraCondensed": QFont.Stretch.UltraCondensed,
        "ExtraCondensed": QFont.Stretch.ExtraCondensed,
        "Condensed": QFont.Stretch.Condensed,
        "SemiCondensed": QFont.Stretch.SemiCondensed,
        "SemiExpanded": QFont.Stretch.SemiExpanded,
        "Expanded": QFont.Stretch.Expanded,
        "ExtraExpanded": QFont.Stretch.ExtraExpanded,
        "UltraExpanded": QFont.Stretch.UltraExpanded,
    }

    WEIGHT_MAP: Dict[str, QFont.Weight] = {
        "Normal": QFont.Weight.Normal,
        "Thin": QFont.Weight.Thin,
        "ExtraLight": QFont.Weight.ExtraLight,
        "Light": QFont.Weight.Light,
        "Medium": QFont.Weight.Medium,
        "DemiBold": QFont.Weight.DemiBold,
        "Bold": QFont.Weight.Bold,
        "ExtraBold": QFont.Weight.ExtraBold,
        "Black": QFont.Weight.Black,
    }

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # noinspection PyArgumentList
        self.font_database: QFontDatabase = QFontDatabase()

    def build_animation(self, config: Dict[str, Any]) -> Optional[Animation]:
        """
        Builds an Animation instance based on the provided configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.

        Returns:
            Optional[Animation]: The created Animation instance or None if creation failed.
        """
        try:
            parent = self.parent()
            animation_type: str = config.get("type")
            sound: QSoundEffect = self._get_sound_effect(config.get("sound"))
            duration: int = int(config.get("duration", 2.25) * 1000)
            starting_position: QPointF = self.POSITION_MAP.get(
                config.get("starting_position", "Top-Left")
            )
            fade_in: bool = config.get("fade_in", False)
            fade_out: bool = config.get("fade_out", False)
            fade_in_percentage: float = config.get("fade_in_percentage", 0.0)
            fade_in_duration: int = self._get_phase_duration(duration, fade_in_percentage)
            fade_out_percentage: float = config.get("fade_out_percentage", 0.0)
            fade_out_duration: int = self._get_phase_duration(duration, fade_out_percentage)
            fade_out_delay: int = self._get_fade_out_delay(duration, fade_out_duration)

            fade_in_easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("fade_in_easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )
            fade_out_easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("fade_out_easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )

            label: AnimationLabel = AnimationLabel(
                text=config.get("text"),
                icon_pixmap=self._get_icon_pixmap(config.get("icon")),
                font_type=config.get("font_type"),
                font_size=config.get("font_size"),
                font_color=config.get("font_color"),
                font_outline=config.get("font_outline"),
                font_outline_color=config.get("font_outline_color"),
                font_drop_shadow=config.get("font_drop_shadow"),
                font_italic=config.get("font_italic"),
                font_bold=config.get("font_bold"),
                font_underline=config.get("font_underline"),
                icon_position=config.get("icon_position"),
                parent=self.parent()
            )

            logging.debug("Building animation of type: %s", animation_type)

            parent_type: str = self._get_animation_type_parent(animation_type)
            if parent_type == "Dynamic":
                return self._build_dynamic_animation(config, animation_type, sound,
                                                     duration, starting_position, fade_in, fade_out,
                                                     fade_in_duration, fade_out_duration, fade_out_delay,
                                                     fade_in_easing_style, fade_out_easing_style, label, parent)
            elif parent_type == "Static":
                return self._build_static_animation(config, animation_type, sound,
                                                    duration, starting_position, fade_in, fade_out,
                                                    fade_in_duration, fade_out_duration, fade_out_delay,
                                                    fade_in_easing_style, fade_out_easing_style, label, parent)
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
            sound: QSoundEffect,
            duration: int,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_duration: int,
            fade_out_duration: int,
            fade_out_delay: int,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel,
            parent=None
    ) -> Optional[Animation]:
        """
        Builds a dynamic type Animation instance.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.
            animation_type (str): The type of animation.
            sound (str): Sound associated with the animation.
            duration (int): Duration of the animation.
            starting_position (QPointF): Starting position of the animation.
            fade_in (bool): Whether to fade in.
            fade_out (bool): Whether to fade out.
            fade_in_duration (int): Fade in duration.
            fade_out_duration (int): Fade out duration.
            fade_out_delay (int): Fade out delay.
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
            """ Can't find a purpose for this, yet
                direction: Tuple[float, float] = (
                self.DIRECTION_MAP.get(config.get("horizontal_direction", "Right"), 1.0),
                self.DIRECTION_MAP.get(config.get("vertical_direction", "Down"), 1.0)
            )"""
            easing_style: QEasingCurve.Type = self.EASING_MAP.get(
                config.get("easing_style", "Linear"),
                QEasingCurve.Type.Linear
            )

            if animation_type == "Directional":
                animation = DirectionalAnimation(
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
                    label=label,
                    ending_position=ending_position,
                    easing_style=easing_style,
                    parent=parent
                )
            elif animation_type == "Parabola":
                vertex_position: QPointF = self._get_vertex_position(starting_position, ending_position)
                parabola_points: List[AnimationPointF] = self._generate_parabola_data(
                    starting_position,
                    vertex_position,
                    ending_position,
                    self._get_total_parabola_points(duration, DEFAULT_FRAMERATE)
                )
                animation = ParabolaAnimation(
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
                    label=label,
                    ending_position=ending_position,
                    easing_style=easing_style,
                    parabola_points=parabola_points,
                    parent=parent
                )
            elif animation_type == "Swivel":
                phase_1_percentage: float = config.get("phase_1_percentage", 0.50)
                phase_2_percentage: float = config.get("phase_2_percentage", 0.50)
                swivel_position: QPointF = self._get_swivel_position(
                    starting_position,
                    ending_position,
                    phase_1_percentage
                )
                animation = SwivelAnimation(
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
                    label=label,
                    ending_position=ending_position,
                    easing_style=easing_style,
                    phase_1_duration=self._get_phase_duration(duration, phase_1_percentage),
                    phase_2_duration=self._get_phase_duration(duration, phase_2_percentage),
                    swivel_position=swivel_position,
                    parent=parent
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
            sound: QSoundEffect,
            duration: int,
            starting_position: QPointF,
            fade_in: bool,
            fade_out: bool,
            fade_in_duration: int,
            fade_out_duration: int,
            fade_out_delay: int,
            fade_in_easing_style: QEasingCurve.Type,
            fade_out_easing_style: QEasingCurve.Type,
            label: AnimationLabel,
            parent=None
    ) -> Optional[Animation]:
        """
        Builds a static type Animation instance.

        Args:
            config (Dict[str, Any]): Configuration dictionary for the animation.
            animation_type (str): The type of animation.
            sound (str): Sound associated with the animation.
            duration (int): Duration of the animation.
            starting_position (QPointF): Starting position of the animation.
            fade_in (bool): Whether to fade in.
            fade_out (bool): Whether to fade out.
            fade_in_duration (int): Fade in duration.
            fade_out_duration (int): Fade out duration.
            fade_out_delay (int): Fade out delay.
            fade_in_easing_style (QEasingCurve.Type): Easing style for fade in.
            fade_out_easing_style (QEasingCurve.Type): Easing style for fade out.
            label (AnimationLabel): Label associated with the animation.

        Returns:
            Optional[Animation]: The created static Animation instance or None.
        """
        try:
            jiggle: bool = config.get("jiggle", False)
            jiggle_intensity: int = self.JIGGLE_MAP.get(config.get("jiggle_intensity", "Medium"), 50)

            if animation_type == "Stationary":
                animation = StationaryAnimation(
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
                    label=label,
                    jiggle=jiggle,
                    jiggle_intensity=jiggle_intensity,
                    parent=parent
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
                    duration=duration,
                    starting_position=starting_position,
                    fade_in=fade_in,
                    fade_out=fade_out,
                    fade_in_duration=fade_in_duration,
                    fade_out_duration=fade_out_duration,
                    fade_out_delay=fade_out_delay,
                    fade_in_easing_style=fade_in_easing_style,
                    fade_out_easing_style=fade_out_easing_style,
                    label=label,
                    jiggle=jiggle,
                    jiggle_intensity=jiggle_intensity,
                    scale_percentage=scale_percentage,
                    phase_1_duration=self._get_phase_duration(duration, phase_1_percentage),
                    phase_2_duration=self._get_phase_duration(duration, phase_2_percentage),
                    scale_easing_style=scale_easing_style,
                    parent=parent
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
    def _get_sound_effect(sound: str) -> QSoundEffect:
        """
        Initialize the sound effect if a sound file is provided.
        """
        try:
            sound_effect = QSoundEffect()
            sound_effect.setSource(QUrl.fromLocalFile(sound))
            logging.debug("Sound Created for Animation: %s", sound)
            return sound_effect
        except Exception as e:
            logging.exception("Error Creating Sound for Animation: %s", e)

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
    def _get_phase_duration(duration: int, percentage: float) -> int:
        """
        Get the phase duration of a faded in or out animation

        Returns:
            fade_duration (int): The phase duration of a faded in or out animation.
        """
        return int(duration * percentage)

    @staticmethod
    def _get_fade_out_delay(duration: int, fade_out_duration: int) -> int:
        """
        Get the millisecond delay of a fade-out animation

        Returns:
            fade_out_delay (int): The millisecond delay of a fade-out animation
        """
        return duration - fade_out_duration

    @staticmethod
    def _get_swivel_position(starting_position: QPointF, ending_position: QPointF, percentage: float) -> QPointF:
        """
            Get the swivel position, which is the ending position of phase 1
            and the starting position of phase 2. It is calculated based on
            the phase 1 percentage of the duration.

        Returns:
            QPointF: The swivel position.
        """
        try:
            swivel_position = QPointF(
                starting_position.x() + (ending_position.x() - starting_position.x()) * percentage,
                starting_position.y() + (ending_position.y() - starting_position.y()) * percentage
            )
            # TODO: Implement logic to determine if swivel_position is out of bounds of the window
            logging.debug(
                f"Swivel position set to ({swivel_position.x()}, "
                f"{swivel_position.y()})."
            )
            return swivel_position
        except Exception as e:
            logging.exception("Failed to set up swivel position: %s", e)

    @staticmethod
    def _get_vertex_position(starting_position: QPointF, ending_position: QPointF) -> QPointF:
        """
        Calculates the vertex position for the ParabolaAnimation.

        Returns:
            QPointF: The vertex position.
        """
        try:
            vertex_position = QPointF(
                starting_position.x() + ending_position.x() / 2.0,
                starting_position.y() + ending_position.y() / 2.0
            )
            # TODO: Implement logic to determine if vertex_position is out of bounds of the window
            logging.debug(f"Calculated vertex position: {vertex_position}")
            return vertex_position
        except Exception as e:
            logging.exception("Failed to calculate vertex position: %s", e)

    @staticmethod
    def _get_total_parabola_points(duration: int, fps: int = DEFAULT_FRAMERATE) -> int:
        return int(float(duration / 1000.0) * fps)

    @staticmethod
    def _generate_parabola_data(
            starting_position: QPointF,
            vertex_position: QPointF,
            ending_position: QPointF,
            num_points: int
    ) -> List[AnimationPointF]:
        """
        Generate evenly spaced AnimationPointF points along a parabola with their position percentages.

        Parameters:
            starting_position (QPointF): The starting point of the parabola.
            vertex_position (QPointF): The vertex point of the parabola.
            ending_position (QPointF): The ending point of the parabola.
            num_points (int): The number of points to generate.

        Returns:
            List[AnimationPointF]: A list of AnimationPointF objects evenly spaced along the parabola curve,
                                    each with an associated key_value between 0.0 and 1.0.
        """
        try:
            logging.debug("Starting generation of parabola data with %d points.", num_points)

            # Validate input
            if num_points < 2:
                logging.warning("num_points is less than 2. Returning start and end points only.")
                return [
                    AnimationPointF(starting_position.x(), starting_position.y(), 0.0),
                    AnimationPointF(ending_position.x(), ending_position.y(), 1.0)
                ]

            # Calculate quadratic coefficients using vertex form: y = a(x - h)^2 + k
            h: float = vertex_position.x()
            k: float = vertex_position.y()
            try:
                denominator: float = (starting_position.x() - h) ** 2
                a: float = (starting_position.y() - k) / denominator
                b: float = -2.0 * a * h
                c: float = a * h ** 2.0 + k
                logging.debug("Quadratic coefficients calculated: a=%.6f, b=%.6f, c=%.6f", a, b, c)
            except ZeroDivisionError:
                logging.exception("Division by zero when calculating quadratic coefficients. Using default y = x^2.")
                a, b, c = 1.0, 0.0, 0.0

            # Precompute a fine grid of points to approximate arc length
            steps: int = 1000
            x_start: float = starting_position.x()
            x_end: float = ending_position.x()
            dx: float = (x_end - x_start) / steps
            x_values: List[float] = [x_start + i * dx for i in range(steps + 1)]
            y_values: List[float] = [a * x ** 2.0 + b * x + c for x in x_values]

            # Compute cumulative arc length
            cumulative_lengths: List[float] = [0.0]
            for i in range(1, len(x_values)):
                dx_segment: float = x_values[i] - x_values[i - 1]
                dy_segment: float = y_values[i] - y_values[i - 1]
                segment_length: float = (dx_segment ** 2.0 + dy_segment ** 2.0) ** 0.5
                cumulative_lengths.append(cumulative_lengths[-1] + segment_length)

            total_length: float = cumulative_lengths[-1]
            logging.debug("Total arc length approximated: %.6f", total_length)

            # Desired spacing between points
            spacing: float = float(total_length / (num_points - 1))
            logging.debug("Desired spacing between points: %.6f", spacing)

            # Function to find the x for a given target length using binary search
            def _find_x(target_len: float) -> float:
                left: int = 0
                right: int = len(cumulative_lengths) - 1
                while left <= right:
                    mid: int = (left + right) // 2
                    current_length: float = cumulative_lengths[mid]
                    if current_length < target_len:
                        left = mid + 1
                    else:
                        right = mid - 1
                if left == 0:
                    return x_values[0]
                elif left >= len(cumulative_lengths):
                    return x_values[-1]
                else:
                    length_before: float = cumulative_lengths[left - 1]
                    length_after: float = cumulative_lengths[left]
                    ratio: float = ((target_len - length_before) /
                                    (length_after - length_before)
                                    if (length_after - length_before) != 0.0
                                    else 0.0
                                    )
                    interpolated_x: float = x_values[left - 1] + ratio * (x_values[left] - x_values[left - 1])
                    return interpolated_x

            # Generate points
            animation_points: List[AnimationPointF] = []
            for i in range(num_points):
                target_length: float = spacing * i
                x: float = _find_x(target_length)
                y: float = a * x ** 2.0 + b * x + c
                key_value: float = (target_length / total_length) if total_length != 0 else 0.0
                animation_point: AnimationPointF = AnimationPointF(x, y, key_value)
                animation_points.append(animation_point)
                logging.debug(
                    "Added point %d: (%.6f, %.6f) with key_value %.6f",
                    i, x, y, key_value
                )

            return animation_points

        except Exception as e:
            logging.exception(f"Failed to generate parabola data: {e}")
            # Return default start and end points with corresponding key_values
            return [
                AnimationPointF(starting_position.x(), starting_position.y(), 0.0),
                AnimationPointF(ending_position.x(), ending_position.y(), 1.0)
            ]

    @staticmethod
    def _create_q_font(
            font_type: str,
            font_size: int,
            font_weight: int,
            font_style: int,
            font_letter_spacing: float,
            font_word_spacing: float,
            font_underline: bool,
            font_overline: bool,
            font_strikeout: bool,
            font_kerning: bool,
            font_capitalization: QFont.Capitalization,
            font_stretch: QFont.Stretch
    ) -> QFont:
        q_font: QFont = QFont(font_type, font_size, font_weight, font_style)
        q_font.setStretch(font_stretch)
        q_font.setKerning(font_kerning)
        q_font.setCapitalization(font_capitalization)
        q_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, font_letter_spacing)
        q_font.setWordSpacing(font_word_spacing)
        q_font.setUnderline(font_underline)
        q_font.setOverline(font_overline)
        q_font.setStrikeOut(font_strikeout)
        return q_font

    @staticmethod
    def _get_font_style(font_database: QFontDatabase, font_type: str, font_italic: bool) -> int:
        if font_italic:
            if font_database.isSmoothlyScalable(font_type) and font_database.italic(font_type):
                return QFont.Style.StyleItalic.value
            else:
                return QFont.Style.StyleOblique.value
        else:
            return QFont.Style.StyleNormal.value
