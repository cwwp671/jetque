# jetque/tests/test_animation_label.py

import unittest
from unittest.mock import patch

from PyQt6.QtGui import QColor, QPixmap, QFontMetrics
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QSize

import sys

from src.animations.animation_label import AnimationLabel, ICON_SPACING

# Initialize the QApplication once for all tests
app = QApplication(sys.argv)


class TestAnimationLabel(unittest.TestCase):
    """
    Test suite for the AnimationLabel class, ensuring all functionalities
    behave as expected under various configurations.
    """

    @staticmethod
    def _calculate_expected_size(label: AnimationLabel, text: str) -> tuple:
        """
        Helper method to calculate the expected size based on text and icon.

        Args:
            label (AnimationLabel): The AnimationLabel instance.
            text (str): The text content of the label.

        Returns:
            tuple: Expected (width, height) of the label.
        """
        fm = QFontMetrics(label.font())
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()

        icon_width = 0
        if label._animation_icon and not label._animation_icon.pixmap().isNull():
            icon_width = label._animation_icon.width() + ICON_SPACING

        total_width = text_width + icon_width
        total_height = text_height

        return total_width, total_height

    def setUp(self) -> None:
        """
        Set up a QWidget to host the AnimationLabel for testing.
        This runs before each test method.
        """
        self.widget = QWidget()
        self.widget.show()

    def tearDown(self) -> None:
        """
        Clean up after each test.
        This runs after each test method.
        """
        self.widget.close()

    def test_default_initialization(self) -> None:
        """
        Test AnimationLabel initialization with default parameters.
        """
        label = AnimationLabel(parent=None)
        self.assertEqual(label.text(), "")
        self.assertEqual(label._font_type, "Arial")
        self.assertEqual(label._font_size, 24)
        self.assertEqual(label._font_color, QColor("white"))
        self.assertEqual(label._font_outline, "thin")
        self.assertEqual(label._font_outline_color, QColor("black"))
        self.assertEqual(label._font_drop_shadow, "none")
        self.assertFalse(label._font_italic)
        self.assertFalse(label._font_bold)
        self.assertFalse(label._font_underline)
        self.assertEqual(label.icon_position, "left")
        self.assertIsNone(label._animation_icon)

    def test_initialization_with_text(self) -> None:
        """
        Test AnimationLabel initialization with provided text.
        """
        label = AnimationLabel(text="Test Label")
        self.assertEqual(label.text(), "Test Label")

    def test_initialization_with_icon(self) -> None:
        """
        Test AnimationLabel initialization with an icon pixmap.
        """
        pixmap = QPixmap(50, 50)
        label = AnimationLabel(icon_pixmap=pixmap)
        self.assertIsNotNone(label._animation_icon)
        self.assertFalse(label._animation_icon.pixmap().isNull(),
                         "Icon pixmap should not be null.")
        # Optionally, check the size of the scaled pixmap
        expected_size = QSize(label._font_size, label._font_size)
        self.assertEqual(label._animation_icon.pixmap().size(), expected_size)

    def test_set_text(self) -> None:
        """
        Test setting text after initialization.
        """
        label = AnimationLabel()
        label.set_text("New Text")
        self.assertEqual(label.text(), "New Text")

    def test_set_font_type(self) -> None:
        """
        Test setting the font type of the label.
        """
        label = AnimationLabel()
        label.set_font_type("Times New Roman")
        self.assertEqual(label._font_type, "Times New Roman")
        self.assertEqual(label.font().family(), "Times New Roman")

    def test_set_font_size(self) -> None:
        """
        Test setting the font size of the label.
        """
        label = AnimationLabel()
        label.set_font_size(30)
        self.assertEqual(label._font_size, 30)
        self.assertEqual(label.font().pointSize(), 30)

    def test_set_font_color(self) -> None:
        """
        Test setting the font color of the label.
        """
        label = AnimationLabel()
        color = QColor("red")
        label.set_font_color(color)
        self.assertEqual(label._font_color, color)

    def test_set_font_outline(self) -> None:
        """
        Test setting the font outline style of the label.
        """
        label = AnimationLabel()
        label.set_font_outline("thick")
        self.assertEqual(label._font_outline, "thick")
        # Attempt to set an invalid outline; should remain unchanged
        label.set_font_outline("invalid")
        self.assertEqual(label._font_outline, "thick")

    def test_set_font_outline_color(self) -> None:
        """
        Test setting the font outline color of the label.
        """
        label = AnimationLabel()
        color = QColor("blue")
        label.set_font_outline_color(color)
        self.assertEqual(label._font_outline_color, color)

    def test_set_font_drop_shadow(self) -> None:
        """
        Test setting the font drop shadow style of the label.
        """
        label = AnimationLabel()
        label.set_font_drop_shadow("strong")
        self.assertEqual(label._font_drop_shadow, "strong")
        # Attempt to set an invalid drop shadow; should remain unchanged
        label.set_font_drop_shadow("invalid")
        self.assertEqual(label._font_drop_shadow, "strong")

    def test_set_font_italic(self) -> None:
        """
        Test setting the font italic style of the label.
        """
        label = AnimationLabel()
        label.set_font_italic(True)
        self.assertTrue(label._font_italic)
        self.assertTrue(label.font().italic())

    def test_set_font_bold(self) -> None:
        """
        Test setting the font bold style of the label.
        """
        label = AnimationLabel()
        label.set_font_bold(True)
        self.assertTrue(label._font_bold)
        self.assertTrue(label.font().bold())

    def test_set_font_underline(self) -> None:
        """
        Test setting the font underline style of the label.
        """
        label = AnimationLabel()
        label.set_font_underline(True)
        self.assertTrue(label._font_underline)
        self.assertTrue(label.font().underline())

    def test_set_icon_pixmap(self) -> None:
        """
        Test setting the icon pixmap of the label.
        """
        label = AnimationLabel()
        pixmap = QPixmap(40, 40)
        label.set_icon_pixmap(pixmap)
        self.assertIsNotNone(label._animation_icon)
        self.assertFalse(label._animation_icon.pixmap().isNull(),
                         "Icon pixmap should not be null.")
        expected_size = QSize(label._font_size, label._font_size)
        self.assertEqual(label._animation_icon.pixmap().size(), expected_size)

    def test_set_icon_position_left(self) -> None:
        """
        Test setting the icon position to 'left'.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(icon_pixmap=pixmap, icon_position="left")
        self.assertEqual(label.icon_position, "left")
        self.assertEqual(label._animation_icon.position, "left")

    def test_set_icon_position_right(self) -> None:
        """
        Test setting the icon position to 'right'.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(icon_pixmap=pixmap, icon_position="right")
        self.assertEqual(label.icon_position, "right")
        self.assertEqual(label._animation_icon.position, "right")

    def test_set_icon_position_invalid(self) -> None:
        """
        Test setting the icon position to an invalid value.
        It should default or remain unchanged based on implementation.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(icon_pixmap=pixmap, icon_position="left")
        label.set_icon_position("top")  # Invalid position
        self.assertEqual(label.icon_position, "left")  # Should remain unchanged
        self.assertEqual(label._animation_icon.position, "left")

    def test_adjust_size_with_icon_left(self) -> None:
        """
        Test size adjustment when the icon is positioned on the left.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(text="Test", icon_pixmap=pixmap, icon_position="left")
        expected_width, expected_height = self._calculate_expected_size(label, "Test")
        self.assertEqual(label.width(), expected_width)
        self.assertEqual(label.height(), expected_height)

    def test_adjust_size_with_icon_right(self) -> None:
        """
        Test size adjustment when the icon is positioned on the right.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(text="Test", icon_pixmap=pixmap, icon_position="right")
        expected_width, expected_height = self._calculate_expected_size(label, "Test")
        self.assertEqual(label.width(), expected_width)
        self.assertEqual(label.height(), expected_height)

    def test_adjust_size_without_icon(self) -> None:
        """
        Test size adjustment when there is no icon.
        """
        label = AnimationLabel(text="Test")
        expected_width, expected_height = self._calculate_expected_size(label, "Test")
        self.assertEqual(label.width(), expected_width)
        self.assertEqual(label.height(), expected_height)

    def test_size_hint(self) -> None:
        """
        Test the sizeHint method to ensure it returns the expected size.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(text="Size Hint Test", icon_pixmap=pixmap)
        expected_width, expected_height = self._calculate_expected_size(label, "Size Hint Test")
        size_hint = label.sizeHint()
        self.assertEqual(size_hint.width(), expected_width)
        self.assertEqual(size_hint.height(), expected_height)

    def test_paint_event_with_outline_and_shadow(self) -> None:
        """
        Test the paintEvent method with outline and shadow enabled.
        Ensures that drawText and drawPath are called.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(
            text="Paint Test",
            icon_pixmap=pixmap,
            font_outline="thick",
            font_drop_shadow="strong"
        )
        with patch('src.animations.animation_label.QPainter') as MockPainter:
            painter_instance = MockPainter.return_value
            label.paintEvent(None)
            self.assertTrue(painter_instance.drawText.called,
                            "drawText should be called when outline and shadow are enabled.")
            self.assertTrue(painter_instance.drawPath.called,
                            "drawPath should be called when outline is enabled.")

    def test_paint_event_without_outline_and_shadow(self) -> None:
        """
        Test the paintEvent method without outline and shadow.
        Ensures that drawText is called and drawPath is not.
        """
        label = AnimationLabel(text="Simple Paint Test", font_outline="none")
        with patch('src.animations.animation_label.QPainter') as MockPainter:
            painter_instance = MockPainter.return_value
            label.paintEvent(None)
            self.assertTrue(painter_instance.drawText.called,
                            "drawText should be called when no outline and shadow are enabled.")
            self.assertFalse(painter_instance.drawPath.called,
                             "drawPath should not be called when no outline is enabled.")

    def test_update_icon_size(self) -> None:
        """
        Test that updating the font size updates the icon size accordingly.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(icon_pixmap=pixmap, font_size=20)
        label.set_font_size(30)
        updated_icon_size = label._animation_icon.size()
        self.assertEqual(updated_icon_size.width(), 30,
                         "Icon width should update to match the new font size.")
        self.assertEqual(updated_icon_size.height(), 30,
                         "Icon height should update to match the new font size.")

    def test_remove_icon(self) -> None:
        """
        Test removing the icon from the label.
        Ensures that the icon is removed and size adjusts accordingly.
        """
        pixmap = QPixmap(40, 40)
        label = AnimationLabel(icon_pixmap=pixmap)
        label.set_icon_pixmap(None)
        self.assertIsNotNone(label._animation_icon,
                             "AnimationIcon instance should still exist.")
        self.assertTrue(label._animation_icon.pixmap().isNull(),
                        "Icon pixmap should be null after removal.")
        expected_width, expected_height = self._calculate_expected_size(label, label.text())
        self.assertEqual(label.width(), expected_width,
                         "Label width should adjust after removing the icon.")
        self.assertEqual(label.height(), expected_height,
                         "Label height should adjust after removing the icon.")


if __name__ == '__main__':
    unittest.main()
