"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        """
        Constructs an instance of MainMenuView and returns it.

        Args:
            controller (Controller): The controller to pass user
                interactions to.
        """
        # The View delivers user input to the Controller.
        self.controller = controller

        # The View uses Graphics to draw.
        self.graphics = controller.graphics

        # The hovered input when entering the main menu.
        self.first_inp = "m"

    def parse(self, inp):
        """
        Parses input and returns an Action. UI-related interactions are
        handled here.

        Args:
            inp (str): The user input.

        Returns:
            Action: The action to perform.
        """
        return Action("", [])

    def draw(self):
        """
        Draws the main menu.
        """
        graph = self.graphics
        graph.clear()

        graph.draw(Point(0, 0), "main menu reached", graph.BRIGHT)
