"""
The generating View provides information to user as the minefield
is being generated. Then, the user is redirected to the game View. This
is not an interactable View.
"""

import time
import threading
from views.view import View
from utility import Action

class GeneratingView(View):
    """
    Provides user with progress updates to minefield generation.
    """

    class Feedback(threading.Thread):
        """
        Provides user feedback while minefield is generating.
        """
        def __init__(self, view):
            """
            Instantiates a Feedback thread and returns it.

            Args:
                view (View): The View this belongs to.
            """
            threading.Thread.__init__(self)
            self.view = view

        def run(self):
            progress = self.view.controller.get_gen_progress()
            while progress < 100:
                progress = self.view.controller.get_gen_progress()
                params = self.view.graphics.center_just(16, str(progress)+"%")
                self.view.graphics.draw(*params)
                self.view.graphics.refresh()
                time.sleep(0.05)

    class Generator(threading.Thread):
        """
        Tells the model to generate a minefield.
        """
        def __init__(self, view):
            """
            Instantiates a Generator thread and returns it.

            Args:
                view (View): The View this belongs to.
            """
            threading.Thread.__init__(self)
            self.view = view

        def run(self):
            self.view.controller.generate_minefield()

    # Override the View loop so that user input is not queried.
    def loop(self):
        self.graphics.clear()

        # Drawing text.
        params = self.graphics.center_just(14, "Generating minefield...")
        self.graphics.draw(*params)
        feedback = self.Feedback(self)
        generator = self.Generator(self)
        feedback.start()

        # Generate minefield.
        generator.start()

        # Wait for feedback thread to finish.
        generator.join()
        feedback.join()
        self.controller.reset_gen_progress()
        self.graphics.flush_inp()

        # Redirect to game view.
        self.controller.act(Action("goto game view", []))
