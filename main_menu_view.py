"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point
from uielement import TextBox, LongTextBox, Button

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        super().__init__(controller)
        grap = self.graphics

        # The hovered input when entering this View.
        self.first_inp = "m"

        # Color options.
        color = grap.BRIGHT
        hovered_color = grap.HIGHLIGHT
        disabled_color = grap.DIM

        # MINESWEEPER logo.
        banner = [
			r"  __ __ _ __  _ ___  __  _   _ ___ ___ ___ ___ ___  ",
			r" |  V  | |  \| | __/' _/| | | | __| __| _,\ __| _ \ ",
			r" | \_/ | | | ' | _|`._`.| 'V' | _|| _|| v_/ _|| v / ",
			r" !_! !_!_!_!\__!___!___/!_/ \_!___!___!_! !___!_!_\ "
		]
        start_point, _ = grap.center_just(4, banner[0])
        title = LongTextBox(start_point, banner)
        title.set_color(color)
        self.uielements.append(title)

        # Delete save Button.
        text = "Delete Save"
        centered_point, _ = grap.center_just(15, text)
        delete_save_button = Button(centered_point, text)
        delete_save_button.set_color(color)
        delete_save_button.set_hovered(hovered_color)
        delete_save_button.set_disabled_color(disabled_color)
        self.uielements.append(delete_save_button)

        # Continue Button.
        continue_button = Button(Point(centered_point.x, 13), "Continue")
        continue_button.set_color(color)
        continue_button.set_hovered(hovered_color)
        continue_button.set_disabled_color(disabled_color)
        self.uielements.append(continue_button)

        # New game Button.
        new_game_button = Button(Point(centered_point.x, 14), "New Game")
        new_game_button.set_color(color)
        new_game_button.set_hovered(hovered_color)
        new_game_button.set_disabled_color(disabled_color)
        self.uielements.append(new_game_button)

        # Keep track of Buttons.
        self.selected = 0
        self.buttons = [continue_button, new_game_button, delete_save_button]

        # Make information box. (Explains what the hovered Button does.)
        self.info_box = TextBox(Point(1, 22))
        self.info_box.set_color(color)
        self.uielements.append(self.info_box)
        self.update_information_box_text()

        info_box_bar = TextBox(Point(0, 21), "_"*grap.LENGTH)
        info_box_bar.set_color(color)
        self.uielements.append(info_box_bar)

        # Make controls bar.
        text = [
            "_"*grap.LENGTH,
            " wasd: Move | m: Select | q: Quit"
        ]
        controls = LongTextBox(Point(0, grap.HEIGHT-3), text)
        controls.set_color(color)
        self.uielements.append(controls)

    def update_information_box_text(self):
        """
        Updates the information box.
        """
        message = ""
        if self.selected == 0:
            message = "Continue a saved game."
        elif self.selected == 1:
            message = "Start a new game."
        elif self.selected == 2:
            message = "Delete the saved game."
        self.info_box.set_text(message)

    def parse(self, inp):
        """
        Parses input and returns an Action. UI-related interactions are
        handled here.

        Args:
            inp (str): The user input.

        Returns:
            Action: The action to perform.
        """
        return Action("", [])
