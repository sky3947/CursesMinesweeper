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
        self.hover_x = controller.get_hover_x()

        # Initialize selected y-position.
        self.hover_y = controller.get_hover_y()

        # Get the minefield.
        self.minefield = controller.get_minefield()

        # Get the difficulty.
        self.difficulty = controller.get_difficulty()

        # Get the number of mines.
        self.num_mines = controller.get_num_mines()

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

        # UIElements for stats graphics.
        self.stats_graphics = {
            "pos_x_label": None,
            "pos_x": None,
            "pos_y_label": None,
            "pos_y": None,
            "mine_counter_label": None,
            "mine_counter": None
        }

        # Make background graphics.
        self.make_background_graphics()

        # Make minefield graphics.
        self.make_minefield_graphics()

        # Make help text.
        self.make_help()

        # Make stats graphics.
        self.make_stats_graphics()

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
            " g: Goto cell | G: Goto random cell | ijkl/IJKL: Move cam"
                .ljust(self.graphics.LENGTH, " "),
            " WASD: Move x10 | m: Open cell | n: Flag cell | q: Quit"
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
        height = self.difficulty.h
        length = self.difficulty.l
        centered_x = (self.graphics.LENGTH - length)//2
        centered_y = ((self.graphics.HEIGHT - 2) - height)//2
        centered = Point(
            0 if length > self.graphics.LENGTH else centered_x,
            0 if height > (self.graphics.HEIGHT - 2) else centered_y
        )

        self.minefield_ui = Minefield(centered, self.minefield)
        self.uielements.append(self.minefield_ui)

    def make_stats_graphics(self):
        """
        Makes the stats graphics.
        """
        self.stats_graphics["pos_x_label"] = TextBox()
        self.stats_graphics["pos_x_label"].set_color(self.graphics.DIM)

        self.stats_graphics["pos_x"] = TextBox()

        self.stats_graphics["pos_y_label"] = TextBox()
        self.stats_graphics["pos_y_label"].set_color(self.graphics.DIM)

        self.stats_graphics["pos_y"] = TextBox()

        self.stats_graphics["mine_counter_label"] = TextBox()
        self.stats_graphics["mine_counter_label"].set_color(self.graphics.DIM)

        self.stats_graphics["mine_counter"] = TextBox()

        self.update_stats_graphics()

        for element in self.stats_graphics.values():
            self.uielements.append(element)

    def update_stats_graphics(self):
        """
        Updates the stats graphics.
        """
        mines_left = str(self.num_mines - self.controller.get_num_flagged())
        pos_x = self.graphics.LENGTH - 1 - len(mines_left)
        pos_y = self.graphics.HEIGHT - 2

        mine_counter = self.stats_graphics["mine_counter"]
        mine_counter.set_location(Point(pos_x, pos_y))
        mine_counter.set_text(mines_left)
        pos_x -= 1

        mine_label = self.stats_graphics["mine_counter_label"]
        mine_label.set_location(Point(pos_x, pos_y))
        mine_label.set_text("*")
        pos_x -= 1

        view_y_text = str(self.hover_y)
        pos_x -= len(view_y_text)

        view_y = self.stats_graphics["pos_y"]
        view_y.set_location(Point(pos_x, pos_y))
        view_y.set_text(view_y_text)
        pos_x -= 1

        view_y_label = self.stats_graphics["pos_y_label"]
        view_y_label.set_location(Point(pos_x, pos_y))
        view_y_label.set_text("y")
        pos_x -= 1

        view_x_text = str(self.hover_x)
        pos_x -= len(view_x_text)

        view_x = self.stats_graphics["pos_x"]
        view_x.set_location(Point(pos_x, pos_y))
        view_x.set_text(view_x_text)
        pos_x -= 1

        view_x_label = self.stats_graphics["pos_x_label"]
        view_x_label.set_location(Point(pos_x, pos_y))
        view_x_label.set_text("x")
