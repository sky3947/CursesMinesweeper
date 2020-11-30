"""
This class is the view for the Minesweeper program.
"""

from abc import ABC, abstractmethod
from utility import Flow

class View(ABC):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    # A View communicates with a controller.
    controller = None

    # A View needs to draw graphics.
    graphics = None

    # The hovered input when entering this View.
    first_inp = ""

    @abstractmethod
    def parse(self, inp):
        """A scene could parse input and return an action."""

    @abstractmethod
    def draw(self):
        """A scene could have graphics."""

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
