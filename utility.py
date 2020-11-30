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

# A Point consists of an x-coordinate and a y-coordinate.
Point = namedtuple("Point", "x y")

# An action has a primary input and an array of secondary inputs.
Action = namedtuple("Action", "primary secondary")
