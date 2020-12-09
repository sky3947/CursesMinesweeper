"""
The new game View provides options to choose a customized minesweeper
difficulty.
"""

import math
from view import View
from utility import Point, Action
from uielement import TextBox, LongTextBox, Button

class NewGameView(View):
    """
    Draws UIElements for customizing a new minefield.
    """
    def __init__(self, controller):
        """
        Instantiates a NewGameView and returns it.

        Args:
            controller (Controller): The controller to pass user input.
        """
        super().__init__(controller)

        # The hovered input when entering this View.
        self.first_inp = "s"

        # Initialize selected variable.
        self.selected = None

        # Make background graphics.
        self.make_background_graphics()

        # Make Buttons.
        self.make_buttons()

        # Minefield options.
        self.options = {
            "easy": {
                "length": 10,
                "height": 10,
                "density": 10
            },
            "medium": {
                "length": 30,
                "height": 20,
                "density": 15
            },
            "hard": {
                "length": 60,
                "height": 30,
                "density": 20
            },
            "custom": {
                "length": 10,
                "height": 10,
                "density": 10
            }
        }

        # Make the information box. This explains each Button.
        self.make_info_box()

        # Map of input to functions.
        self.controls = {
            # Pressing "q" will go back to the main menu.
            "q": lambda: Action("goto main menu view", [])
        }

    def update_information_box_text(self):
        """
        Updates the information box.
        """
        message = "Unrecognized difficulty."
        length = 10
        height = 10
        density = 10
        if self.selected is self.buttons[0]:
            message = "Small field and easy mine density."
            length = self.options["easy"]["length"]
            height = self.options["easy"]["height"]
            density = self.options["easy"]["density"]
        elif self.selected is self.buttons[1]:
            message = "Increased field area and mine density."
            length = self.options["medium"]["length"]
            height = self.options["medium"]["height"]
            density = self.options["medium"]["density"]
        elif self.selected is self.buttons[2]:
            message = "Challenging field and mine density."
            length = self.options["hard"]["length"]
            height = self.options["hard"]["height"]
            density = self.options["hard"]["density"]
        elif self.selected is self.buttons[3]:
            message = "Customized settings."
            length = self.options["custom"]["length"]
            height = self.options["custom"]["height"]
            density = self.options["custom"]["density"]

        self.info_message_textbox.set_text(message)
        self.info_length_textbox.set_text("Length: " + str(length))
        self.info_height_textbox.set_text("Height: " + str(height))
        mines = math.floor(length * height * density / 100)
        mines_msg = "Mine density: {}% ({} mines)".format(density, mines)
        self.info_mines_textbox.set_text(mines_msg)

    def make_info_box(self):
        """
        Creates the info box to explain each difficulty.
        """
        self.info_message_textbox = TextBox(Point(1, 10))
        self.info_length_textbox = TextBox(Point(1, 13))
        self.info_height_textbox = TextBox(Point(1, 14))
        self.info_mines_textbox = TextBox(Point(1, 15))
        self.update_information_box_text()

        self.uielements.append(TextBox(Point(1, 12), "Difficulty Statistics:"))
        self.uielements.append(self.info_message_textbox)
        self.uielements.append(self.info_length_textbox)
        self.uielements.append(self.info_height_textbox)
        self.uielements.append(self.info_mines_textbox)


    def make_buttons(self):
        """
        Initializes and adds Buttons.
        """
        # Color options.
        hovered_color = self.graphics.HIGHLIGHT
        disabled_color = self.graphics.DIM

        # Easy Button.
        easy_button = Button(Point(1, 4), "Easy")
        easy_button.set_hovered_color(hovered_color)
        easy_button.set_inactive_color(disabled_color)
        self.uielements.append(easy_button)

        # Medium Button.
        medium_button = Button(Point(1, 5), "Medium")
        medium_button.set_hovered_color(hovered_color)
        medium_button.set_inactive_color(disabled_color)
        self.uielements.append(medium_button)

        # Hard Button.
        hard_button = Button(Point(1, 6), "Hard")
        hard_button.set_hovered_color(hovered_color)
        hard_button.set_inactive_color(disabled_color)
        self.uielements.append(hard_button)

        # Custom Button.
        custom_button = Button(Point(1, 7), "Custom")
        custom_button.set_hovered_color(hovered_color)
        custom_button.set_inactive_color(disabled_color)
        self.uielements.append(custom_button)

        # Keep track of Buttons.
        self.buttons = [easy_button, medium_button, hard_button, custom_button]

        self.selected = easy_button
        easy_button.set_hovered(True)

    def make_background_graphics(self):
        """
        Draws static background graphics.
        """
        # Title.
        centered = self.graphics.center_just(1, "CHOOSE  DIFFICULTY")
        title = TextBox(*centered)
        self.uielements.append(title)

        # Bars.
        bar_a = TextBox(Point(0, 2), "_"*self.graphics.LENGTH)
        self.uielements.append(bar_a)

        bar_b = TextBox(Point(0, 8), "_"*self.graphics.LENGTH)
        self.uielements.append(bar_b)

        # Controls.
        text = [
            "_"*self.graphics.LENGTH,
            " wasd: Move | m: Select | q: Quit"
        ]
        controls = LongTextBox(Point(0, self.graphics.HEIGHT-3), text)
        self.uielements.append(controls)
