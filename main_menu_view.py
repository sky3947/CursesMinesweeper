"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point, Direction
from uielement import TextBox, LongTextBox, Button, Popup

class MainMenuView(View):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        """
        Instantiates a MainMenuView and returns it.

        Args:
            controller (Controller): The controller to pass user input.
        """
        super().__init__(controller)

        # The hovered input when entering this View.
        self.first_inp = "m"

        # Make the MINESWEEPER logo.
        self.make_banner()

        # Initialize selected variable.
        self.selected = None

        # Make Buttons
        self.make_buttons()

        # Make the information box. This explains each Button.
        self.make_info_box()

        # Make controls bar.
        self.make_controls_bar()

        # Set up Popup.
        self.make_popup()

        # Map of input to functions.
        enter = self.graphics.ENTER_KEY
        self.controls = {
            # Pressing "q" will quit the application.
            "q": lambda: Action("quit", []),

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

    def repeat_last_valid_input(self):
        """
        Repeats the last valid input.

        Returns:
            Action: The Action to pass to the controller.
        """
        return self.parse(self.controller.get_last_inp())

    def move_cursor(self, direction):
        """
        Moves the selected Button in a Direction.

        Args:
            direction (Direction): The Direction to move the cursor.

        Returns:
            Action: An empty Action.
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

        has_active_buttons = any(but.is_active() for but in self.buttons)
        if has_active_buttons:
            # Find the next active Button.
            cur_but_ind = self.buttons.index(self.selected)
            next_but_ind = (cur_but_ind + movement) % len(self.buttons)
            while not self.buttons[next_but_ind].is_active():
                next_but_ind = (next_but_ind + movement) % len(self.buttons)
            next_active_button = self.buttons[next_but_ind]

            # Update Buttons and information box.
            self.selected.set_hovered(False)
            next_active_button.set_hovered(True)
            self.selected = next_active_button
            self.update_information_box_text()

            self.controller.set_last_inp(last_input)

    def make_popup(self):
        """
        Initializes a reusable Popup.
        """
        popup_controls = {
            "q": self.reset_popup,
            "w": self.toggle_choice,
            "a": self.toggle_choice,
            "s": self.toggle_choice,
            "d": self.toggle_choice,
            self.graphics.ENTER_KEY: self.toggle_choice
        }
        self.popup = Popup(Point(0, 10), "", "")
        self.popup.set_color(self.graphics.BRIGHT)
        self.popup.set_highlight_color(self.graphics.HIGHLIGHT)
        self.popup.set_secondary_color(self.graphics.DIM)
        title_color = self.graphics.BRIGHT | self.graphics.UNDERLINE
        self.popup.set_title_color(title_color)
        self.popup.set_controls(popup_controls)
        self.popup.set_enabled(False)
        self.uielements.append(self.popup)

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
        delete_save_button.set_inactive_color(disabled_color)
        delete_save_button.set_action(self.delete_save)
        self.uielements.append(delete_save_button)

        # Continue Button.
        continue_button = Button(Point(centered_point.x, 13), "Continue")
        continue_button.set_color(color)
        continue_button.set_hovered_color(hovered_color)
        continue_button.set_inactive_color(disabled_color)
        continue_button.set_action(self.continue_game)
        self.uielements.append(continue_button)

        # New game Button.
        new_game_button = Button(Point(centered_point.x, 14), "New Game")
        new_game_button.set_color(color)
        new_game_button.set_hovered_color(hovered_color)
        new_game_button.set_inactive_color(disabled_color)
        new_game_button.set_action(self.new_game)
        self.uielements.append(new_game_button)

        # Keep track of Buttons.
        self.buttons = [continue_button, new_game_button, delete_save_button]

        self.selected = continue_button
        if self.controller.has_saved_game():
            continue_button.set_hovered(True)
        else:
            self.selected = new_game_button
            new_game_button.set_hovered(True)
            continue_button.set_active(False)
            delete_save_button.set_active(False)

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

    #
    # Button functionality.
    #

    def delete_save(self):
        """
        Sets up the Popup for deleting the saved game.
        """
        msg = (
            "You are about to delete your saved game. Do you want to proceed?"
        )
        self.popup.set_text(msg)
        self.popup.set_title("DELETE SAVE?")
        self.popup.change_control("m", self.delete_save_popup_click)
        self.set_focused_ui(self.popup)
        self.popup.set_enabled(True)

    def continue_game(self):
        pass

    def new_game(self):
        pass

    #
    # Popup controls.
    #

    def reset_popup(self):
        """
        Closes (disables) the Popup.
        """
        self.popup.set_enabled(False)
        self.popup.set_option(False)
        self.set_focused_ui(None)

    def toggle_choice(self):
        """
        Toggles the selected option in the Popup.
        """
        self.popup.set_option(not self.popup.get_option())

    def delete_save_popup_click(self):
        """
        Handles Popup response for deleting a saved game.
        """
        if self.popup.get_option():
            # Delete the saved game.
            # self.controller.delete_saved_game()

            # Reconfigure Buttons.
            self.buttons[0].set_active(False)
            self.buttons[1].set_hovered(True)
            self.buttons[2].set_hovered(False)
            self.buttons[2].set_active(False)
            self.selected = self.buttons[1]
            self.update_information_box_text()

        self.reset_popup()
