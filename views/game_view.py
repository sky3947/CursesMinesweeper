"""
The game View is the main View for the game. It displays the minefield to the
user and lets them interact with it.
"""

from uielement import LongTextBox, Minefield, TextBox
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

        # Get the minefield.
        self.minefield = controller.get_minefield()

        # Show the help text.
        self.show_help = False

        # Map of input to functions.
        enter = self.graphics.ENTER_KEY
        self.controls = {
            # Pressing "q" will go back to the main menu.
            "q": lambda: Action("goto main menu view", []),
            "?": self.toggle_help,

            # Repeat the last valid input.
            enter: self.repeat_last_valid_input
        }

        # Make background graphics.
        self.make_background_graphics()

        # Make minefield graphics.
        self.make_minefield_graphics()

        # Make help text.
        self.make_help()
    
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
            " wasd: Move | ?: Controls"
        ]
        controls = LongTextBox(Point(0, self.graphics.HEIGHT-3), text)
        self.uielements.append(controls)
    
    def make_help(self):
        """
        Draws the help text to display extra controls.
        """
        # Help text.
        text = [
            " g: Goto cell | G: Goto random cell"
                .ljust(self.graphics.LENGTH, " "),
            " WASD: Skip | m: Open cell | n: Flag cell | q: Quit"
                .ljust(self.graphics.LENGTH, "_")
        ]
        first_line, second_line = text
        help_text_l1 = TextBox(Point(0, self.graphics.HEIGHT-4), first_line)
        help_text_l2 = TextBox(Point(0, self.graphics.HEIGHT-3), second_line)

        help_text_l1.color = self.graphics.BRIGHT
        help_text_l2.color = self.graphics.BRIGHT | self.graphics.UNDERLINE

        help_text_l1.set_enabled(False)
        help_text_l2.set_enabled(False)

        self.help_text_list = [help_text_l1, help_text_l2]
        self.uielements.append(help_text_l1)
        self.uielements.append(help_text_l2)

    def toggle_help(self):
        """
        Toggles the help text.
        """
        self.show_help = not self.show_help
        if self.show_help:
            for help_text in self.help_text_list:
                help_text.set_enabled(True)
        else:
            for help_text in self.help_text_list:
                help_text.set_enabled(False)

    def make_minefield_graphics(self):
        """
        Makes the minefield graphics.
        """
        self.minefield_ui = Minefield(Point(0, 0), self.minefield)
        self.uielements.append(self.minefield_ui)
