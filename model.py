"""
This class is the model for the Minesweeper program.
"""

import os
from controller import Controller
from utility import Option

class Model:
    """
    Stores data and logic for Minesweeper.
    """

    # Game save information.
    SAVE_PATH = "./saves/"
    SAVE_FILE = SAVE_PATH + "minefield.save"

    def __init__(self, screen):
        """
        Constructs an instance of Model and returns it.

        Args:
            screen (_CursesWindow): A standard screen object from the
                curses library.
        """
        # The controller class for user interaction.
        self.controller = Controller(self, screen)

        # Controls the game loop.
        self.running = True

        # The current view.
        self.view = None

        # Minefield options.
        self.options = {
            "easy": Option(10, 10, 10),
            "medium": Option(30, 20, 15),
            "hard": Option(60, 30, 20),
            "custom": Option(10, 10, 10)
        }

        # The current state of the minefield.
        self.minefield = None

    def set_custom_field_options(self, values):
        """
        Sets the length, height, and density values for generating a
        custom minefield.

        Args:
            values (list): An array [length, height, density].
        """
        self.options["custom"] = Option(*values)

    def has_saved_game(self):
        """
        Checks if there's a save file.

        Returns:
            bool: True if a save file exists, False otherwise.
        """
        return os.path.exists(self.SAVE_FILE)

    def delete_saved_game(self):
        """
        Deletes the save file.
        """
        if self.has_saved_game():
            os.remove(self.SAVE_FILE)

    def change_view(self, view):
        """
        Sets the next view to be served to the user.

        Args:
            view (View): The next view.
        """
        self.view = view

    def start(self):
        """
        Starts the game loop at the main menu view.
        """
        self.controller.start()
        self.loop()

    def stop_game_loop(self):
        """
        Stops the game loop.
        """
        self.running = False

    def loop(self):
        """
        The main game loop. The view may change at any time.
        """
        while self.running:
            self.view.loop()
