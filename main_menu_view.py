"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point, Direction
from uielement import TextBox, LongTextBox, Button

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        super().__init__(controller)

        # The hovered input when entering this View.
        self.first_inp = "m"

        # Make the MINESWEEPER logo.
        self.make_banner()

        # Make Buttons
        self.make_buttons()

        # Make the information box. This explains each Button.
        self.make_info_box()

        # Make controls bar.
        self.make_controls_bar()

        # Map of input to functions.
        self.controls = {
            "q": lambda: Action("quit", []),
            "w": lambda: self.move_cursor(Direction.U),
            "a": lambda: self.move_cursor(Direction.L),
            "s": lambda: self.move_cursor(Direction.D),
            "d": lambda: self.move_cursor(Direction.R)
        }

    def move_cursor(self, direction):
        movement = 1
        last_input = ""
        if direction is Direction.U:
            movement = -1
            last_input = "w"
        elif direction is Direction.L:
            movement = -1
            last_input = "a"
        elif direction is Direction.D:
            last_input = "s"
        elif direction is Direction.R:
            last_input = "d"

        has_enabled_buttons = any(but.is_enabled() for but in self.buttons)
        if has_enabled_buttons:
            # Find the next enabled Button.
            cur_but_ind = self.buttons.index(self.selected)
            next_but_ind = (cur_but_ind + movement) % len(self.buttons)
            while not self.buttons[next_but_ind].is_enabled:
                next_but_ind = (next_but_ind + movement) % len(self.buttons)
            next_enabled_button = self.buttons[next_but_ind]

            self.selected.set_hovered(False)
            next_enabled_button.set_hovered(True)
            self.selected = next_enabled_button
        else:
            return Action("", [])

        return Action("set last input", [last_input])

    def make_controls_bar(self):
        """
        Creates the controls bar to display controls.
        """
        # Color options.
        color = self.graphics.BRIGHT

        text = [
            "_"*self.graphics.LENGTH,
            " wasd: Move | m: Select | q: Quit"
        ]
        controls = LongTextBox(Point(0, self.graphics.HEIGHT-3), text)
        controls.set_color(color)
        self.uielements.append(controls)

    def update_information_box_text(self):
        """
        Updates the information box.
        """
        message = ""
        if self.selected is self.buttons[0]:
            message = "Continue a saved game."
        elif self.selected is self.buttons[1]:
            message = "Start a new game."
        elif self.selected is self.buttons[2]:
            message = "Delete the saved game."
        self.info_box.set_text(message)

    def make_info_box(self):
        """
        Creates the info box to explain each Button.
        """
        # Color options.
        color = self.graphics.BRIGHT

        self.info_box = TextBox(Point(1, 22))
        self.info_box.set_color(color)
        self.uielements.append(self.info_box)
        self.update_information_box_text()

        info_box_bar = TextBox(Point(0, 21), "_"*self.graphics.LENGTH)
        info_box_bar.set_color(color)
        self.uielements.append(info_box_bar)

    def make_buttons(self):
        """
        Initializes and adds Buttons.
        """
        # Color options.
        color = self.graphics.BRIGHT
        hovered_color = self.graphics.HIGHLIGHT
        disabled_color = self.graphics.DIM

        # Delete save Button.
        text = "Delete Save"
        centered_point, _ = self.graphics.center_just(15, text)
        delete_save_button = Button(centered_point, text)
        delete_save_button.set_color(color)
        delete_save_button.set_hovered_color(hovered_color)
        delete_save_button.set_disabled_color(disabled_color)
        self.uielements.append(delete_save_button)

        # Continue Button.
        continue_button = Button(Point(centered_point.x, 13), "Continue")
        continue_button.set_color(color)
        continue_button.set_hovered_color(hovered_color)
        continue_button.set_disabled_color(disabled_color)
        self.uielements.append(continue_button)

        # New game Button.
        new_game_button = Button(Point(centered_point.x, 14), "New Game")
        new_game_button.set_color(color)
        new_game_button.set_hovered_color(hovered_color)
        new_game_button.set_disabled_color(disabled_color)
        self.uielements.append(new_game_button)

        # Keep track of Buttons.
        self.buttons = [continue_button, new_game_button, delete_save_button]

        self.selected = continue_button
        if self.controller.has_saved_game():
            continue_button.set_hovered(True)
        else:
            self.selected = new_game_button
            new_game_button.set_hovered(True)
            continue_button.set_enabled(False)
            delete_save_button.set_enabled(False)

    def make_banner(self):
        """
        Creates the MINESWEEPER banner.
        """
        # Color options.
        color = self.graphics.BRIGHT

        banner = [
			R"  __ __ _ __  _ ___  __  _   _ ___ ___ ___ ___ ___  ",
			R" |  V  | |  \| | __/' _/| | | | __| __| _,\ __| _ \ ",
			R" | \_/ | | | ' | _|`._`.| 'V' | _|| _|| v_/ _|| v / ",
			R" !_! !_!_!_!\__!___!___/!_/ \_!___!___!_! !___!_!_\ "
		]
        start_point, _ = self.graphics.center_just(4, banner[0])
        title = LongTextBox(start_point, banner)
        title.set_color(color)
        self.uielements.append(title)

    def parse(self, inp):
        """
        Parses input and returns an Action. UI-related interactions are
        handled here.

        Args:
            inp (str): The user input.

        Returns:
            Action: The action to perform.
        """
        inp = inp.lower()
        fun = self.controls.get(inp, lambda: Action("", []))
        return fun()
