"""
This class is the model for the Minesweeper program.
"""

import os
import random
import math
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

        # Minefield Options.
        self.options = {
            "easy": Option(10, 10, 10),
            "medium": Option(30, 20, 15),
            "hard": Option(60, 30, 20),
            "custom": Option(10, 10, 10),
            "custom_minimums": Option(2, 2, 1),
            "custom_maximums": Option(1024, 1024, 99)
        }

        # An Option to generate a minefield with.
        self.difficulty = None

        # A user feedback value for minefield generation (percentage.)
        self.gen_progress = 0

        # The current state of the minefield.
        self.minefield = None

        # The currently hovered cell's x-position.
        self.hover_x = 0

        # The currently hovered cell's y-position.
        self.hover_y = 0

    class Cell:
        """
        Stores information about an individual cell in the minefield.
        """
        def __init__(self, opened, mine, flagged, number):
            """
            Constructs an instance of Cell and returns it.

            Args:
                opened (bool): Whether or not this Cell has been opened.
                mine (bool): Whether or not this Cell is a mine.
                flagged (bool): Whether or not this Cell has been
                    flagged.
                number (int): The supposed number of mines around this
                    Cell.
            """
            self.opened = opened
            self.mine = mine
            self.flagged = flagged
            self.number = number

        def is_opened(self):
            """
            Checks if this cell has been opened.

            Returns:
                bool: True if opened, False otherwise.
            """
            return self.opened

        def open(self):
            """
            Opens this cell.
            """
            self.opened = True

        def is_mine(self):
            """
            Checks if this cell is a mine.

            Returns:
                bool: True if mine, False otherwise.
            """
            return self.mine

        def set_mine(self, mine):
            """
            Sets whether or not this cell is a mine.

            Args:
                mine (bool): True to make this cell a mine, False
                    otherwise.
            """
            self.mine = mine

        def is_flagged(self):
            """
            Checks if this cell is flagged.

            Returns:
                bool: True if flagged, False otherwise.
            """
            return self.flagged

        def set_flagged(self, flagged):
            """
            Sets whether or not this cell is flagged.

            Args:
                flagged (bool): True to flag this cell, False otherwise.
            """
            self.flagged = flagged

        def get_number(self):
            """
            Gets the number of surrounding mines.

            Returns:
                int: The number of surrounding mines.
            """
            return self.number

        def set_number(self, number):
            """
            Sets the supposed number of mines around this cell.

            Args:
                number (int): The supposed number of mines around this
                    cell.
            """
            self.number = number

    def save_minefield(self):
        """
        Saves the minefield.

        Minefield save format:
            HEADER:
                10 bits: LENGTH
                10 bits: HEIGHT
                10 bits: HOVERX
                10 bits: HOVERY
            DATA:
                3n bits: CELL

        LENGTH: One less than the length of the minefield.
        HEIGHT: One less than the height of the minefield.
        HOVERX: One less than the x-position of the hovered cell.
        HOVERY: One less than the y-position of the hovered cell.
        DATA: Sets of flags representing a cell. Each cell,
            C_n(O, M, F), where C_n is the nth cell (starting at n=0),
            is reconstructed into minefield position x=i%(LENGTH+1),
            y=i//(LENGTH+1). O, the "opened" flag, is only True if the
            cell has been opened. M, the "mine" flag, is only True if
            the cell is a mine. F, the "flagged" flag, is only True if
            the cell has been flagged. Any extra cells C_n where
            n>=#cells should be ignored.
        """
        # Parameters
        length = self.difficulty.l
        height = self.difficulty.h
        hover_x = self.hover_x
        hover_y = self.hover_y

        # Decide open mode.
        open_mode = "ab"
        if self.has_saved_game():
            open_mode = "wb"

        # Make header (length and height)
        piece_a = ((length-1)&0x3FF)<<30
        piece_b = ((height-1)&0x3FF)<<20
        piece_c = ((hover_x-1)&0x3FF)<<10
        piece_d = (hover_y-1)&0x3FF
        combined = piece_a|piece_b|piece_c|piece_d
        bin_header = combined.to_bytes(5, "big")

        with open(self.SAVE_FILE, open_mode) as save:
            # Write 5 byte header.
            save.write(bin_header)

            # Write each minefield cell.
            # Use a 3-byte buffer to save 8 cells at a time.
            mt_buffer = 0xFFFFFF
            buffer = mt_buffer
            current = 0
            max_index = length*height
            while current < max_index:
                for buffer_index in range(8):
                    if not current < max_index:
                        break
                    # Organize cell information.
                    cell = self.minefield[current//length][current%length]
                    opened = cell.is_opened()
                    mine = cell.is_mine()
                    flagged = cell.is_flagged()
                    cell_flags = opened<<2|mine<<1|flagged

                    # Put cell into buffer.
                    buffer &= cell_flags<<(3*(7-buffer_index))
                    current += 1

                # Write the buffer to file and reset.
                save.write(buffer.to_bytes(3, "big"))
                buffer = mt_buffer

    def generate_minefield(self):
        """
        Generates a minefield based on the options in self.difficulty.
        """
        # Parameters.
        length = self.difficulty.l
        height = self.difficulty.h
        mines = self.calculate_mines(self.difficulty)

        # Set up an empty minefield.
        mk_mt_cell = lambda: self.Cell(False, False, False, 0)
        self.minefield = [
            [mk_mt_cell() for _ in range(length)] for _ in range(height)
        ]

        # Done when mines_left == 0.
        mines_left = mines
        while mines_left > 0:
            # Pick a random cell.
            xselected = random.randint(0, length - 1)
            yselected = random.randint(0, height - 1)

            # Try to make it a mine.
            selected_cell = self.minefield[yselected][xselected]
            if not selected_cell.is_mine():
                selected_cell.set_mine(True)

                # Increment the numbers around the mine.
                xbound = (max(0, xselected - 1), min(length, xselected + 1))
                ybound = (max(0, yselected - 1), min(height, yselected + 1))
                for xpos in range(*xbound):
                    for ypos in range(*ybound):
                        cell = self.minefield[ypos][xpos]
                        cell.set_number(cell.get_number() + 1)

                # Update gen_progress.
                mines_left -= 1
                self.gen_progress = round((1 - (mines_left / mines)) * 100)

    def reset_gen_progress(self):
        """
        Resets the gen_progress.
        """
        self.gen_progress = 0

    def get_gen_progress(self):
        """
        Gets a user feedback value for minefield generation.

        Returns:
            int: A percentage.
        """
        return self.gen_progress

    @staticmethod
    def calculate_mines(option):
        """
        Calculates the number of mines in a minefield.

        Args:
            option (Option): An Option containing length, height, and
            mine density.

        Returns:
            int: The number of mines generated.
        """
        min_mines = 1
        max_mines = option.l * option.h - 1
        raw_mines = math.floor(option.l * option.h * option.d / 100)
        return min(max_mines, max(min_mines, raw_mines))

    def set_difficulty(self, option):
        """
        Sets the difficulty of the minefield to generate.

        Args:
            option (Option): The Option containing length, height, and
            density information.
        """
        self.difficulty = option

    def set_custom_field_options(self, option):
        """
        Sets the length, height, and density values for generating a
        custom minefield.

        Args:
            option (Option): An Option containing length, height, and
            mine density.
        """
        self.options["custom"] = option

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
