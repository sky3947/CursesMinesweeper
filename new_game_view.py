"""
The new game View provides options to choose a customized minesweeper
difficulty.
"""

from view import View
from utility import Point, Action
from uielement import TextBox

class NewGameView(View):
    """
    Draws UIElements for customizing a new minefield.
    """
    def __init__(self, controller):
        """
        Instantiates a NewGameView and returns it.

        Args:
            controller (Controller): The controller to pass user input.
        """
        super().__init__(controller)

        # The hovered input when entering this View.
        self.first_inp = "s"

        # Initialize selected variable.
        self.selected = None

        # Map of input to functions.
        self.controls = {
            # Pressing "q" will go back to the main menu.
            "q": lambda: Action("goto main menu view", [])
        }

        # Testing area
        textbox = TextBox(Point(0, 0), "Reached New Game View")
        self.uielements.append(textbox)
