# src/animations/animation_object.py

import logging
from typing import Optional

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsObject

from jetque.source.animations.animation_icon import AnimationIcon
from jetque.source.animations.animation_text import AnimationText


class AnimationObject(QGraphicsObject):
    """
    A QGraphicsItemGroup that combines AnimationText with an optional AnimationIcon.

    Attributes:
        animation_text (AnimationObject): The text component of the animation.
        animation_icon (Optional[AnimationIcon]): The optional icon component of the animation.
        animation_icon_position (str): Position of the icon relative to the text ('left' or 'right').
    """

    def __init__(
            self,
            animation_text: AnimationText,
            animation_icon: Optional[AnimationIcon] = None,
            animation_icon_position: str = "left",  # using a str instead of bool incase I allow more positions
            parent=None
    ) -> None:
        """
        Initializes the AnimationObject with pre-created AnimationText and optional AnimationIcon.

        Args:
            animation_text (AnimationObject): The pre-created AnimationText instance.
            animation_icon (Optional[AnimationIcon], optional): The pre-created AnimationIcon instance.
            animation_icon_position (str, optional): Position of the icon relative to the text ('left' or 'right').
            parent (QGraphicsItem, optional): The parent graphics item.
        """
        super().__init__(parent)

        try:
            self.animation_text = animation_text

            if animation_icon:
                self.animation_icon: Optional[AnimationIcon] = animation_icon
                self.animation_icon_position = animation_icon_position.lower()
                logging.debug("AnimationIcon added to AnimationObject.")

            self.layout_items()

            logging.debug(
                "AnimationObject initialized with text: '%s' and icon_position: '%s'",
                self.animation_text.toPlainText(),
                self.animation_icon_position
            )

        except Exception as e:
            logging.exception("Failed to initialize AnimationObject: %s", e)

    def layout_items(self) -> None:
        """
        Layouts the AnimationText and AnimationIcon within the group based on the icon position.
        """
        try:
            # Ensure the text's bounding rect is up-to-date
            self.animation_text.update()
            animation_text_rect: QRectF = self.animation_text.boundingRect()
            animation_text_height = animation_text_rect.height()

            logging.debug("Text bounding rect: %s, height: %f", animation_text_rect, animation_text_height)

            # If icon exists, set its size and position
            if self.animation_icon:
                # Set icon size to be a square with side equal to text height
                self.animation_icon.set_icon_size(animation_text_height)
                icon_pixmap = self.animation_icon.pixmap_item.pixmap()
                if icon_pixmap:
                    icon_size = icon_pixmap.size()
                    icon_width = icon_size.width()
                    icon_height = icon_size.height()
                else:
                    icon_width = icon_height = 0

                logging.debug("Icon size set to: %dx%d", icon_width, icon_height)

                padding = 5  # Pixels between icon and text

                if self.animation_icon_position == "left":
                    self.animation_icon.setPos(-icon_width, -icon_width)
                    self.animation_text.setPos(0, 0)
                    logging.debug("Icon positioned to the left of text.")
                elif self.animation_icon_position == "right":
                    self.animation_icon.setPos(animation_text_rect.width(), -animation_text_rect.height() / 2)
                    self.animation_text.setPos(0, 0)
                    logging.debug("Icon positioned to the right of text.")
            else:
                # Center text if no icon
                self.animation_text.setPos(0, 0)
                logging.debug("No icon to position; text centered.")

        except Exception as e:
            logging.exception("Failed to layout items in AnimationObject: %s", e)

    def boundingRect(self):
        """
        Calculate the bounding rectangle that encompasses all child items.

        Returns:
            QRectF: The bounding rectangle for the item.
        """
        try:
            # Get the text's bounding rectangle translated to its position
            text_rect = self.animation_text.boundingRect().translated(self.animation_text.pos())

            if self.animation_icon:
                # Include the icon's bounding rectangle translated to its position
                icon_rect = self.animation_icon.pixmap_item.boundingRect().translated(self.animation_icon.pos())
                return text_rect.united(icon_rect)
            else:
                # If no icon, just return the text's bounding rectangle
                return text_rect
        except Exception as e:
            logging.exception("Failed to calculate bounding rectangle: %s", e)
            return QRectF()  # Return an empty rectangle as a fallback

    def paint(self, painter, option, widget=None):
        # self.animation_text.paint(painter, option, widget=None)
        # self.animation_icon.paint(painter, option, widget=None)
        pass

    def set_icon_position(self, position: str) -> None:
        """
        Sets the position of the icon relative to the text.

        Args:
            position (str): 'left' or 'right'
        """
        try:
            position = position.lower()
            if position in ["left", "right"]:
                self.animation_icon_position = position
                self.layout_items()
                logging.debug("Icon position set to '%s'.", position)
            else:
                logging.warning("Invalid icon position: '%s'. Must be 'left' or 'right'.", position)
        except Exception as e:
            logging.exception("Failed to set icon position: %s", e)
