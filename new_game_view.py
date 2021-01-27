"""
The new game View provides options to choose a customized minesweeper
difficulty.
"""

from view import View
from utility import Point, Action, Direction, Option
from uielement import UIType, TextBox, LongTextBox, Button, NumberField, Popup

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

        # Make the information box. This explains each Button.
        self.make_info_box()

        # Initializes popup.
        self.make_popup()

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
            enter: self.repeat_last_valid_input,

            # Click the selected UIElement.
            "m": self.click
        }

    def click(self):
        """
        Clicks the selected UIElement.

        Args:
            params (list): The list of parameters to pass to the
                UIElement.

        Returns:
            Action: The Action to pass to the controller.
        """
        return self.selected.click()

    def make_popup(self):
        """
        Initializes a reusable Popup.
        """
        self.popup = Popup(Point(0, 2), self, "", "")
        self.popup.set_highlight_color(self.graphics.HIGHLIGHT)
        self.popup.set_secondary_color(self.graphics.DIM)
        title_color = self.graphics.BRIGHT | self.graphics.UNDERLINE
        self.popup.set_title_color(title_color)
        self.popup.set_enabled(False)
        self.popup.set_action(self.custom_field_popup_action)
        self.uielements.append(self.popup)

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
        # Hard <- Custom <- Easy -> Medium -> Hard -> Custom -> NumberField
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
        if self.selected.get_type() is UIType.NumberField:
            self.selected.fix_bounds()
            values = [numberfield.value for numberfield in self.numberfields]
            self.controller.set_custom_field_options(Option(*values))

        # Update NumberField focus.
        condition = next_selected.get_type() is UIType.NumberField
        next_focus = next_selected if condition else None
        self.set_focused_ui(next_focus)

        self.selected = next_selected
        self.update_information_box_text()

        self.controller.set_last_inp(last_input)

    def update_information_box_text(self):
        """
        Updates the information box.
        """
        # Get the minefield options from the model.
        options = self.controller.get_minefield_options()

        # Default values.
        message = "Unrecognized difficulty."
        length = 10
        height = 10
        density = 10
        option = Option(length, height, density)

        # Change default values based on button hovering.
        if self.selected is self.buttons[0]:
            message = "Small field and easy mine density."
            option = options["easy"]
            length = option.l
            height = option.h
            density = option.d
        elif self.selected is self.buttons[1]:
            message = "Increased field area and mine density."
            option = options["medium"]
            length = option.l
            height = option.h
            density = option.d
        elif self.selected is self.buttons[2]:
            message = "Challenging field and mine density."
            option = options["hard"]
            length = option.l
            height = option.h
            density = option.d
        elif (self.selected is self.buttons[3] or
                self.selected.get_type() is UIType.NumberField):
            message = "Customized settings."
            option = options["custom"]
            length = option.l
            height = option.h
            density = option.d

        # Set values.
        self.info_message_textbox.set_text(message)
        self.numberfields[0].set_value(length)
        self.numberfields[1].set_value(height)
        mines = self.controller.calculate_mines(option)
        plural = "" if mines == 1 else "s"
        num_mines_msg = "% ({} mine{})".format(mines, plural)
        self.numberfields[2].set_value(density)
        self.numberfields[2].set_postfix(num_mines_msg)

    def make_info_box(self):
        """
        Creates the info box to explain each difficulty.
        """
        # Color options.
        hovered_color = self.graphics.HIGHLIGHT
        inactive_color = self.graphics.DIM

        # Get the minefield options from the model.
        options = self.controller.get_minefield_options()
        mins = options["custom_minimums"]
        maxs = options["custom_maximums"]

        # Difficulty-specific message.
        self.info_message_textbox = TextBox(Point(1, 10))

        # NumberField for the length.
        info_length_numberfield = NumberField(Point(1, 13), 0, maxs.l)
        info_length_numberfield.set_minimum(mins.l)
        info_length_numberfield.set_hovered_color(hovered_color)
        info_length_numberfield.set_inactive_color(inactive_color)
        info_length_numberfield.set_prefix("Length: ")

        # NumberField for the height.
        info_height_numberfield = NumberField(Point(1, 14), 0, maxs.h)
        info_height_numberfield.set_minimum(mins.h)
        info_height_numberfield.set_hovered_color(hovered_color)
        info_height_numberfield.set_inactive_color(inactive_color)
        info_height_numberfield.set_prefix("Height: ")

        # NumberField for mine density.
        info_mines_numberfield = NumberField(Point(1, 15), 0, maxs.d)
        info_mines_numberfield.set_minimum(mins.d)
        info_mines_numberfield.set_hovered_color(hovered_color)
        info_mines_numberfield.set_inactive_color(inactive_color)
        info_mines_numberfield.set_prefix("Mine density: ")
        # Postfix is updated in self.update_information_box_text().

        self.uielements.append(TextBox(Point(1, 12), "Difficulty settings:"))
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
        easy_button.set_action(self.mk_easy_field)
        self.uielements.append(easy_button)

        # Medium Button.
        medium_button = Button(Point(1, 5), "Medium")
        medium_button.set_hovered_color(hovered_color)
        medium_button.set_inactive_color(disabled_color)
        medium_button.set_action(self.mk_medium_field)
        self.uielements.append(medium_button)

        # Hard Button.
        hard_button = Button(Point(1, 6), "Hard")
        hard_button.set_hovered_color(hovered_color)
        hard_button.set_inactive_color(disabled_color)
        hard_button.set_action(self.mk_hard_field)
        self.uielements.append(hard_button)

        # Custom Button.
        custom_button = Button(Point(1, 7), "Custom")
        custom_button.set_hovered_color(hovered_color)
        custom_button.set_inactive_color(disabled_color)
        custom_button.set_action(self.mk_custom_field)
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

    #
    # Button functionality.
    #

    def mk_custom_field(self):
        """
        Show a popup to confirm the minefield options. Generates the
        minefield if confirmed.
        """
        msg = "Do you want to generate a minefield with these options?"
        self.popup.set_text(msg)
        self.popup.set_title("GENERATE  FIELD?")
        self.set_focused_ui(self.popup)
        self.popup.set_enabled(True)

    def mk_hard_field(self):
        """
        Generates a minefield with hard difficulty.
        """
        hard_options = self.controller.get_minefield_options()["hard"]
        self.controller.set_difficulty(hard_options)
        return Action("goto generating view", [])

    def mk_medium_field(self):
        """
        Generates a minefield with medium difficulty.
        """
        medium_options = self.controller.get_minefield_options()["medium"]
        self.controller.set_difficulty(medium_options)
        return Action("goto generating view", [])

    def mk_easy_field(self):
        """
        Generates a minefield with easy difficulty.
        """
        easy_options = self.controller.get_minefield_options()["easy"]
        self.controller.set_difficulty(easy_options)
        return Action("goto generating view", [])

    #
    # Popup controls.
    #

    def custom_field_popup_action(self):
        """
        Handles Popup response for starting a new game with custom
        settings.

        Returns:
            Action: The action to give the controller.
        """
        if self.popup.get_option():
            custom_options = self.controller.get_minefield_options()["custom"]
            self.controller.set_difficulty(custom_options)
            return Action("goto generating view", [])
        return None
