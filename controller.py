"""
This class is the controller for the Minesweeper program.
"""

from graphics import Graphics
from utility import Flow

class Controller:
    """
    Translates user input from views to changes in the model.
    """

    def __init__(self, model, screen):
        """
        Constructs an instance of Controller and returns it.

        Args:
            model (Model): The Minesweeper model.
            screen (_CursesWindow): A standard screen object from the
                curses library.
        """
        # The Minesweeper model.
        self.model = model

        # The Graphics class for user input and drawing.
        self.graphics = Graphics(screen)

    def stop_game_loop(self):
        """
        Tells the model to stop the game loop.
        """
        self.model.stop_game_loop()

    def change_view(self, view):
        """
        Tells the model to change the view.

        Args:
            view (View): The next view.
        """
        self.model.change_view(view)

    def act(self, action):
        """
        Responds to input from a View.

        Args:
            action (Action): The Action to perform.

        Returns:
            Flow: The control flow to pass to the View.
        """
        return Flow.PASS
