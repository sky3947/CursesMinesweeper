"""
This file contains UIElements for user interaction. A UIElement can be
extended to provide a variety of interactable UI.
"""

from enum import Enum
from abc import ABC, abstractmethod
from utility import Point

class UIType(Enum):
    """An Enum used to easily differentiate UIElements."""
    TextBox = 0
    LongTextBox = 1
    Button = 2

class UIElement(ABC):
    """UI elements provide methods for user interaction."""
    def __init__(self, uitype, point):
        """
        Constructs a UIElement and returns it.

        Args:
            uitype (UIType): The UIType of this UIElement.
            point (Point): The x and y-location of this UIElement.
        """
        # The type of UIElement this is.
        self.ui_type = uitype

        # The x and y-location of this UIElement.
        self.point = point

        # The default color.
        self.color = 0

        # The function to be executed when the UIElement is clicked.
        self.action = lambda: None

    def get_type(self):
        """
        Returns this UIElement's UIType.

        Returns:
            UIType: This UIElement's UIType.
        """
        return self.ui_type

    def set_location(self, point):
        """
        Sets this UIElement's x and y locations.

        Args:
            point (Point): The new x and y-positions of this UIElement.
        """
        self.point = point

    def set_color(self, color):
        """
        Sets this UIElement's color.

        Args:
            color (int): The new color.
        """
        self.color = color

    def set_action(self, action):
        """
        Sets this UIElement's action.

        Args:
            action (lambda): The function to execute when this UIElement
                is clicked.
        """
        self.action = action

    def click(self, params=()):
        """
        Executes this UIElement's action.

        Args:
            params (tuple, optional): Function parameters to be
                unpacked. Defaults to ().

        Returns:
            Any: Returns the result of this UIElement's action function.
        """
        return self.action(*params)

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
    def __init__(self, point, text="TextBox"):
        """
        Constructs a TextBox and returns it.

        Args:
            point (Point): The x and y-positions of this TextBox.
            text (str): The text to display.
        """
        # Give this UIElement the TextBox UI type.
        super().__init__(UIType.TextBox, point)

        # The text to display.
        self.text = text

    def set_text(self, text):
        """
        Sets the text of this TextBox.

        Args:
            text (str): The new text.
        """
        self.text = text

    def to_tuples(self):
        return [(self.point, self.text, self.color)]

class LongTextBox(UIElement):
    """
    A LongTextBox is a UIElement used to display a block of text.
    """
    def __init__(self, point, lines=("LongTextBox",)):
        """
        Constructs a LongTextBox and returns it.

        Args:
            point (Point): The x and y-positions of this LongTextBox.
            lines (list): The lines of text to display.
        """
        # Give this UIElement the LongTextBox UI type.
        super().__init__(UIType.LongTextBox, point)

        # The block of text to display.
        self.lines = lines

    def set_lines(self, lines):
        """
        Sets the block of text to display.

        Args:
            lines (list): The new block of text.
        """
        self.lines = lines

    def to_tuples(self):
        x = self.point.x
        y = self.point.y
        lines = enumerate(self.lines)
        return [(Point(x, y+dy), line, self.color) for dy, line in lines]

class Button(UIElement):
    """
    A Button is a UIElement that can be hovered, disabled, and clicked.
    """
    def __init__(self, point, text="Button"):
        """
        Constructs a Button and returns it.

        Args:
            point (Point): The x and y-positions of this Button.
            text (str): The text to display.
        """
        # Give this UIElement the Button UI type.
        super().__init__(UIType.Button, point)

        # The text to display.
        self.text = text

        # The hovered color.
        self.hovered_color = 0

        # The disabled color.
        self.disabled_color = 0

        # A Button can be hovered.
        self.hovered = False

        # A disabled button uses disabled_color.
        self.enabled = True

    def set_text(self, text):
        """
        Sets the text of this Button.

        Args:
            text (str): The new text.
        """
        self.text = text

    def set_hovered_color(self, color):
        """
        Sets this Button's hovered color.

        Args:
            color (int): The new color.
        """
        self.hovered_color = color

    def set_disabled_color(self, color):
        """
        Sets this Button's disabled color.

        Args:
            color (int): The new color.
        """
        self.disabled_color = color

    def set_hovered(self, hovered):
        """
        Sets this Button's hovered flag.

        Args:
            hovered (bool): The new hovered flag.
        """
        self.hovered = hovered

    def set_enabled(self, enabled):
        """
        Sets this Button's enabled flag.

        Args:
            enabled (bool): The new enabled flag.
        """
        self.enabled = enabled

    def is_hovered(self):
        """
        Checks this Button's hovered flag.

        Returns:
            bool: The hovered flag.
        """
        return self.hovered_color

    def is_enabled(self):
        """
        Checks this Button's enabled flag.

        Returns:
            bool: The enabled flag.
        """
        return self.enabled

    def to_tuples(self):
        color = self.color
        if not self.is_enabled():
            color = self.disabled_color
        elif self.is_hovered():
            color = self.hovered_color
        return [(self.point, self.text, color)]
