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
    NumberField = 4

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

        # A UIElement can be disabled. (Disabled => no drawing.)
        self.enabled = True

        # The function to be executed when the UIElement is clicked.
        self.action = lambda: None

        # A focusable UIElement should have controls.
        self.focusable = False

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

    def is_focusable(self):
        """
        Checks if this UIElement is focusable.

        Returns:
            bool: True if focusable, False otherwise.
        """
        return self.focusable

    def draw(self, graphics):
        """
        Draws this UIElement.

        Args:
            graphics (Graphics): The Graphics class with drawing
                functions.
        """
        tuples = self.to_tuples()
        if tuples is None or not self.is_enabled():
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

class FocusableUIElement(UIElement):
    """
    A FocusableUIElement has re-defineable controls.
    """
    def __init__(self, uitype, point):
        """
        Constructs a FocusableUIElement and returns it.

        Args:
            uitype (UIType): The UIType of this FocusableUIElement.
            point (Point): The x and y-location of this
                FocusableUIElement.
        """
        # Provide FocusableUIElement parameters.
        super().__init__(uitype, point)

        # This FocusableUIElement is focusable.
        self.focusable = True

        # Blocks controls from the View if True.
        self.blocking = True

        # A FocusableUIElement has View-defined controls.
        self.controls = {}

    def set_controls(self, controls):
        """
        Sets the controls of this FocusableUIElement.

        Args:
            controls (dict): The set of controls to use.
        """
        self.controls = controls

    def is_blocking(self):
        """
        Checks if this FocusableUIElement is blocking other input.

        Returns:
            bool: The blocking boolean.
        """
        return self.blocking

    def change_control(self, name, value):
        """
        Changes one of the controls mappings of this FocusableUIElement.

        Args:
            name (str): The name field.
            value (Any): The value field.
        """
        self.controls[name] = value

class NumberField(FocusableUIElement):
    """
    A NumberField allows the user to provide number inputs.
    """
    def __init__(self, point, value, maximum):
        """
        Constructs a NumberField and returns it.

        Args:
            point (Point): The x and y-positions of a NumberField.
            value (int): The starting value.
            maximum (int): The maximum value.
        """
        # Give this UIElement the NumberField UI type and starting Point.
        super().__init__(UIType.NumberField, point)

        # Doesn't block other UIElement controls.
        self.blocking = False

        # The minimum value of this NumberField.
        self.minimum = min(value, 0)

        # The maximum value of this NumberField.
        self.maximum = maximum

        # The current value of this NumberField.
        self.value = min(value, maximum)

        # The minimum (drawn) length of this NumberField.
        self.min_length = 0

        # An inactive NumberField uses inactive_color.
        self.active = True

        # A NumberField can be hovered.
        self.hovered = False

        # Drawing parameters.
        self.decorations = {
            # The prefix to draw.
            "prefix": "",

            # The postfix to draw.
            "postfix": "",

            # The color to use when hovering this NumberField.
            "hovered color": 0,

            # The color to use when this NumberField is inactive.
            "inactive color": 0,

            # Left justify the value.
            "left justify": True
        }

        # Controls.
        self.controls = {
            Graphics.BACKSPACE_KEY: self.backspace,
            Graphics.WIN_BACKSPACE_KEY: self.backspace,
            "0": lambda: self.add_digit(0),
            "1": lambda: self.add_digit(1),
            "2": lambda: self.add_digit(2),
            "3": lambda: self.add_digit(3),
            "4": lambda: self.add_digit(4),
            "5": lambda: self.add_digit(5),
            "6": lambda: self.add_digit(6),
            "7": lambda: self.add_digit(7),
            "8": lambda: self.add_digit(8),
            "9": lambda: self.add_digit(9)
        }

    def add_digit(self, digit):
        """
        Appends a digit to the end of the value.

        Args:
            digit (int): The digit to append.
        """
        self.set_value(self.value*10 + digit)
        if self.value > self.maximum:
            self.fix_bounds()

    def backspace(self):
        """
        Divides the value by 10 (pressing backspace.)
        """
        self.set_value(self.value//10)

    def set_minimum(self, minimum):
        """
        Sets the new minimum value.

        Args:
            minimum (int): The new minimum value.
        """
        self.minimum = minimum
        self.value = max(self.value, minimum)

    def set_maximum(self, maximum):
        """
        Sets the new maximum value.

        Args:
            maximum (int): The new maximum value.
        """
        self.maximum = maximum
        self.value = min(self.minimum, maximum)

    def set_value(self, value):
        """
        Sets the new value. This value can be out of bounds.

        Args:
            value (int): The new value.
        """
        self.value = value

    def fix_bounds(self):
        """
        Makes sure the value is in-bounds.
        """
        self.value = min(max(self.value, self.minimum), self.maximum)

    def set_min_length(self, length):
        """
        Sets the minimum length.

        Args:
            length (int): The new minimum length of the NumberField.
        """
        self.min_length = length

    def set_prefix(self, prefix):
        """
        Sets the prefix to draw before the value.

        Args:
            prefix (str): The prefix.
        """
        self.decorations["prefix"] = prefix

    def set_postfix(self, postfix):
        """
        Sets the postfix to draw after the value.

        Args:
            postfix (str): The postfix.
        """
        self.decorations["postfix"] = postfix

    def set_hovered_color(self, color):
        """
        Sets the hovered color of this NumerField.

        Args:
            color (int): A curses color.
        """
        self.decorations["hovered color"] = color

    def set_inactive_color(self, color):
        """
        Sets the inactive color of this NumberField.

        Args:
            color (int): A curses color.
        """
        self.decorations["inactive color"] = color

    def set_left_justify(self, boolean):
        """
        Sets the left-justify boolean value of this NumberField.

        Args:
            boolean (bool): True to left-justify, False to
                right-justify.
        """
        self.decorations["left justify"] = boolean

    def set_active(self, active):
        """
        Sets a new active value.

        Args:
            active (bool): The new active value.
        """
        self.active = active

    def is_active(self):
        """
        Checks the active flag.

        Returns:
            bool: The active flag.
        """
        return self.active

    def set_hovered(self, hovered):
        """
        Sets this NumberField's hovered flag.

        Args:
            hovered (bool): The new hovered flag.
        """
        self.hovered = hovered

    def is_hovered(self):
        """
        Checks this NumberField's hovered flag.

        Returns:
            bool: The hovered flag.
        """
        return self.hovered

    def to_tuples(self):
        # Colors
        text_color = self.color
        value_color = self.color
        if not self.is_active():
            text_color = self.decorations["inactive color"]
            value_color = self.decorations["inactive color"]
        elif self.is_hovered():
            value_color = self.decorations["hovered color"]

        tuples = []

        # Prefix.
        t_point = self.point
        tuples.append((t_point, self.decorations["prefix"], text_color))

        # Value.
        new_x = t_point.x + len(self.decorations["prefix"])
        t_point = Point(new_x, t_point.y)
        text = str(self.value)
        text_length = max(len(text), self.min_length)
        tuples.append((t_point, " "*text_length, value_color))
        if not self.decorations["left justify"]:
            new_x = t_point.x + text_length - len(text)
            s_t_point = Point(new_x, t_point.y)
            tuples.append((s_t_point, str(self.value), value_color))
        else:
            tuples.append((t_point, str(self.value), value_color))

        # Postfix.
        new_x = t_point.x + text_length
        t_point = Point(new_x, t_point.y)
        tuples.append((t_point, self.decorations["postfix"], text_color))

        return tuples

class Popup(FocusableUIElement):
    """
    A Popup prompts for a Y/N response.
    """
    def __init__(self, point, view, title="CONTINUE ON?", text=""):
        """
        Constructs a Popup and returns it.

        Args:
            point (Point): The x and y-positions of this Popup.
            title (str, optional): The title of this Popup. Defaults to
                "CONTINUE ON?".
            text (str, optional): The text to show in this Popup.
                Defaults to "".
        """
        # Give this UIElement the Popup UI type.
        super().__init__(UIType.Popup, point)

        # Keep track of the View so this UIElement can be unfocused.
        self.view = view

        # The title of the Popup.
        self.title = title

        # The text to display.
        self.text = text

        # If False, "No" is hovered. If True, "Yes" is hovered.
        self.option = False

        # Drawing parameters.
        self.decorations = {
            # The title color when drawing the Popup.
            "title color": 0,

            # The secondary color when drawing the Popup.
            "secondary color": 0,

            # The highlight color when drawing Y and N options.
            "highlight color": 0
        }

        # Controls.
        self.controls = {
            "q": self.reset_popup,
            "w": lambda: self.set_option(not self.get_option()),
            "a": lambda: self.set_option(not self.get_option()),
            "s": lambda: self.set_option(not self.get_option()),
            "d": lambda: self.set_option(not self.get_option()),
            Graphics.ENTER_KEY: lambda: self.set_option(not self.get_option()),
            "m": self.click_action
        }

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

    def get_option(self):
        """
        Gets the hovered option.

        Returns:
            bool: The hovered option.
        """
        return self.option

    def set_title_color(self, color):
        """
        Sets the title color.

        Args:
            color (int): The new title color.
        """
        self.decorations["title color"] = color

    def set_secondary_color(self, color):
        """
        Sets the secondary color.

        Args:
            color (int): The new secondary color.
        """
        self.decorations["secondary color"] = color

    def set_highlight_color(self, color):
        """
        Sets the highlight color.

        Args:
            color (int): The new highlight color.
        """
        self.decorations["highlight color"] = color

    def reset_popup(self):
        """
        Closes the Popup.
        """
        self.set_enabled(False)
        self.set_option(False)
        self.view.set_focused_ui(None)

    def click_action(self, params=()):
        """
        Resets the Popup and returns the click function's result.

        Args:
            params (tuple, optional): Function parameters for the click
                function. Defaults to ().
        """
        result = self.click(params)
        self.reset_popup()
        return result

    def to_tuples(self):
        # Colors
        title_color = self.decorations["title color"]
        secondary_color = self.decorations["secondary color"]
        highlight_color = self.decorations["highlight color"]

        tuples = []

        # Background
        for i in range(10):
            t_point = Point(0, self.point.y+i)
            tuples.append((t_point, " "*Graphics.LENGTH, self.color))

        # Top and bottom borders.
        t_point = Point(0, self.point.y)
        tuples.append((t_point, "="*Graphics.LENGTH, self.color))
        t_point = Point(0, self.point.y+9)
        tuples.append((t_point, "="*Graphics.LENGTH, self.color))

        # Title.
        t_point = Point(9, self.point.y+1)
        if title_color & Graphics.UNDERLINE:
            tuples.append((t_point, "_"*(Graphics.LENGTH-18), title_color))
        else:
            tuples.append((t_point, " "*(Graphics.LENGTH-18), title_color))
        t_point = Point((Graphics.LENGTH-len(self.title))//2, self.point.y+1)
        tuples.append((t_point, self.title, title_color))

        # Exclamation mark decorations.
        for i in range(2):
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+1)
            tuples.append((t_point, " _ ", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+2)
            tuples.append((t_point, "| |", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+3)
            tuples.append((t_point, "| |", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+4)
            tuples.append((t_point, "| |", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+5)
            tuples.append((t_point, "!_!", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+6)
            tuples.append((t_point, " _ ", secondary_color))
            t_point = Point(i*(Graphics.LENGTH-9)+3, self.point.y+7)
            tuples.append((t_point, "!_!", secondary_color))

        # Text.
        wrapper = textwrap.TextWrapper(width=40, max_lines=5)
        wrapped = wrapper.wrap(self.text)
        t_point = Point(10, self.point.y+7)
        if title_color & Graphics.UNDERLINE:
            tuples.append((t_point, "_"*(Graphics.LENGTH-20), title_color))
        else:
            tuples.append((t_point, " "*(Graphics.LENGTH-20), title_color))
        for i, text in enumerate(wrapped):
            t_point = Point(10, self.point.y+i+2)
            tuples.append((t_point, text, self.color))

        # N and Y selection.
        n_point = Point(24, self.point.y+8)
        n_color = self.color if self.option else highlight_color
        y_point = Point(Graphics.LENGTH-25, self.point.y+8)
        y_color = highlight_color if self.option else self.color
        tuples.append((n_point, "N", n_color))
        tuples.append((y_point, "Y", y_color))

        return tuples

class Button(UIElement):
    """
    A Button is a UIElement that can be hovered, deactivated, and
    clicked.
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

        # Drawing parameters.
        self.decorations = {
            # The color of this Button when it's hovered.
            "hovered color": 0,

            # The color of this Button when it's inactive.
            "inactive color": 0
        }

        # An inactive Button uses inactive_color.
        self.active = True

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
        self.decorations["hovered color"] = color

    def set_inactive_color(self, color):
        """
        Sets this Button's disabled color.

        Args:
            color (int): The new color.
        """
        self.decorations["inactive color"] = color

    def set_active(self, active):
        """
        Sets a new active value.

        Args:
            active (bool): The new active value.
        """
        self.active = active

    def is_active(self):
        """
        Checks this Button's active flag.

        Returns:
            bool: The Button's active flag.
        """
        return self.active

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
        if not self.is_active():
            color = self.decorations["inactive color"]
        elif self.is_hovered():
            color = self.decorations["hovered color"]
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
