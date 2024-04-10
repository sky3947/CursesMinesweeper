"""
This class is the View for the Minesweeper program.
"""

from abc import ABC
from utility import Flow, Point, Action

class View(ABC):
    """
    Translates model information into human-readable information by
    drawing graphics. Also passes user input onto the controller.
    """
    def __init__(self, controller):
        # A View communicates with a controller.
        self.controller = controller

        # A View needs to draw graphics.
        self.graphics = controller.graphics

        # The hovered input when entering this View.
        self.first_inp = ""

        # A list of UIElements in the View.
        self.uielements = []

        # The interactable UI currently being focused.
        self.focused_ui = None

        # The default table of controls.
        self.controls = {}

    def parse(self, inp):
        """
        A scene could parse input and return an action.

        Args:
            inp (str): A single character input from the user.

        Returns:
            Action: The action for the controller to perform.
        """
        mt_reaction = lambda: Action("", [])

        reaction = None
        if self.focused_ui is not None and self.focused_ui.is_focusable():
            reaction = self.focused_ui.controls.get(inp, mt_reaction)
            if not self.focused_ui.is_blocking():
                # Run focused_ui reaction first
                reaction()
                reaction = self.controls.get(inp, mt_reaction)
        else:
            reaction = self.controls.get(inp, mt_reaction)

        return reaction() or mt_reaction()

    def set_focused_ui(self, uielement):
        """
        Sets the focused UIElement.

        Args:
            uielement (UIElement): The focused UIElement.
        """
        self.focused_ui = uielement

    def get_focused_ui(self):
        """
        Gets the focused UIElement.

        Returns:
            UIElement: The focused UIElement.
        """
        return self.focused_ui

    def draw(self):
        """A scene could have graphics."""
        self.graphics.clear()

        for uielement in self.uielements:
            uielement.draw(self.graphics)

        # Draw last valid input.
        text = "({})".format(self.controller.get_last_inp())
        self.graphics.draw(Point(1, self.graphics.HEIGHT-1), text)

    def get_first_input(self):
        """
        Gets the first hovered input when entering this View.

        Returns:
            str: The first hovered input.
        """
        return self.first_inp

    def loop(self):
        """The main loop of a View."""
        while True:
            self.draw()

            action = self.parse(self.graphics.get_inp())
            flow = self.controller.act(action)

            # Use Flow.RETURN when changing scenes. Stops stack growth.
            if flow is Flow.RETURN:
                return

            # Use Flow.BREAK when stopping the game loop.
            if flow is Flow.BREAK:
                break

            if flow is Flow.CONTINUE:
                continue

            if flow is Flow.PASS:
                pass

        # If this portion is reached, stop the game loop.
        self.controller.stop_game_loop()
