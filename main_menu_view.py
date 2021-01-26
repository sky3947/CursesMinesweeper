"""
The main menu View provides graphics and receives input to continue,
start, or delete a Minesweeper game.
"""

from view import View
from utility import Action, Point, Direction
from uielement import TextBox, LongTextBox, Button, Popup

class MainMenuView(View):
    """
    Draws main menu elements, such as: TextBoxes, Buttons and Popups.
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

        # Initialize selected variable.
        self.selected = None

        # Make the MINESWEEPER logo.
        self.make_banner()

        # Make Buttons.
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
        Changes the selected Button to another in a Direction.

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

        has_active_buttons = any(but.is_active() for but in self.buttons)
        if has_active_buttons:
            # Find the next active Button.
            cur_but_ind = self.buttons.index(self.selected)
            next_but_ind = (cur_but_ind + movement) % len(self.buttons)
            while not self.buttons[next_but_ind].is_active():
                next_but_ind = (next_but_ind + movement) % len(self.buttons)
            next_selected_button = self.buttons[next_but_ind]

            # Update Buttons and information box.
            self.selected.set_hovered(False)
            next_selected_button.set_hovered(True)
            self.selected = next_selected_button
            self.update_information_box_text()

            self.controller.set_last_inp(last_input)

    def make_popup(self):
        """
        Initializes a reusable Popup.
        """
        self.popup = Popup(Point(0, 10), self, "", "")
        self.popup.set_highlight_color(self.graphics.HIGHLIGHT)
        self.popup.set_secondary_color(self.graphics.DIM)
        title_color = self.graphics.BRIGHT | self.graphics.UNDERLINE
        self.popup.set_title_color(title_color)
        self.popup.set_enabled(False)
        self.uielements.append(self.popup)

    def make_controls_bar(self):
        """
        Creates the controls bar to display controls.
        """
        text = [
            "_"*self.graphics.LENGTH,
            " wasd: Move | m: Select | q: Quit"
        ]
        controls = LongTextBox(Point(0, self.graphics.HEIGHT-3), text)
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
        self.info_box = TextBox(Point(1, 22))
        self.uielements.append(self.info_box)
        self.update_information_box_text()

        info_box_bar = TextBox(Point(0, 21), "_"*self.graphics.LENGTH)
        self.uielements.append(info_box_bar)

    def make_buttons(self):
        """
        Initializes and adds Buttons.
        """
        # Color options.
        hovered_color = self.graphics.HIGHLIGHT
        disabled_color = self.graphics.DIM

        # Delete save Button.
        text = "Delete Save"
        centered_point, _ = self.graphics.center_just(15, text)
        delete_save_button = Button(centered_point, text)
        delete_save_button.set_hovered_color(hovered_color)
        delete_save_button.set_inactive_color(disabled_color)
        delete_save_button.set_action(self.delete_save)
        self.uielements.append(delete_save_button)

        # Continue Button.
        continue_button = Button(Point(centered_point.x, 13), "Continue")
        continue_button.set_hovered_color(hovered_color)
        continue_button.set_inactive_color(disabled_color)
        continue_button.set_action(self.continue_game)
        self.uielements.append(continue_button)

        # New game Button.
        new_game_button = Button(Point(centered_point.x, 14), "New Game")
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
        banner = [
			R"  __ __ _ __  _ ___  __  _   _ ___ ___ ___ ___ ___  ",
			R" |  V  | |  \| | __/' _/| | | | __| __| _,\ __| _ \ ",
			R" | \_/ | | | ' | _|`._`.| 'V' | _|| _|| v_/ _|| v / ",
			R" !_! !_!_!_!\__!___!___/!_/ \_!___!___!_! !___!_!_\ "
		]
        start_point, _ = self.graphics.center_just(4, banner[0])
        title = LongTextBox(start_point, banner)
        self.uielements.append(title)

    def display_loading_screen(self):
        """
        Clears all UIElements and puts a loading text on the screen.
        """
        self.uielements = []
        msg = "Loading minefield..."
        centered = self.graphics.center_just(self.graphics.HEIGHT//2, msg)
        loading_text = TextBox(*centered)
        loading_text.set_color(self.graphics.BRIGHT)
        self.uielements.append(loading_text)

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
        self.popup.set_action(self.delete_save_popup_action)
        self.set_focused_ui(self.popup)
        self.popup.set_enabled(True)

    def continue_game(self):
        """
        Tells the Model to load the save file and continue to the game
        View.
        """
        self.display_loading_screen()

        # TODO: Load save file.

    def new_game(self):
        """
        Sets up the Popup warning for overriding an existing game, or
        skips Popup if there's no saved game.
        """
        if self.controller.has_saved_game():
            msg = (
                "You are about to override your save file with a new game. Do "
                "you want to proceed?"
            )
            self.popup.set_text(msg)
            self.popup.set_title("OVERRIDE SAVE?")
            self.popup.set_action(self.new_game_popup_click)
            self.set_focused_ui(self.popup)
            self.popup.set_enabled(True)

    #
    # Popup controls.
    #

    def delete_save_popup_action(self):
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

    def new_game_popup_click(self):
        """
        Handles Popup response for starting a new game.

        Returns:
            Action: The action to give the controller (change view to
            new_game_view.)
        """
        if self.popup.get_option():
            return Action("goto new game view", [])
        return None
