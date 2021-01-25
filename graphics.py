"""
This file provides functions to interface with the curses library.
"""

import curses
from utility import Point

class Graphics:
    """
    A class for interfacting with curses functions.
    """
    # The length and height of the draw window.
    LENGTH = 60
    HEIGHT = 30



    # Text decoration options.

    # The color option to underline text.
    UNDERLINE = curses.A_UNDERLINE



    # Special characters.

    # Enter key.
    ENTER_KEY = chr(10)

    # Backspace key.
    BACKSPACE_KEY = chr(263)

    # Symbol used for mines.
    MINE_KEY = chr(0x00A4)



    def __init__(self, screen):
        """
        Constructs an instance of Graphics and returns it.

        Args:
            screen (_CursesWindow): A standard screen object from the
                curses library.
        """
        # The curses standard screen.
        self.screen = screen

        # Initialize custom color options.
        curses.init_pair(1, 16, 231)
        curses.init_pair(2, 231, 16)
        curses.init_pair(3, 240, 16)
        curses.init_pair(4, 16, 16)
        curses.init_pair(5, 231, 1)

        # Black text color on white background.
        self.HIGHLIGHT = curses.color_pair(1)

        # White text on black background.
        self.BRIGHT = curses.color_pair(2)

        # Gray text color on black background.
        self.DIM = curses.color_pair(3)

        # Black text color on black background.
        self.DARKEST = curses.color_pair(4)

        # White text color on red background.
        self.MINE = curses.color_pair(5)

    def get_inp(self):
        """
        Gets a single-character input from the user.

        Returns:
            str: The character input from the user.
        """
        return chr(self.screen.getch())

    def draw(self, point, inp, color=None):
        """
        Draws on the curses standard screen.

        Args:
            point (Point): The x and y location to draw at.
            inp (str): The string to draw.
            color (int, optional): the color to use. Defaults to BRIGHT.
        """
        self.screen.addstr(point.y, point.x, inp, color or self.BRIGHT)

    def clear(self, color=None):
        """
        Clears the curses window.

        Args:
            color (int, optional): the color to use. Defaults to BRIGHT.
        """
        for i in range(self.HEIGHT):
            self.draw(Point(0, i), " "*self.LENGTH, color or self.BRIGHT)

    @staticmethod
    def center_just(y, inp, win_len=LENGTH):
        """
        Center-justifies an input text.

        Args:
            y (int): The y-position to draw at.
            input (str): The string to center-justify.
            win_len (int, optional): The length of the window. Defaults
                to self.LENGTH.

        Returns:
            (int, int, str): A tuple representing the center-justified
                input text (x, y, inp).
        """
        return (Point((win_len - len(inp))//2, y), inp)

    @staticmethod
    def right_justify(y, inp, win_len=LENGTH):
        """
        Right-justifies an input text.

        Args:
            y (int): The y-position to draw at.
            inp (str): The string to right-justify.
            win_len (int, optional): The length of the window. Defaults
                to LENGTH.

        Returns:
            (int, int, str): A tuple representing the right-justified
                input text (x, y, inp).
        """
        return (Point((win_len - len(inp)), y), inp)
