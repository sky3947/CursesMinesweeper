"""
The game View is the main View for the game. It displays the minefield to the
user and lets them interact with it. Cuts corners with the minefield
manipulation. Should use controller to manipulate the model, but the server
doesn't exist, so the model is the same as in the controller.
"""

import random
from uielement import LongTextBox, Minefield, NumberField, TextBox
from utility import Action, Direction, Point, State
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

        # Get the number of flagged cells.
        self.num_flagged = controller.get_num_flagged()

        # Show the help text.
        self.show_help = False

        # Show the goto cell ui.
        self.show_goto = False

        # The state of the game.
        self.state = State.RUNNING

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

            "g": self.toggle_goto_graphics,
            "G": self.goto_random_cell,

            "n": self.toggle_flag,
            "m": self.open_cell,

            "z": self.center_camera,

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

        # The UIElement for winning.
        self.win_graphic = None

        # The UIElement for losing.
        self.lose_graphic = None

        # Make the win and lose graphics.
        self.make_endgame_graphics()

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
            if self.state == State.RUNNING:
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
        screen_length = self.graphics.LENGTH // 2
        screen_height = self.graphics.HEIGHT - 2

        if self.hover_x < self.window_x + 10:
            self.window_x = max(0, self.hover_x - 10)
        elif self.hover_x > self.window_x + (screen_length - 1) - 10:
            self.window_x = min(
                self.difficulty.l - screen_length,
                self.hover_x + 10 - screen_length + 1
            )

        if self.hover_y < self.window_y + 5:
            self.window_y = max(0, self.hover_y - 5)
        elif self.hover_y > self.window_y + (screen_height - 1) - 5:
            self.window_y = min(
                self.difficulty.h - screen_height,
                self.hover_y + 5 - screen_height + 1
            )

    def move_camera(self, direction, amount=1):
        """
        Moves the window_x and window_y in the given direction.

        Args:
            direction (Direction): The direction to move.
        """
        screen_length = self.graphics.LENGTH // 2
        screen_height = self.graphics.HEIGHT - 2

        if direction == Direction.U:
            self.window_y = max(0, self.window_y - amount)
            self.controller.set_last_inp("i")
        elif direction == Direction.L:
            self.window_x = max(0, self.window_x - amount)
            self.controller.set_last_inp("j")
        elif direction == Direction.D:
            self.window_y = min(self.difficulty.h - screen_height,
                                self.window_y + amount)
            self.controller.set_last_inp("k")
        elif direction == Direction.R:
            self.window_x = min(self.difficulty.l - screen_length,
                                self.window_x + amount)
            self.controller.set_last_inp("l")

        # Update minefield graphics.
        self.update_minefield_graphics()
        self.hide_help()
        self.hide_goto_graphics()

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

        centered_x = max(0, ((self.graphics.LENGTH // 2) - length) // 2)
        centered_y = max(0, ((self.graphics.HEIGHT - 2) - height)//2)
        centered = Point(centered_x, centered_y)

        self.minefield_ui = Minefield(centered, self.minefield)
        self.center_camera()
        self.update_minefield_graphics()

        self.uielements.append(self.minefield_ui)

    def update_minefield_graphics(self):
        """
        Updates the minefield graphics.
        """
        self.minefield_ui.set_hover_x(self.hover_x)
        self.minefield_ui.set_hover_y(self.hover_y)
        self.minefield_ui.set_window_x(self.window_x)
        self.minefield_ui.set_window_y(self.window_y)

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
        pos_x = self.graphics.LENGTH - 1
        pos_y = self.graphics.HEIGHT - 2

        mines_left = str(self.num_mines - self.num_flagged)
        pos_x = pos_x - len(mines_left)

        mine_counter = self.stats_graphics["mine_counter"]
        mine_counter.set_location(Point(pos_x, pos_y))
        mine_counter.set_text(mines_left)
        pos_x -= 1

        mine_label = self.stats_graphics["mine_counter_label"]
        mine_label.set_location(Point(pos_x, pos_y))
        mine_label.set_text(self.graphics.MINE_KEY)
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

    def make_endgame_graphics(self):
        """
        Makes the endgame graphics.
        """
        win_text = "You won!"
        lose_text = "You lost."

        pos_x = self.graphics.LENGTH - 1
        pos_y = self.graphics.HEIGHT - 1

        win_graphic = TextBox(Point(pos_x - len(win_text), pos_y), win_text)
        win_graphic.set_color(self.graphics.YELLOW)
        win_graphic.set_enabled(False)
        self.uielements.append(win_graphic)

        lose_graphic = TextBox(Point(pos_x - len(lose_text), pos_y), lose_text)
        lose_graphic.set_color(self.graphics.YELLOW)
        lose_graphic.set_enabled(False)
        self.uielements.append(lose_graphic)

        self.win_graphic = win_graphic
        self.lose_graphic = lose_graphic

    def goto_random_cell(self):
        """
        Goto to a random unopened cell.
        """
        pos_x = random.randint(0, self.difficulty.l - 1)
        pos_y = random.randint(0, self.difficulty.h - 1)
        tries = 50

        # Try to find an unopened cell.
        while tries > 0:
            if (not self.minefield[pos_y][pos_x].is_opened()
                and not self.minefield[pos_y][pos_x].is_flagged()):
                self.hover_x = pos_x
                self.hover_y = pos_y
                self.controller.set_hover_x(self.hover_x)
                self.controller.set_hover_y(self.hover_y)
                self.center_camera()
                self.update_minefield_graphics()
                self.update_stats_graphics()
                self.hide_help()
                self.hide_goto_graphics()
                return

            pos_x = random.randint(0, self.difficulty.l - 1)
            pos_y = random.randint(0, self.difficulty.h - 1)
            tries -= 1

        # If none found yet, pick from a list of unopened cells.
        unopened_positions = []
        for y in range(self.difficulty.h):
            for x in range(self.difficulty.l):
                if (not self.minefield[y][x].is_opened()
                    and not self.minefield[y][x].is_flagged()):
                    unopened_positions.append((x, y))

        if len(unopened_positions) == 0:
            return

        pos_x, pos_y = random.choice(unopened_positions)
        self.hover_x = pos_x
        self.hover_y = pos_y
        self.controller.set_hover_x(self.hover_x)
        self.controller.set_hover_y(self.hover_y)
        self.center_camera()
        self.update_minefield_graphics()
        self.update_stats_graphics()
        self.hide_help()

    def toggle_flag(self):
        """
        Places or removes a flag at the hovered cell.
        """
        if self.state == State.WON or self.state == State.LOST:
            return

        hovered_cell = self.minefield[self.hover_y][self.hover_x]

        # Flagging unopened cells.
        if not hovered_cell.is_opened():
            if hovered_cell.is_flagged():
                self.num_flagged -= 1
                hovered_cell.set_flagged(False)
            else:
                self.num_flagged += 1
                hovered_cell.set_flagged(True)
            self.update_stats_graphics()
            return

        cell_mound = []

        # Quick flag adjacent cells.
        xbound = (max(0, self.hover_x - 1),
                    min(self.difficulty.l - 1, self.hover_x + 1) + 1)
        ybound = (max(0, self.hover_y - 1),
                    min(self.difficulty.h - 1, self.hover_y + 1) + 1)
        temp_mound = []
        unopened = 0
        for x_near in range(*xbound):
            for y_near in range(*ybound):
                cell = self.minefield[y_near][x_near]
                if not cell.is_opened():
                    unopened += 1
                    if not cell.is_flagged():
                        temp_mound.append(Point(x_near, y_near))

        if unopened == hovered_cell.get_number():
            cell_mound.extend(temp_mound)

        # Flag cells.
        for point in cell_mound:
            if not self.minefield[point.y][point.x].is_flagged():
                self.num_flagged += 1
                self.minefield[point.y][point.x].set_flagged(True)

        self.update_stats_graphics()

    def open_cell(self):
        """
        Opens the hovered cell.
        """
        if self.state == State.WON or self.state == State.LOST:
            return

        hovered_cell = self.minefield[self.hover_y][self.hover_x]
        if hovered_cell.is_flagged():
            return

        cell_mound = []
        mound_position = 0

        # Quick open adjacent cells.
        if hovered_cell.is_opened():
            xbound = (max(0, self.hover_x - 1),
                      min(self.difficulty.l - 1, self.hover_x + 1) + 1)
            ybound = (max(0, self.hover_y - 1),
                      min(self.difficulty.h - 1, self.hover_y + 1) + 1)
            temp_mound = []
            flagged_count = 0
            for x_near in range(*xbound):
                for y_near in range(*ybound):
                    cell = self.minefield[y_near][x_near]
                    if cell.is_flagged():
                        flagged_count += 1
                    if (not cell.is_opened()
                        and not cell.is_flagged()):
                        temp_mound.append(Point(x_near, y_near))

            if flagged_count == hovered_cell.get_number():
                cell_mound.extend(temp_mound)

        cell_mound.append(Point(self.hover_x, self.hover_y))

        # Open cells.
        while mound_position < len(cell_mound):
            point = cell_mound[mound_position]

            if not self.minefield[point.y][point.x].is_opened():
                self.minefield[point.y][point.x].open()

                # Check for loss condition.
                if self.minefield[point.y][point.x].is_mine():
                    self.state = State.LOST
                    self.minefield_ui.set_lost(True)
                    self.lose_graphic.set_enabled(True)
                    self.controller.delete_saved_game()
                    return

                # Add neighbors to the mound if there are no mines around.
                if self.minefield[point.y][point.x].get_number() == 0:
                    xbound = (max(0, point.x - 1),
                              min(self.difficulty.l - 1, point.x + 1) + 1)
                    ybound = (max(0, point.y - 1),
                              min(self.difficulty.h - 1, point.y + 1) + 1)
                    for x_near in range(*xbound):
                        for y_near in range(*ybound):
                            cell = self.minefield[y_near][x_near]
                            if (not cell.is_opened()
                                and not cell.is_flagged()):
                                cell_mound.append(Point(x_near, y_near))

            mound_position += 1

        # Check for win condition.
        won = True
        for row in self.minefield:
            for point in row:
                if not point.is_opened() and not point.is_mine():
                    won = False
                    break
            if not won:
                break

        if won:
            self.state = State.WON
            self.win_graphic.set_enabled(True)
            self.controller.delete_saved_game()
