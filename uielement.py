"""
This file contains UIElements for user interaction. A UIElement can be
extended to provide a variety of interactable UI.
"""

import textwrap
from enum import Enum
from abc import ABC, abstractmethod
from utility import Point
from graphics import Graphics

class UIType(Enum):
    """An Enum used to easily differentiate UIElements."""
    TextBox = 0
    LongTextBox = 1
    Button = 2
    Popup = 3

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

        # A UIElement can be disabled.
        self.enabled = True

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

    def set_enabled(self, enabled):
        """
        Sets this Button's enabled flag.

        Args:
            enabled (bool): The new enabled flag.
        """
        self.enabled = enabled

    def is_enabled(self):
        """
        Checks this Button's enabled flag.

        Returns:
            bool: The enabled flag.
        """
        return self.enabled

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
        if tuples is None:
            return
        for tup in tuples:
            graphics.draw(*tup)

    @abstractmethod
    def to_tuples(self):
        """
        A UIElement must return an array of tuples to represent itself.
        These tuples should draw this UIElement when unpacked as
        arguments for Graphics.draw.
        """

class Popup(UIElement):
    """
    A Popup prompts for a Y/N response.
    """
    def __init__(self, point, title="CONTINUE ON?", text=""):
        # Give this UIElement the Popup UI type.
        super().__init__(UIType.Popup, point)

        # The title of the Popup.
        self.title = title

        # The text to display.
        self.text = text

        # If False, "No" is hovered. If True, "Yes" is hovered.
        self.option = False

        # The primary color when drawing the Popup.
        self.primary_color = 0

        # The title color when drawing the Popup.
        self.title_color = 0

        # The secondary color when drawing the Popup.
        self.secondary_color = 0

        # The highlight color when drawing Y and N options.
        self.highlight_color = 0

    def set_title(self, title):
        """
        Sets the title of this Popup.

        Args:
            title (str): The new title.
        """
        self.title = title

    def set_text(self, text):
        """
        Sets the text of this Popup.

        Args:
            text (str): The new text.
        """
        self.text = text

    def set_option(self, option):
        """
        Sets the hovered option.

        Args:
            option (bool): The new hovered option.
        """
        self.option = option

    def set_primary_color(self, color):
        """
        Sets the primary color.

        Args:
            color (int): The new primary color.
        """
        self.primary_color = color

    def set_title_color(self, color):
        """
        Sets the title color.

        Args:
            color (int): The new title color.
        """
        self.title_color = color

    def set_secondary_color(self, color):
        """
        Sets the secondary color.

        Args:
            color (int): The new secondary color.
        """
        self.secondary_color = color

    def set_highlight_color(self, color):
        """
        Sets the highlight color.

        Args:
            color (int): The new highlight color.
        """
        self.highlight_color = color

    def to_tuples(self):
        lines = []

        # Background
        for i in range(10):
            t_point = Point(0, self.point.y+i)
            lines.append((t_point, " "*Graphics.LENGTH, self.primary_color))

        # Top and bottom borders.
        t_point = Point(0, self.point.y)
        lines.append((t_point, "="*Graphics.LENGTH, self.primary_color))
        t_point = Point(0, self.point.y+9)
        lines.append((t_point, "="*Graphics.LENGTH, self.primary_color))

        # Title.
        t_point = Point(10, self.point.y+1)
        lines.append((t_point, " "*(Graphics.LENGTH-20), self.title_color))
        t_point = Point((Graphics.LENGTH-len(self.title))//2, self.point.y+1)
        lines.append((t_point, self.title, self.title_color))

        # Exclamation mark decorations.
        for i in range(2):
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+1)
            lines.append((t_point, " _ ", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+2)
            lines.append((t_point, "| |", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+3)
            lines.append((t_point, "| |", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+4)
            lines.append((t_point, "| |", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+5)
            lines.append((t_point, "!_!", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+6)
            lines.append((t_point, " _ ", self.secondary_color))
            t_point = Point(i*(Graphics.LENGTH-10)+3, self.point.y+7)
            lines.append((t_point, "!_!", self.secondary_color))

        # Text.
        wrapper = textwrap.TextWrapper(width=40, max_lines=6)
        wrapped = wrapper.wrap(self.text)
        t_point = Point(10, self.point.y+7)
        lines.append((t_point, " "*(Graphics.LENGTH-20), self.title_color))
        for i, text in enumerate(wrapped):
            t_point = Point(10, self.point.y+i+2)
            if i != 6:
                lines.append((t_point, text, self.primary_color))
            else:
                lines.append((t_point, text, self.title_color))

        # N and Y selection.
        n_point = Point(24, self.point.y+8)
        n_color = self.primary_color if self.option else self.highlight_color
        y_point = Point(Graphics.LENGTH-25, self.point.y+8)
        y_color = self.highlight_color if self.option else self.primary_color
        lines.append((n_point, "N", n_color))
        lines.append((y_point, "Y", y_color))

        return lines

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

    def is_hovered(self):
        """
        Checks this Button's hovered flag.

        Returns:
            bool: The hovered flag.
        """
        return self.hovered

    def to_tuples(self):
        color = self.color
        if not self.is_enabled():
            color = self.disabled_color
        elif self.is_hovered():
            color = self.hovered_color
        return [(self.point, self.text, color)]

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
