"""
This program lets the user play Minesweeper using curses for input and
graphics.
"""

import curses
from model import Model

def main(screen):
    """
    The main function to be used by the curses wrapper.

    Args:
        screen (_CursesWindow): The screen to be used for graphics.
    """
    curses.curs_set(False)

    game = Model(screen)
    game.start()

if __name__ == "__main__":
    curses.wrapper(main)
