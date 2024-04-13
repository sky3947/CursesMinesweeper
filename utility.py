"""
This file contains useful structures that are used in many parts of the
project code.
"""

from enum import Enum
from collections import namedtuple

class Flow(Enum):
    """An Enum used to provide flow control."""
    PASS = 0
    BREAK = 1
    CONTINUE = 2
    RETURN = 3

class Direction(Enum):
    """An Enum used to represent 2D directions."""
    U = 0
    L = 1
    D = 2
    R = 3

class State(Enum):
    """An Enum used to represent the state of the game."""
    RUNNING = 0
    WON = 1
    LOST = 2

# A Point consists of an x-coordinate and a y-coordinate.
Point = namedtuple("Point", "x y")

# An Option consists of length, height, and density integers.
Option = namedtuple("Option", "l h d")

# An action has a primary input and an array of secondary inputs.
Action = namedtuple("Action", "primary secondary")

def get_color(value, hovered, indicator_colors, hovered_indicator_colors):
    """
    Returns the color for the given value.

    Args:
        graphics (Graphics): The graphics object.
        value (int): The value to get the color for.
        hovered (bool): Whether or not the value is hovered.
    """
    if value == 0 or value > len(indicator_colors) + 1:
        return None
    
    return (hovered_indicator_colors[value - 1]
            if hovered
            else indicator_colors[value - 1])
