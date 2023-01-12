import random

from pygame import Vector2

import core
from vivarium.item import Item


class Cadavre(Item):
    def __init__(self, position):
        super()
        self.position = position
        self.mass = 2
        self.color = (200,0,0)

    def show(self):
        core.Draw.circle(self.color, self.position, self.mass)
