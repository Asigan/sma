import random

from pygame import Vector2

import core
from item import Item


class Cadavre(Item):
    def __init__(self, position):
        super().__init__()
        if position != Vector2(0,0):
            self.position = position

        self.mass = 10
        self.color = (200,0,0)

    def show(self):
        core.Draw.circle(self.color, self.position, self.mass)
