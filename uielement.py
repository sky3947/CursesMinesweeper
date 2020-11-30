"""
This file contains UIElements for user interaction. A UIElement can be
extended to provide a variety of interactable UI.
"""

from enum import Enum
from abc import ABC, abstractmethod

class UIType(Enum):
    """An Enum used to easily differentiate UIElements."""
    TextBox = 0
    Button = 1

class UIElement(ABC):
    """UI elements provide methods for user interaction."""
    def __init__(self, uitype):
        # The type of UIElement this is.
        self.ui_type = uitype

    def get_type(self):
        """Each UIElement should have a unique type."""
        return self.ui_type

    def draw(self, graphics):
        """
        Draws this UIElement.

        Args:
            graphics (Graphics): The Graphics class with drawing
                functions.
        """
        tuples = self.to_tuples()
        for tup in tuples:
            graphics.draw(*tup)

    @abstractmethod
    def to_tuples(self):
        """
        A UIElement must return an array of tuples to represent itself.
        These tuples should draw this UIElement when unpacked as
        arguments for Graphics.draw.
        """

class TextBox(UIElement):
    """
    A TextBox is a UIElement used to display text.
    """
    def __init__(self, point, text):
        # Give this UIElement the TextBox UI type.
        super().__init__(UIType.TextBox)

        # The x and y-positions to start drawing text.
        self.point = point

        # The text to display.
        self.text = text

        # The default color.
        self.color = 0

    def set_color(self, color):
        """
        Sets the TextBox's color.

        Args:
            color (int): The new color.
        """
        self.color = color

    def to_tuples(self):
        return [(self.point, self.text, self.color)]
