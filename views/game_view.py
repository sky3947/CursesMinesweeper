"""
The game View is the main View for the game. It displays the minefield to the
user and lets them interact with it.
"""

from uielement import LongTextBox
from utility import Action, Point
from views.view import View


class GameView(View):
    def __init__(self, controller):
        """
        Instantiates a GameView and returns it.

        Args:
            controller (Controller): The Controller to pass user input.
        """
        super().__init__(controller)

        # The hovered input when entering this View.
        self.first_inp = "q"

        # Initialize selected x-position.
        self.x = controller.get_hover_x()

        # Initialize selected y-position.
        self.y = controller.get_hover_y()
        
        # Map of input to functions.
        enter = self.graphics.ENTER_KEY
        self.controls = {
            # Pressing "q" will go back to the main menu.
            "q": lambda: Action("goto main menu view", []),

            # Repeat the last valid input.
            enter: self.repeat_last_valid_input
        }

        self.make_background_graphics()
    
    def repeat_last_valid_input(self):
        """
        Repeats the last valid input.

        Returns:
            Action: The Action to pass to the controller.
        """
        return self.parse(self.controller.get_last_inp())
    
    def make_background_graphics(self):
        """
        Makes the background graphics.
        """
        # Controls.
        text = [
            "_"*self.graphics.LENGTH,
            " wasd: Move | m: Select | q: Quit"
        ]
        controls = LongTextBox(Point(0, self.graphics.HEIGHT-3), text)
        self.uielements.append(controls)
