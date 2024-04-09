"""
The continue game View provides an intermediate View to inform the
user that the minefield is loading.
"""

import threading
import time
from views.view import View
from utility import Action

class ContinueGameView(View):
    """
    Intermediate View for loading the minefield from a file.
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

    class Loader(threading.Thread):
        """
        Tells the model to load a minefield.
        """

        def __init__(self, view):
            """
            Instantiates a Loader thread and returns it.

            Args:
                view (View): The View this belongs to.
            """
            threading.Thread.__init__(self)
            self.view = view

        def run(self):
            self.view.controller.load_minefield()

    # Override the View loop so that user input is not queried.
    def loop(self):
        self.graphics.clear()

        # Drawing text.
        params = self.graphics.center_just(14, "Loading minefield...")
        self.graphics.draw(*params)
        feedback = self.Feedback(self)
        loader = self.Loader(self)
        feedback.start()

        # Load minefield.
        loader.start()

        # Wait for feedback thread to finish.
        loader.join()
        feedback.join()
        self.controller.reset_gen_progress()
        self.graphics.flush_inp()

        # Redirect to game view.
        self.controller.act(Action("goto game view", []))
