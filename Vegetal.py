import random

from pygame import Vector2

import core
from item import Item


class Vegetal(Item):
    def __init__(self):
        super().__init__()
        self.position = Vector2(random.randint(0, core.WINDOW_SIZE[0]), random.randint(0, core.WINDOW_SIZE[1]))
        self.mass = 5
        self.color = (0,255,0)

    def show(self):
        core.Draw.circle(self.color, self.position, self.mass)
