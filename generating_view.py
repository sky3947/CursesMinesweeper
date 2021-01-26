"""
The generating View provides information to user as the minefield
is being generated. Then, the user is redirected to the game View. This
is not an interactable View.
"""

from view import View
from utility import Action, Point

class GeneratingView(View):
    """
    Provides user with progress updates to minefield generation.
    """
    def __init__(self, controller):
        """
        Instantiates a GeneratingView and returns it.

        Args:
            controller (Controller): The controller to pass user input.
        """
        super().__init__(controller)

        # Updated to show minefield generation progress.
        self.progress = 0

    # Override the View loop so that user input is not queried.
    def loop(self):
        while self.progress < 50000:
            graphics = self.graphics
            graphics.clear()
            params = graphics.center_just(14, "Generating minefield..")
            graphics.draw(*params)
            graphics.draw(Point(0, 0), str(self.progress))
            graphics.refresh()
            self.progress += 1
        self.controller.act(Action("goto main menu view", []))
