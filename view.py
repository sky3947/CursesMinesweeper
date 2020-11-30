"""
This class is the View for the Minesweeper program.
"""

from abc import ABC, abstractmethod
from utility import Flow

class View(ABC):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        # A View communicates with a controller.
        self.controller = controller

        # A View needs to draw graphics.
        self.graphics = controller.graphics

        # The hovered input when entering this View.
        self.first_inp = ""

        # A list of UIElements in the View.
        self.uielements = []

        # True if the user is using interactable UI.
        self.using_ui = False

    @abstractmethod
    def parse(self, inp):
        """A scene could parse input and return an action."""

    def draw(self):
        """A scene could have graphics."""
        self.graphics.clear()

        for uielement in self.uielements:
            uielement.draw(self.graphics)

    def loop(self):
        """The main loop of a View."""
        while True:
            self.draw()

            action = self.parse(self.graphics.get_inp())
            flow = self.controller.act(action)

            if flow is Flow.RETURN:
                return

            if flow is Flow.BREAK:
                break

            if flow is Flow.CONTINUE:
                continue

            if flow is Flow.PASS:
                pass

        # If this portion is reached, stop the game loop.
        self.controller.stop_game_loop()
