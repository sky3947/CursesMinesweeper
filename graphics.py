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



    # Custom color options. These are based on predetermined curses
    # color_pair values. This was done so that these colors can be
    # stored as static values.

    # Black text color on white background.
    HIGHLIGHT = 256

    # White text on black background.
    BRIGHT = 512

    # Gray text color on black background.
    DIM = 768

    # Black text color on black background.
    DARKEST = 1024

    # White text color on red background.
    MINE = 1280



    # Special characters.

    # Enter key.
    ENTER_KEY = chr(10)

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

    def get_inp(self):
        """
        Gets a single-character input from the user.

        Returns:
            str: The character input from the user.
        """
        return chr(self.screen.getch())

    @staticmethod
    def win_draw(window, point, inp, color=BRIGHT):
        """
        Draws on a specified window.

        Args:
            window (_CursesWindow): The curses window to draw on.
            point (Point): The x and y location to draw at.
            inp (str): The string to draw.
            color (int, optional): The color to use. Defaults to BRIGHT.
        """
        window.addstr(point.y, point.x, inp, color)

    def draw(self, point, inp, color=BRIGHT):
        """
        Draws on the curses standard screen.

        Args:
            point (Point): The x and y location to draw at.
            inp (str): The string to draw.
            color (int, optional): the color to use. Defaults to BRIGHT.
        """
        self.win_draw(self.screen, point, inp, color)

    def clear(self, window=None, color=BRIGHT):
        """
        Clears a curses window.

        Args:
            window (_CursesWindow, optional): The window to clear.
                Defaults to self.screen.
            color (int, optional): the color to use. Defaults to BRIGHT.
        """
        window = window or self.screen
        for i in range(self.HEIGHT):
            self.draw(Point(0, i), " "*self.LENGTH, color)

    @staticmethod
    def center_just(y_pos, inp, win_len=LENGTH):
        """
        Center-justifies an input text.

        Args:
            y_pos (int): The y-position to draw at.
            input (str): The string to center-justify.
            win_len (int, optional): The length of the window. Defaults
                to self.LENGTH.

        Returns:
            (int, int, str): A tuple representing the center-justified
                input text (x, y, inp).
        """
        return ((win_len - len(inp))//2, y_pos, inp)

    @staticmethod
    def right_justify(y_pos, inp, win_len=LENGTH):
        """
        Right-justifies an input text.

        Args:
            y_pos (int): The y-position to draw at.
            inp (str): The string to right-justify.
            win_len (int, optional): The length of the window. Defaults
                to LENGTH.

        Returns:
            (int, int, str): A tuple representing the right-justified
                input text (x, y, inp).
        """
        return ((win_len - len(inp)), y_pos, inp)
