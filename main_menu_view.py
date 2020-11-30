"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point
from uielement import TextBox

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        super().__init__(controller)

        self.test_text = TextBox(Point(0, 10), "test textbox")
        self.test_text.set_color(self.graphics.BRIGHT)

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

        self.test_text.draw(graph)
