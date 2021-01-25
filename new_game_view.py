"""
The new game View provides options to choose a customized minesweeper
difficulty.
"""

import math
from view import View
from utility import Point, Action, Direction
from uielement import UIType, TextBox, LongTextBox, Button, NumberField

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
        enter = self.graphics.ENTER_KEY
        self.controls = {
            # Pressing "q" will go back to the main menu.
            "q": lambda: Action("goto main menu view", []),

            # Movement keys.
            "w": lambda: self.move_cursor(Direction.U),
            "a": lambda: self.move_cursor(Direction.L),
            "s": lambda: self.move_cursor(Direction.D),
            "d": lambda: self.move_cursor(Direction.R),

            # Repeat the last valid input.
            enter: self.repeat_last_valid_input
        }

    def repeat_last_valid_input(self):
        """
        Repeats the last valid input.

        Returns:
            Action: The Action to pass to the controller.
        """
        return self.parse(self.controller.get_last_inp())

    def move_cursor(self, direction):
        """
        Changes the selected Button or NumberField to another in a
        Direction.

        Args:
            direction (Direction): The Direction to move the cursor.
        """
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

        uielements = self.buttons + self.numberfields

        # Button selection rules:
        # Custom <- Easy -> Medium
        # Button | NumberField <- NumberField -> NumberField
        if movement == 1:
            if self.selected is uielements[-1]:
                next_selected = self.numberfields[0]
            else:
                next_selected = uielements[uielements.index(self.selected)+1]
        else:
            if self.selected is uielements[0]:
                next_selected = self.buttons[-1]
            else:
                next_selected = uielements[uielements.index(self.selected)-1]

        # Update UIElement hovering.
        self.selected.set_hovered(False)
        next_selected.set_hovered(True)

        # Update changed settings.
        if self.selected is self.numberfields[0]:
            self.options["custom"]["length"] = self.selected.value
        elif self.selected is self.numberfields[1]:
            self.options["custom"]["height"] = self.selected.value
        elif self.selected is self.numberfields[2]:
            self.options["custom"]["density"] = self.selected.value

        # Update NumberField focus.
        if next_selected.get_type() is UIType.NumberField:
            self.set_focused_ui(next_selected)
        else:
            self.set_focused_ui(None)

        self.selected = next_selected
        self.update_information_box_text()

        self.controller.set_last_inp(last_input)

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
        else:
            message = "Customized settings."
            length = self.options["custom"]["length"]
            height = self.options["custom"]["height"]
            density = self.options["custom"]["density"]

        self.info_message_textbox.set_text(message)
        self.numberfields[0].set_value(length)
        self.numberfields[1].set_value(height)
        mines = math.floor(length * height * density / 100)
        num_mines_msg = "% ({} mines)".format(mines)
        self.numberfields[2].set_value(density)
        self.numberfields[2].set_postfix(num_mines_msg)

    def make_info_box(self):
        """
        Creates the info box to explain each difficulty.
        """
        # Color options.
        hovered_color = self.graphics.HIGHLIGHT
        inactive_color = self.graphics.DIM

        # Difficulty-specific message.
        self.info_message_textbox = TextBox(Point(1, 10))

        # NumberField for the length.
        info_length_numberfield = NumberField(Point(1, 13), 0, 1024)
        info_length_numberfield.set_hovered_color(hovered_color)
        info_length_numberfield.set_inactive_color(inactive_color)
        info_length_numberfield.set_prefix("Length: ")

        # NumberField for the height.
        info_height_numberfield = NumberField(Point(1, 14), 0, 1024)
        info_height_numberfield.set_hovered_color(hovered_color)
        info_height_numberfield.set_inactive_color(inactive_color)
        info_height_numberfield.set_prefix("Height: ")

        # NumberField for mine density.
        info_mines_numberfield = NumberField(Point(1, 15), 0, 100)
        info_mines_numberfield.set_hovered_color(hovered_color)
        info_mines_numberfield.set_inactive_color(inactive_color)
        info_mines_numberfield.set_prefix("Mine density: ")
        # Postfix is updated in self.update_information_box_text().

        self.uielements.append(TextBox(Point(1, 12), "Difficulty Statistics:"))
        self.uielements.append(self.info_message_textbox)
        self.uielements.append(info_length_numberfield)
        self.uielements.append(info_height_numberfield)
        self.uielements.append(info_mines_numberfield)

        # Keep track of NumberFields.
        self.numberfields = [info_length_numberfield, info_height_numberfield,
            info_mines_numberfield]

        self.update_information_box_text()

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
