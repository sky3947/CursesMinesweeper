"""
This class is the model for the Minesweeper program.
"""

import os
from controller import Controller
from main_menu_view import MainMenuView

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

    def has_saved_game(self):
        """
        Checks if there's a save file.

        Returns:
            bool: True if a save file exists, False otherwise.
        """
        return os.path.exists(self.SAVE_FILE)

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
        self.controller.change_view(MainMenuView(self.controller))
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
