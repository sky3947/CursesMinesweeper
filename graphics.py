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

    # Windows backspace key.
    WIN_BACKSPACE_KEY = chr(8)

    # Symbol used for mines.
    MINE_KEY = chr(0x00A4)

    # Symbol used for closed cells.
    CELL_KEY = chr(0x00B7)



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
        curses.init_pair(5, 196, 234)
        curses.init_pair(6, 231, 234)
        curses.init_pair(7, 240, 234)
        curses.init_pair(8, 240, 231)
        curses.init_pair(9, 196, 231)
        curses.init_pair(10, 226, 234)
        curses.init_pair(11, 226, 16)
        curses.init_pair(12, 226, 234)
        curses.init_pair(13, 234, 231)

        # Black text color on white background.
        self.HIGHLIGHT = curses.color_pair(1)
        # White text on black background.
        self.BRIGHT = curses.color_pair(2)
        # Gray text color on black background.
        self.DIM = curses.color_pair(3)
        # Black text color on black background.
        self.DARKEST = curses.color_pair(4)
        # Red text color on dark gray background.
        self.MINE = curses.color_pair(5)
        # White text color on a dark gray background.
        self.CARD = curses.color_pair(6)
        # Gray text color on a dark gray background.
        self.DIM_CARD = curses.color_pair(7)
        # Gray text color on a white background.
        self.HIGHLIGHT_DIM_CARD = curses.color_pair(8)
        # Red text color on a white background.
        self.HIGHLIGHT_MINE = curses.color_pair(9)
        # Yellow text color on a dark gray background.
        self.INDICATOR = curses.color_pair(10)
        # Yellow text color on a black background.
        self.YELLOW = curses.color_pair(11)
        # Yellow text color on a dark gray background.
        self.YELLOW_CARD = curses.color_pair(12)
        # Dark gray text color on a white background.
        self.HIGHLIGHT_YELLOW_CARD = curses.color_pair(13)

        # Initialize mine indicator color options.
        curses.init_pair(14, 33, 234)
        curses.init_pair(15, 33, 231)
        curses.init_pair(16, 34, 234)
        curses.init_pair(17, 34, 231)
        curses.init_pair(18, 160, 234)
        curses.init_pair(19, 160, 231)
        curses.init_pair(20, 21, 234)
        curses.init_pair(21, 21, 231)
        curses.init_pair(22, 88, 234)
        curses.init_pair(23, 88, 231)
        curses.init_pair(24, 31, 234)
        curses.init_pair(25, 31, 231)
        curses.init_pair(26, 16, 234)
        curses.init_pair(27, 16, 231)
        curses.init_pair(28, 240, 234)
        curses.init_pair(29, 240, 231)

        # Bright blue text color on dark gray background.
        self.INDICATOR_BRIGHT_BLUE = curses.color_pair(14)
        self.HIGHLIGHT_INDICATOR_BRIGHT_BLUE = curses.color_pair(15)
        # Green text color on dark gray background.
        self.INDICATOR_GREEN = curses.color_pair(16)
        self.HIGHLIGHT_INDICATOR_GREEN = curses.color_pair(17)
        # Bright red text color on dark gray background.
        self.INDICATOR_BRIGHT_RED = curses.color_pair(18)
        self.HIGHLIGHT_INDICATOR_BRIGHT_RED = curses.color_pair(19)
        # Dark blue text color on dark gray background.
        self.INDICATOR_DARK_BLUE = curses.color_pair(20)
        self.HIGHLIGHT_INDICATOR_DARK_BLUE = curses.color_pair(21)
        # Dark red text color on dark gray background.
        self.INDICATOR_DARK_RED = curses.color_pair(22)
        self.HIGHLIGHT_INDICATOR_DARK_RED = curses.color_pair(23)
        # Cyan text color on dark gray background.
        self.INDICATOR_CYAN = curses.color_pair(24)
        self.HIGHLIGHT_INDICATOR_CYAN = curses.color_pair(25)
        # Black text color on dark gray background.
        self.INDICATOR_BLACK = curses.color_pair(26)
        self.HIGHLIGHT_INDICATOR_BLACK = curses.color_pair(27)
        # Gray text color on dark gray background.
        self.INDICATOR_GRAY = curses.color_pair(28)
        self.HIGHLIGHT_INDICATOR_GRAY = curses.color_pair(29)

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
        try:
            self.screen.addstr(point.y, point.x, inp, color or self.BRIGHT)
        except:
            curses.resize_term(self.HEIGHT, self.LENGTH)

    def refresh(self):
        """
        Refreshes the screen for threading purposes.
        """
        self.screen.refresh()

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

    @staticmethod
    def flush_inp():
        """
        Flushes the input buffer of keys pressed.
        """
        curses.flushinp()
