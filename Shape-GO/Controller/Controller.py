import logging
import random as rnd
from time import sleep

import numpy as np

from GO.Helper import Shape
from GO.Model.Goban import Goban
from GO.View.Goban_View import GobanView


class Controller:

    def __init__(self, model: Goban, view: GobanView, shapes: list[Shape]):
        self.generated = False
        self.go_view = view
        self._current_player = 0  # default starting with black
        self.model = model
        self.shapes = shapes
        self.sel_shape = np.array([1])

    def setView(self, go_view: GobanView):
        self.go_view = go_view

    def _define_start_player(self):
        if self.model.hc != 0:
            self._current_player = 1  # starting with white

    def on_rotate(self):
        # should be a model function?
        self.sel_shape.shape = np.rot90(self.sel_shape.shape, 1, (1, 0))

    def on_generate(self):
        # select a shape at random based on the current player and display it
        # ! If HC != 0 white start
        self.sel_shape = rnd.choice(self.shapes)
        self._current_player = (self._current_player % 2) + 1  # between 1 (black) and 2 (white)
        self.generated = True
        self.go_view.update_text(self.sel_shape.name)

    def on_place(self, x: int, y: int):
        if self.generated and self.model.fits_shape_in_goban(self.sel_shape.shape, x, y):
            self.generated = False
            self.model.place_shape(self.sel_shape.shape, x, y, self._current_player)
            if self.model.captured(self._current_player):  # valid capture
                self.go_view.update_capt(self._current_player, self.model.captures)
                self.go_view.draw_goban(self.model.goban)
            else:
                self.model.remove_shape(self.sel_shape.shape, x, y)
                self.generated = True
                logging.info("self-capture -> notify user?")

    def preview(self, x, y):
        if self.generated:
            if self.model.fits_shape_in_goban(self.sel_shape.shape, x, y):
                self.go_view.preview_shape(self.sel_shape.shape, x, y, self._current_player)

    def on_start(self):
        print("Starting")
        self._define_start_player()
        self.go_view.start()
