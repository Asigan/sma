import random
import time

from pygame import Vector2

import core
from furstrum import Fustrum
from body import Body
from toolbox_tore import draw_circle_in_tore



class CarnivoreBody(Body):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.vMax = 2
        self.accMax = 10
        self.faimMax = 20
        self.seuilfaim = 50
        self.faim = 0
        self.fatigueMax = 10
        self.fatique = 0
        self.reproductionMax = 100
        self.reproduction = 0
        self.dateNaissance = time.time()
        # on va considérer en secondes
        self.esperanceVie = 100
        self.set_champ_vision(200)
        self.color = (255,125,0)
        self.targets = ["herbivores"]

    def dedoubler(self):
        c = CarnivoreBody()
        v = Vector2(random.randint(-5, 5), random.randint(-5, 5))
        c.position = self.position+v
        c.mutation()
        self.aDedoubler = False
        self.reproduction=0
        return c

    def update(self):
        super().update()

    def show(self):
        super().show()
