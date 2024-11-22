# src/animations/animation_font.py
from PyQt6.QtGui import QFont


class AnimationFont(QFont):
    """
    Needs description

    Attributes:
        Needs attributes
    """

    def __init__(
            self,
            font_type: str,
            font_size: int,
            font_weight: QFont.Weight,
            font_capitalization: QFont.Capitalization,
            font_stretch: QFont.Stretch,
            font_letter_spacing: float,
            font_word_spacing: float,
            font_italic: bool,
            font_kerning: bool,
            font_overline: bool,
            font_strikethrough: bool,
            font_underline: bool
    ) -> None:
        """
        Needs description

        Args:
            Needs args
        """
        super().__init__(
            family=font_type,
            pointSize=font_size,
            weight=font_weight,
            italic=font_italic
        )

        # Initializes more font attributes than the parent QFont
        self.setCapitalization(font_capitalization)
        self.setStretch(font_stretch)
        self.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, font_letter_spacing)
        self.setWordSpacing(font_word_spacing)
        self.setKerning(font_kerning)
        self.setOverline(font_overline)
        self.setStrikeOut(font_strikethrough)
        self.setUnderline(font_underline)
