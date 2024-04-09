"""
This program lets the user play Minesweeper using curses for input and
graphics.
"""

try:
    import curses
except ImportError:
    print("Curses module not found. Are you on Windows? Install it using 'pip install windows-curses'")
    exit(1)

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
