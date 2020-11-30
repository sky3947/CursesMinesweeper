"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point
from uielement import TextBox, LongTextBox

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        super().__init__(controller)
        grap = self.graphics

        banner = [
			r"  __ __ _ __  _ ___  __  _   _ ___ ___ ___ ___ ___  ",
			r" |  V  | |  \| | __/' _/| | | | __| __| _,\ __| _ \ ",
			r" | \_/ | | | ' | _|`._`.| 'V' | _|| _|| v_/ _|| v / ",
			r" !_! !_!_!_!\__!___!___/!_/ \_!___!___!_! !___!_!_\ "
		]
        start_point, _ = grap.center_just(4, banner[0])
        title = LongTextBox(start_point, banner)
        title.set_color(grap.BRIGHT)
        self.uielements.append(title)

        test_text = TextBox(Point(0, 10), "test textbox")
        test_text.set_color(grap.BRIGHT)
        self.uielements.append(test_text)

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
