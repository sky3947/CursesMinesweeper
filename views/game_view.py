"""
The game View is the main View for the game. It displays the minefield to the
user and lets them interact with it.
"""

from uielement import LongTextBox, Minefield, NumberField, TextBox
from utility import Action, Direction, Point
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
        self.first_inp = "d"

        # Initialize selected x-position.
        self.hover_x = controller.get_hover_x()

        # Initialize selected y-position.
        self.hover_y = controller.get_hover_y()

        # The x-position of the window to start drawing the field.
        self.window_x = self.hover_x

        # The y-position of the window to start drawing the field.
        self.window_y = self.hover_y

        # Get the minefield.
        self.minefield = controller.get_minefield()

        # Get the difficulty.
        self.difficulty = controller.get_difficulty()

        # Get the number of mines.
        self.num_mines = controller.get_num_mines()

        # Show the help text.
        self.show_help = False

        # Show the goto cell ui.
        self.show_goto = False

        # Map of input to functions.
        enter = self.graphics.ENTER_KEY
        self.controls = {
            # Pressing "q" will go back to the main menu or hide the goto menu.
            "q": self.quit,
            "?": self.toggle_help,

            # Gameplay controls.
            "w": lambda: self.move(Direction.U),
            "a": lambda: self.move(Direction.L),
            "s": lambda: self.move(Direction.D),
            "d": lambda: self.move(Direction.R),

            "W": lambda: self.move(Direction.U, 10),
            "A": lambda: self.move(Direction.L, 10),
            "S": lambda: self.move(Direction.D, 10),
            "D": lambda: self.move(Direction.R, 10),

            "i": lambda: self.move_camera(Direction.U),
            "j": lambda: self.move_camera(Direction.L),
            "k": lambda: self.move_camera(Direction.D),
            "l": lambda: self.move_camera(Direction.R),

            "I": lambda: self.move_camera(Direction.U, 10),
            "J": lambda: self.move_camera(Direction.L, 10),
            "K": lambda: self.move_camera(Direction.D, 10),
            "L": lambda: self.move_camera(Direction.R, 10),

            "g": lambda: self.toggle_goto_graphics(),

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

        # Background UIElements for goto graphics.
        self.goto_graphics = []

        # UIElements for goto NumberFields.
        self.goto_number_fields = {
            "pos_x": None,
            "pos_y": None
        }

        # Make goto graphics.
        self.make_goto_graphics()

    def repeat_last_valid_input(self):
        """
        Repeats the last valid input.

        Returns:
            Action: The Action to pass to the controller.
        """
        return self.parse(self.controller.get_last_inp())

    def quit(self):
        """
        Quits the game or hides the goto menu.
        """
        if self.show_goto:
            self.hide_goto_graphics()
        else:
            # Draw decorative text.
            decorative_text = self.graphics.center_just(9, "             ")
            self.graphics.draw(*decorative_text)
            decorative_text = self.graphics.center_just(11, "             ")
            self.graphics.draw(*decorative_text)
            saving_text = self.graphics.center_just(10, "  Saving...  ")
            self.graphics.draw(*saving_text)
            self.graphics.refresh()

            # Save the game.
            self.controller.save_minefield()

            # Go back to the main menu.
            return Action("goto main menu view", [])

    def move(self, direction, amount=1):
        """
        Moves hover_x and hover_y in the given direction. If goto window is
        visible, instead change NumberField focus.

        Args:
            direction (Direction): The direction to move.
        """
        if self.show_goto:
            if self.focused_ui is self.goto_number_fields["pos_x"]:
                self.set_focused_ui(self.goto_number_fields["pos_y"])
                self.goto_number_fields["pos_x"].set_hovered(False)
                self.goto_number_fields["pos_y"].set_hovered(True)
            else:
                self.set_focused_ui(self.goto_number_fields["pos_x"])
                self.goto_number_fields["pos_x"].set_hovered(True)
                self.goto_number_fields["pos_y"].set_hovered(False)
        else:
            if direction == Direction.U:
                self.hover_y = max(0, self.hover_y - amount)
                self.controller.set_last_inp("w")
            elif direction == Direction.L:
                self.hover_x = max(0, self.hover_x - amount)
                self.controller.set_last_inp("a")
            elif direction == Direction.D:
                self.hover_y = min(self.difficulty.h - 1, self.hover_y + amount)
                self.controller.set_last_inp("s")
            elif direction == Direction.R:
                self.hover_x = min(self.difficulty.l - 1, self.hover_x + amount)
                self.controller.set_last_inp("d")

            # Update minefield graphics.
            self.controller.set_hover_x(self.hover_x)
            self.controller.set_hover_y(self.hover_y)
            self.center_camera()
            self.update_minefield_graphics()
            self.update_stats_graphics()
            self.hide_help()

    def center_camera(self):
        """
        Centers the camera based on hover_x and hover_y.
        """
        if self.hover_x < self.window_x + 10:
            self.window_x = max(0, self.hover_x - 10)
        elif self.hover_x > self.window_x + (self.graphics.LENGTH - 1) - 10:
            self.window_x = min(
                self.difficulty.l - self.graphics.LENGTH,
                self.hover_x + 10 - self.graphics.LENGTH + 1
            )

        if self.hover_y < self.window_y + 5:
            self.window_y = max(0, self.hover_y - 5)
        elif self.hover_y > self.window_y + (self.graphics.HEIGHT - 3) - 5:
            self.window_y = min(
                self.difficulty.h - (self.graphics.HEIGHT - 2),
                self.hover_y + 5 - (self.graphics.HEIGHT - 2) + 1
            )

    def move_camera(self, direction, amount=1):
        """
        Moves the window_x and window_y in the given direction.

        Args:
            direction (Direction): The direction to move.
        """
        if direction == Direction.U:
            self.window_y = max(0, self.window_y - amount)
            self.controller.set_last_inp("i")
        elif direction == Direction.L:
            self.window_x = max(0, self.window_x - amount)
            self.controller.set_last_inp("j")
        elif direction == Direction.D:
            self.window_y = min(self.difficulty.h - (self.graphics.HEIGHT - 2),
                                self.window_y + amount)
            self.controller.set_last_inp("k")
        elif direction == Direction.R:
            self.window_x = min(self.difficulty.l - self.graphics.LENGTH,
                                self.window_x + amount)
            self.controller.set_last_inp("l")

        # Update minefield graphics.
        self.update_minefield_graphics()
        self.hide_help()

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

    def hide_help(self):
        """
        Hides the help text.
        """
        self.show_help = False
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
        self.minefield_ui.set_hover_x(self.hover_x)
        self.minefield_ui.set_hover_y(self.hover_y)
        self.minefield_ui.set_window_x(self.window_x)
        self.minefield_ui.set_window_y(self.window_y)
        self.center_camera()
        self.update_minefield_graphics()

        self.uielements.append(self.minefield_ui)

    def update_minefield_graphics(self):
        """
        Updates the minefield graphics.
        """
        self.minefield_ui.hover_x = self.hover_x
        self.minefield_ui.hover_y = self.hover_y
        self.minefield_ui.window_x = self.window_x
        self.minefield_ui.window_y = self.window_y

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

    def make_goto_graphics(self):
        """
        Makes the goto graphics.
        """
        # Color options.
        hovered_color = self.graphics.HIGHLIGHT

        # Background.
        background_text = [
            "----------------",
            "      Goto      ",
            "                ",
            "     x          ",
            "     y          ",
            "----------------"
        ]

        # UIElements for background graphics.
        start_x = (self.graphics.LENGTH - len(background_text[0]))//2
        start_y = 5
        for index in range(len(background_text)):
            background_graphic = TextBox(Point(start_x, start_y + index),
                                         background_text[index])
            background_graphic.set_enabled(False)
            self.uielements.append(background_graphic)
            self.goto_graphics.append(background_graphic)

        # NumberFields.
        field_pos_x = NumberField(Point(start_x + 7, 8),
                                  0, self.difficulty.l - 1)
        field_pos_x.set_minimum(0)
        field_pos_x.set_hovered_color(hovered_color)
        field_pos_x.set_enabled(False)
        self.uielements.append(field_pos_x)
        self.goto_number_fields["pos_x"] = field_pos_x

        field_pos_y = NumberField(Point(start_x + 7, 9),
                                  0, self.difficulty.h - 1)
        field_pos_y.set_minimum(0)
        field_pos_y.set_hovered_color(hovered_color)
        field_pos_y.set_enabled(False)
        self.uielements.append(field_pos_y)
        self.goto_number_fields["pos_y"] = field_pos_y

    def show_goto_graphics(self):
        """
        Shows the goto graphics.
        """
        self.show_goto = True
        for background in self.goto_graphics:
            background.set_enabled(True)
        for field in self.goto_number_fields.values():
            field.set_enabled(True)

        # Update initial values.
        self.goto_number_fields["pos_x"].set_value(self.hover_x)
        self.goto_number_fields["pos_y"].set_value(self.hover_y)

        self.set_focused_ui(self.goto_number_fields["pos_x"])
        self.goto_number_fields["pos_x"].set_hovered(True)

    def hide_goto_graphics(self):
        """
        Hides the goto graphics.
        """
        self.show_goto = False
        for background in self.goto_graphics:
            background.set_enabled(False)
        for field in self.goto_number_fields.values():
            field.set_enabled(False)
            field.set_hovered(False)

        self.set_focused_ui(None)

    def toggle_goto_graphics(self):
        """
        Toggles the goto graphics.
        """
        if self.show_goto:
            goto_x = self.goto_number_fields["pos_x"].value
            goto_y = self.goto_number_fields["pos_y"].value
            self.hover_x = goto_x
            self.hover_y = goto_y

            self.controller.set_hover_x(self.hover_x)
            self.controller.set_hover_y(self.hover_y)
            self.center_camera()
            self.update_minefield_graphics()
            self.update_stats_graphics()
            self.hide_help()
            self.hide_goto_graphics()
        else:
            self.show_goto_graphics()
