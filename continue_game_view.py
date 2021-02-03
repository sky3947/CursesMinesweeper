"""
The continue game View provides is an intermediate View to inform the
user that the minefield is loading.
"""

from view import View
from utility import Action

class ContinueGameView(View):
    """
    Intermediate View for loading the minefield from a file.
    """

    # Override the View loop so that user input is not queried.
    def loop(self):
        self.graphics.clear()

        # Drawing text.
        params = self.graphics.center_just(14, "Loading minefield...")
        self.graphics.draw(*params)

        # Load minefield.
        self.controller.load_minefield()

        # TODO: Redirect to game view.
        self.controller.act(Action("goto main menu view", []))
