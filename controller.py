"""
This class is the controller for the Minesweeper program.
"""

from graphics import Graphics
from utility import Flow
from main_menu_view import MainMenuView
from views.new_game_view import NewGameView
from views.generating_view import GeneratingView
from views.continue_game_view import ContinueGameView

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

        # The last valid input by the user.
        self.last_inp = ""

        # Map of actions to functions.
        gnegav_fun = lambda: self.action_change_view(NewGameView(self))
        gmamev_fun = lambda: self.action_change_view(MainMenuView(self))
        ggev_fun = lambda: self.action_change_view(GeneratingView(self))
        gcogav_fun = lambda: self.action_change_view(ContinueGameView(self))
        ggav_fun = lambda: Flow.PASS

        self.actions = {
            "quit": self.action_quit,
            "goto new game view": gnegav_fun,
            "goto main menu view": gmamev_fun,
            "goto generating view": ggev_fun,
            "goto continue game view": gcogav_fun,
            "goto game view": ggav_fun
        }

    def load_minefield(self):
        """
        Tells the model to load the minefield from a save file.
        """
        self.model.load_minefield()

    def calculate_mines(self, option):
        """
        Tells the model to calculate the number of mines in a minefield.

        Args:
            option (Option): An Option containing length, height, and
            mine density.

        Returns:
            int: The number of mines generated.
        """
        return self.model.calculate_mines(option)

    def generate_minefield(self):
        """
        Tells the model to generate a new minefield.
        """
        self.model.generate_minefield()

    def reset_gen_progress(self):
        """
        Tells the model to reset the gen_progress.
        """
        self.model.reset_gen_progress()

    def get_gen_progress(self):
        """
        Gets the minefield generation progress percentage from the
        model.

        Returns:
            int: The progress percentage.
        """
        return self.model.get_gen_progress()

    def get_difficulty(self):
        """
        Gets the difficulty of the minefield to be generated from the
        model.

        Returns:
            Option: The Option containing length, height, and density
            information.
        """
        return self.model.difficulty

    def set_difficulty(self, option):
        """
        Tells the model to set the difficulty of the minefield to
        generate.

        Args:
            option (Option): The Option containing length, height, and
            density information.
        """
        self.model.set_difficulty(option)

    def has_saved_game(self):
        """
        Asks the model if there's a saved game.

        Returns:
            bool: True if there's a saved game, False otherwise.
        """
        return self.model.has_saved_game()

    def delete_saved_game(self):
        """
        Asks the model to delete the saved game.
        """
        self.model.delete_saved_game()

    def set_last_inp(self, inp):
        """
        Sets the last valid input.

        Args:
            inp (str): The last valid input.
        """
        self.last_inp = inp

    def get_last_inp(self):
        """
        Gets the last valid input.

        Returns:
            str: The last valid input.
        """
        return self.last_inp

    def start(self):
        """
        Readies Controller to start the game loop.
        """
        self.change_view(MainMenuView(self))

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
        self.set_last_inp(view.get_first_input())

    def set_custom_field_options(self, values):
        """
        Tells the model to set the length, height, and density values
        for generating a custom minefield.

        Args:
            values (list): An array [length, height, density].
        """
        self.model.set_custom_field_options(values)

    def get_minefield_options(self):
        """
        Gets the minefield generation options from the model.

        Returns:
            dict: The table of difficulty options.
        """
        return self.model.options

    def act(self, action):
        """
        Responds to input from a View.

        Args:
            action (Action): The Action to perform.

        Returns:
            Flow: The control flow to pass to the View.
        """
        fun = self.actions.get(action.primary, lambda: Flow.PASS)
        try:
            return fun(*action.secondary)
        except TypeError:
            return Flow.PASS

    #
    # Actions functions. The Flow is sent back to the View.
    #

    @staticmethod
    def action_quit():
        """
        Sends the control flow to quit the game.

        Returns:
            Flow: Send Flow.BREAK.
        """
        return Flow.BREAK

    def action_change_view(self, view):
        """
        Sends the control flow to change the View.

        Args:
            view (View): The new View.

        Returns:
            Flow: Send Flow.RETURN.
        """
        self.change_view(view)
        return Flow.RETURN
