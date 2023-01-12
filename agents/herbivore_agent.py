import random

from pygame import Vector2


import core
import vivarium.toolbox_tore
from vivarium.body import Body
from vivarium.item import Item
from vivarium.agent import Agent
from vivarium.agent import Agent


class Herbivore(Agent):
    def __init__(self, body):
        self.parent = Agent(body)
        self.body=body
        self.uuid=random.randint(100000,999999999)

    def update(self):
        self.parent.update()