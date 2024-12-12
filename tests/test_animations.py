import sys
import logging
from typing import List

from PyQt6.QtCore import QTimer, QEasingCurve, QPointF, QUrl, Qt, pyqtSlot, QAbstractAnimation
from PyQt6.QtGui import QFont, QPen, QColor
from PyQt6.QtMultimedia import QSoundEffect

from jetque.jetque import JetQue
from jetque.source.animations.animation import Animation
from jetque.source.animations.animation_font import AnimationFont
from jetque.source.animations.dynamics.directional_animation import DirectionalAnimation
from jetque.source.animations.dynamics.parabola_animation import ParabolaAnimation
from jetque.source.animations.dynamics.swivel_animation import SwivelAnimation
from jetque.source.animations.statics.pow_animation import PowAnimation
from jetque.source.animations.statics.stationary_animation import StationaryAnimation
from jetque.source.animations.animation_point_f import AnimationPointF
from jetque.source.gui.items.jq_graphics_pixmap_item import JQGraphicsPixmapItem
from jetque.source.gui.items.jq_graphics_text_item import JQGraphicsTextItem


class AnimationTester(JetQue):
    def __init__(self, sys_argv: List[str]) -> None:
        super().__init__(sys_argv)

        self.overlay.setParent(self)
        self.active_animations = []
        self.upper_start_point = None
        self.upper_vertex_point = None
        self.upper_end_point = None
        self.upper_num_points = None
        self.upper_bezier_points = None
        self.lower_start_point = None
        self.lower_vertex_point = None
        self.lower_end_point = None
        self.lower_num_points = None
        self.lower_bezier_points = None

        self.outgoing_triggers_counter = 0
        self.outgoing_triggers_timer = QTimer(self)
        self.outgoing_hits_counter = 0
        self.outgoing_hits_timer = QTimer(self)
        self.outgoing_avoidance_counter = 0
        self.outgoing_avoidance_timer = QTimer(self)
        self.incoming_hits_counter = 0
        self.incoming_hits_timer = QTimer(self)
        self.incoming_avoidance_counter = 0
        self.incoming_avoidance_timer = QTimer(self)

        self.fun()

    def debug(self):
        pass

    def fun(self):
        self.upper_start_point = QPointF(980.0, 700.0)
        self.upper_vertex_point = QPointF(540.0, 350.0)
        self.upper_end_point = QPointF(0.0, 700.0)
        self.upper_num_points = 100

        self.upper_bezier_points = self.calculate_quadratic_interpolation_points(

            self.upper_start_point, self.upper_vertex_point, self.upper_end_point, self.upper_num_points

        )

        self.lower_start_point = QPointF(980.0, 700.0)
        self.lower_vertex_point = QPointF(540.0, 1050.0)
        self.lower_end_point = QPointF(0.0, 700.0)
        self.lower_num_points = 100

        self.lower_bezier_points = self.calculate_quadratic_interpolation_points(

            self.lower_start_point, self.lower_vertex_point, self.lower_end_point, self.lower_num_points

        )

        self.outgoing_triggers_timer.timeout.connect(self.run_outgoing_triggers_animation_test)
        self.outgoing_triggers_timer.start(5250)
        self.outgoing_hits_timer.timeout.connect(self.run_outgoing_hits_animation_test)
        self.outgoing_hits_timer.start(1600)
        self.outgoing_avoidance_timer.timeout.connect(self.run_outgoing_avoidance_animation_test)
        self.outgoing_avoidance_timer.start(1725)
        self.incoming_hits_timer.timeout.connect(self.run_incoming_hits_animation_test)
        self.incoming_hits_timer.start(1850)
        self.incoming_avoidance_timer.timeout.connect(self.run_incoming_avoidance_animation_test)
        self.incoming_avoidance_timer.start(1975)

    def start_animation(self, animation) -> None:
        """
        Starts the given animation and adds it to the appropriate active animations list.

        Args:
            animation (Animation): The animation instance to start.
        """
        try:
            if animation and animation.animation_object:

                def animation_cleanup():
                    self.animation_cleanup(animation, animation.animation_object)

                animation.finished.connect(animation_cleanup)
                self.active_animations.append(animation)
                self.overlay.addItem(animation.animation_object)
                animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        except Exception as e:
            logging.exception("Exception in start_animation: %s", e)

    @pyqtSlot()
    def animation_cleanup(self, animation, animation_object) -> None:
        """
        Handles the cleanup process when an animation finishes.

        Args:
            animation (Animation): The animation instance that has started.
            animation_object (Optional[QObject]): The object being animated.
        """
        try:
            if animation and animation_object and animation in self.active_animations:
                self.active_animations.remove(animation)
                animation.finished.disconnect()
                animation_object.deleteLater()
        except Exception as e:
            logging.exception("Exception in animation_cleanup: %s", e)

    def _create_base_animation_text(
            self,
            size=36,
            event_type="default",
            msg="Default Message",
            color="white",
            outline_color="black",
            alignment="left",
            capitalization_type=QFont.Capitalization.MixedCase
    ) -> JQGraphicsTextItem:

        font_type = "Helvetica"
        font_size = size
        # file_path = "default"
        message = msg
        color = QColor(color)
        outline_color = QColor(outline_color)
        drop_shadow_color = QColor(0, 0, 0, 191)
        icon_alignment = alignment
        outline_on = True
        drop_shadow_on = True
        italics_on = False
        kerning_on = True
        overline_on = False
        strikethrough_on = False
        underline_on = False
        extra_letter_spacing = 0.0
        extra_word_spacing = 0.0
        outline_width = 2.0
        drop_shadow_radius = 7.0
        drop_shadow_offset = QPointF(3.5, 6.1)
        outline_type = Qt.PenStyle.SolidLine
        outline_shape = Qt.PenCapStyle.RoundCap
        outline_corners = Qt.PenJoinStyle.RoundJoin
        weight = QFont.Weight.Bold
        capitalization = capitalization_type
        stretch = QFont.Stretch.Unstretched

        text_font = AnimationFont(
            font_type=font_type,
            font_size=font_size,
            font_weight=weight,
            font_capitalization=capitalization,
            font_stretch=stretch,
            font_letter_spacing=extra_letter_spacing,
            font_word_spacing=extra_word_spacing,
            font_italic=italics_on,
            font_kerning=kerning_on,
            font_overline=overline_on,
            font_strikethrough=strikethrough_on,
            font_underline=underline_on
        )

        text_outline_pen = QPen(
            outline_color,
            outline_width,
            outline_type,
            outline_shape,
            outline_corners
        )

        text_item = JQGraphicsTextItem(
            font=text_font,
            text=message,
            color=color,
            outline=outline_on,
            outline_pen=text_outline_pen,
            drop_shadow=drop_shadow_on,
            drop_shadow_offset=drop_shadow_offset,
            drop_shadow_blur_radius=drop_shadow_radius,
            drop_shadow_color=drop_shadow_color,
            parent_object=self.overlay
        )

        if event_type == "hit":
            file_path = "C:/intellij-projects/jetque/jetque/resources/hit.png"
        elif event_type == "punch":
            file_path = "C:/intellij-projects/jetque/jetque/resources/punch.png"
        elif event_type == "crush":
            file_path = "C:/intellij-projects/jetque/jetque/resources/crush.png"
        elif event_type == "slash":
            file_path = "C:/intellij-projects/jetque/jetque/resources/slash.png"
        elif event_type == "pierce":
            file_path = "C:/intellij-projects/jetque/jetque/resources/pierce.png"
        elif event_type == "kick":
            file_path = "C:/intellij-projects/jetque/jetque/resources/kick.png"
        elif event_type == "bash":
            file_path = "C:/intellij-projects/jetque/jetque/resources/bash.png"
        elif event_type == "strike":
            file_path = "C:/intellij-projects/jetque/jetque/resources/strike.png"
        elif event_type == "backstab":
            file_path = "C:/intellij-projects/jetque/jetque/resources/backstab.png"
        elif event_type == "dodge":
            file_path = "C:/intellij-projects/jetque/jetque/resources/dodge.png"
        elif event_type == "block":
            file_path = "C:/intellij-projects/jetque/jetque/resources/block.png"
        elif event_type == "parry":
            file_path = "C:/intellij-projects/jetque/jetque/resources/parry.png"
        elif event_type == "riposte":
            file_path = "C:/intellij-projects/jetque/jetque/resources/riposte.png"
        elif event_type == "miss":
            file_path = "C:/intellij-projects/jetque/jetque/resources/miss.png"
        elif event_type == "absorb":
            file_path = "C:/intellij-projects/jetque/jetque/resources/absorb.png"
        else:
            file_path = "C:/intellij-projects/jetque/jetque/resources/default.png"

        text_icon = JQGraphicsPixmapItem(
            file_path=file_path,
            outline=False,
            outline_pen=text_outline_pen,
            drop_shadow=False,
            drop_shadow_offset=drop_shadow_offset,
            drop_shadow_blur_radius=drop_shadow_radius,
            drop_shadow_color=drop_shadow_color,
            alignment=icon_alignment
        )

        text_icon.setParentItem(text_item)

        return text_item

    @staticmethod
    def calculate_quadratic_interpolation_points(start, vertex, end, num_points):
        """
        Calculate points on a quadratic Bézier curve.
        """
        # Extract x and y values from the provided points
        x0, y0 = start.x(), start.y()
        x1, y1 = vertex.x(), vertex.y()
        x2, y2 = end.x(), end.y()

        # Ensure all x-values are distinct to avoid division by zero
        if x0 == x1 or x0 == x2 or x1 == x2:
            raise ValueError("All x-values must be distinct for quadratic interpolation.")

        # Determine the direction based on start and end points
        if x0 < x2:
            step = (x2 - x0) / (num_points - 1)
            x_values = [x0 + step * i for i in range(num_points)]
        else:
            step = (x0 - x2) / (num_points - 1)
            x_values = [x0 - step * i for i in range(num_points)]

        points = []
        for t in x_values:
            # Calculate Lagrange basis polynomials
            l0 = ((t - x1) * (t - x2)) / ((x0 - x1) * (x0 - x2))
            l1 = ((t - x0) * (t - x2)) / ((x1 - x0) * (x1 - x2))
            l2 = ((t - x0) * (t - x1)) / ((x2 - x0) * (x2 - x1))

            # Apply the Quadratic Interpolation Formula
            y = (y0 * l0) + (y1 * l1) + (y2 * l2)

            # Create a QPointF object and append to the list
            point = QPointF(t, y)
            points.append(point)

        return points

    @staticmethod
    def _create_sound_effect() -> QSoundEffect:
        sound = QSoundEffect()
        sound.setSource(QUrl())  # Fake sound file
        return sound

    def run_directional_animation_test(self):
        starting_pos = QPointF()
        ending_pos = QPointF()
        anim_text = self._create_base_animation_text()

        anim = DirectionalAnimation(
            animation_type="Directional",
            sound=self._create_sound_effect(),
            duration=1000,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.OutQuad,
            fade_out_easing_style=QEasingCurve.Type.InQuad,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
        )

        self.start_animation(anim)

    def run_parabola_animation_test(self):
        starting_pos = QPointF()
        ending_pos = QPointF()
        parabola_points = [
            AnimationPointF((starting_pos.x() + ending_pos.x()) / 2, starting_pos.y() - 100, 0.5),
        ]
        anim_text = self._create_base_animation_text()

        anim = ParabolaAnimation(
            animation_type="Parabola",
            sound=self._create_sound_effect(),
            duration=1500,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
            parabola_points=parabola_points
        )

        self.start_animation(anim)

    def run_outgoing_hits_animation_test(self):
        starting_pos = QPointF(1280.0, 700.0)
        swivel_pos = QPointF(1920.0, 350.0)
        ending_pos = QPointF(2560.0, 350.0)
        duration = 2200
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration / 2)
        phase_2_duration = int(duration / 2)
        fade_in_on = True
        fade_out_on = True
        event_type = "Blank"
        message = "Blank"

        if self.outgoing_hits_counter == 0:
            event_type = "hit"
            message = "40 Hit"
        elif self.outgoing_hits_counter == 1:
            event_type = "punch"
            message = "15 Punch"
        elif self.outgoing_hits_counter == 2:
            event_type = "slash"
            message = "60 Slash"
        elif self.outgoing_hits_counter == 3:
            event_type = "crush"
            message = "60 Crush"
        elif self.outgoing_hits_counter == 4:
            event_type = "pierce"
            message = "25 Pierce"

        anim_text = self._create_base_animation_text(
            24,
            event_type,
            message,
            "white",
            "black",
            "left",
            QFont.Capitalization.SmallCaps
        )

        anim = SwivelAnimation(
            animation_type="Swivel",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.OutInQuad,
            phase_1_duration=phase_1_duration,
            phase_2_duration=phase_2_duration,
            swivel_position=swivel_pos,
        )

        self.start_animation(anim)

        if self.outgoing_hits_counter < 4:
            self.outgoing_hits_counter += 1
        else:
            self.outgoing_hits_counter = 0

    def run_incoming_hits_animation_test(self):
        starting_pos = QPointF(0.0, 0.0)
        ending_pos = QPointF(0.0, 0.0)
        duration = 2200
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        fade_in_on = True
        fade_out_on = True
        event_type = "Blank"
        message = "Blank"

        if self.incoming_hits_counter == 0:
            event_type = "hit"
            message = "(a gnoll pup) 40"
        elif self.incoming_hits_counter == 1:
            event_type = "punch"
            message = "(a gnoll pup) 15"
        elif self.incoming_hits_counter == 2:
            event_type = "slash"
            message = "(a gnoll pup) 60"
        elif self.incoming_hits_counter == 3:
            event_type = "crush"
            message = "(a gnoll pup) 60"
        elif self.incoming_hits_counter == 4:
            event_type = "pierce"
            message = "(a gnoll pup) 25"

        anim_text = self._create_base_animation_text(
            24,
            event_type,
            message,
            "red",
            "black",
            "right",
            QFont.Capitalization.SmallCaps
        )

        anim = ParabolaAnimation(
            animation_type="Parabola",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
            parabola_points=self.upper_bezier_points
        )

        self.start_animation(anim)

        if self.incoming_hits_counter < 4:
            self.incoming_hits_counter += 1
        else:
            self.incoming_hits_counter = 0

    def run_outgoing_avoidance_animation_test(self):
        starting_pos = QPointF(1280.0, 700.0)
        swivel_pos = QPointF(1920.0, 1050.0)
        ending_pos = QPointF(2560.0, 1050.0)
        duration = 2200
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration / 2)
        phase_2_duration = int(duration / 2)
        fade_in_on = True
        fade_out_on = True
        event_type = "Blank"
        message = "Blank"

        if self.outgoing_avoidance_counter == 0:
            event_type = "miss"
            message = "Miss"
        elif self.outgoing_avoidance_counter == 1:
            event_type = "dodge"
            message = "Dodge"
        elif self.outgoing_avoidance_counter == 2:
            event_type = "parry"
            message = "Parry"
        elif self.outgoing_avoidance_counter == 3:
            event_type = "riposte"
            message = "Riposte"
        elif self.outgoing_avoidance_counter == 4:
            event_type = "block"
            message = "Block"
        elif self.outgoing_avoidance_counter == 5:
            event_type = "absorb"
            message = "Absorb"

        anim_text = self._create_base_animation_text(
            24,
            event_type,
            message,
            "white",
            "black",
            "left",
            QFont.Capitalization.SmallCaps
        )

        anim = SwivelAnimation(
            animation_type="Swivel",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.OutInQuad,
            phase_1_duration=phase_1_duration,
            phase_2_duration=phase_2_duration,
            swivel_position=swivel_pos,
        )

        self.start_animation(anim)

        if self.outgoing_avoidance_counter < 5:
            self.outgoing_avoidance_counter += 1
        else:
            self.outgoing_avoidance_counter = 0

    def run_incoming_avoidance_animation_test(self):
        starting_pos = QPointF(0.0, 0.0)
        ending_pos = QPointF(0.0, 0.0)
        duration = 2200
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        fade_in_on = True
        fade_out_on = True
        event_type = "Blank"
        message = "Blank"

        if self.incoming_avoidance_counter == 0:
            event_type = "miss"
            message = "(Fippy Darkpaw) Miss"
        elif self.incoming_avoidance_counter == 1:
            event_type = "dodge"
            message = "(Cazic-Tool) Dodge"
        elif self.incoming_avoidance_counter == 2:
            event_type = "parry"
            message = "(a skeleton) Parry"
        elif self.incoming_avoidance_counter == 3:
            event_type = "riposte"
            message = "(an orc pawn) Riposte"
        elif self.incoming_avoidance_counter == 4:
            event_type = "block"
            message = "(Priest of Discord) Block"
        elif self.incoming_avoidance_counter == 5:
            event_type = "absorb"
            message = "(pain and suffering) Absorb"

        anim_text = self._create_base_animation_text(
            24,
            event_type,
            message,
            "red",
            "black",
            "left",
            QFont.Capitalization.SmallCaps
        )

        anim = ParabolaAnimation(
            animation_type="Parabola",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            ending_position=ending_pos,
            easing_style=QEasingCurve.Type.Linear,
            parabola_points=self.lower_bezier_points
        )

        self.start_animation(anim)

        if self.incoming_avoidance_counter < 5:
            self.incoming_avoidance_counter += 1
        else:
            self.incoming_avoidance_counter = 0

    def run_outgoing_triggers_animation_test(self):
        starting_pos = QPointF(1180.0, 250.0)  # Manual start pos
        duration = 5000
        fade_in_duration = int(duration * 0.1)
        fade_out_duration = int(duration * 0.1)
        fade_out_delay = int(duration - fade_out_duration)
        phase_1_duration = int(duration * 0.05)
        phase_2_duration = int(duration * 0.95)
        jiggle_intensity = 25
        scale_increase_percentage = 2.75
        jiggle_on = True
        fade_in_on = True
        fade_out_on = True
        event_type = "Blank"
        message = "Blank"

        if self.outgoing_triggers_counter == 0:
            event_type = "backstab"
            message = "300 Backstab"
        elif self.outgoing_triggers_counter == 1:
            event_type = "kick"
            message = "120 Kick"
        elif self.outgoing_triggers_counter == 2:
            event_type = "bash"
            message = "15 Bash"
        elif self.outgoing_triggers_counter == 3:
            event_type = "strike"
            message = "60 Strike"

        anim_text = self._create_base_animation_text(
            36,
            event_type,
            message,
            "yellow",
            "black",
            "left",
            QFont.Capitalization.SmallCaps
        )

        anim = PowAnimation(
            animation_type="Pow",
            sound=self._create_sound_effect(),
            duration=duration,
            starting_position=starting_pos,
            fade_in=fade_in_on,
            fade_out=fade_out_on,
            fade_in_duration=fade_in_duration,
            fade_out_duration=fade_out_duration,
            fade_out_delay=fade_out_delay,
            fade_in_easing_style=QEasingCurve.Type.Linear,
            fade_out_easing_style=QEasingCurve.Type.Linear,
            animation_object=anim_text,
            jiggle=jiggle_on,
            jiggle_intensity=jiggle_intensity,
            scale_percentage=scale_increase_percentage,
            scale_easing_style=QEasingCurve.Type.OutInQuad,
            phase_1_duration=phase_1_duration,
            phase_2_duration=phase_2_duration
        )

        self.start_animation(anim)

        if self.outgoing_triggers_counter < 3:
            self.outgoing_triggers_counter += 1
        else:
            self.outgoing_triggers_counter = 0

    def run_stationary_animation_test(self):
        starting_pos = QPointF()
        anim_text = self._create_base_animation_text()

        anim = StationaryAnimation(
            animation_type="Stationary",
            sound=self._create_sound_effect(),
            duration=1000,
            starting_position=starting_pos,
            fade_in=True,
            fade_out=True,
            fade_in_duration=250,
            fade_out_duration=250,
            fade_out_delay=250,
            fade_in_easing_style=QEasingCurve.Type.OutQuad,
            fade_out_easing_style=QEasingCurve.Type.InQuad,
            animation_object=anim_text,
            jiggle=True,
            jiggle_intensity=100
        )

        self.start_animation(anim)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s:%(name)s:%(levelname)s: %(filename)s:%(funcName)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    app = AnimationTester(sys.argv)
    app.run()
