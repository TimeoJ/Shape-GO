import numpy as np


class Shape:

    def __init__(self, name: str, shape: np.array):
        self.name = name
        self.shape = shape  # create shapes for white and black. More colors possible!

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
