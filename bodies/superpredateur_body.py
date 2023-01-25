import random
import time

from pygame import Vector2

import core
from furstrum import Fustrum
from body import Body
from toolbox_tore import draw_circle_in_tore


class SuperpredateurBody(Body):
    def __init__(self):
        super().__init__()
        self.size = 15
        self.vMax = 5
        self.accMax = 50
        self.faimMax = 100
        self.faim = 0
        self.fatigueMax = 100
        self.fatigue = 0
        self.reproductionMax = 100
        self.reproduction = 0
        self.dateNaissance = time.time()
        # on va considérer en secondes
        self.esperanceVie = 100
        self.set_champ_vision(250)
        self.color = (255, 0, 0)
        self.targets = ["carnivores"]


    def dedoubler(self):
        c = SuperpredateurBody()
        v = Vector2(random.randint(-5, 5), random.randint(-5, 5))
        c.position = self.position + v
        c.mutation()
        self.aDedoubler = False
        self.reproduction = 0
        return c

    def update(self):
        super().update()
    def show(self):
        super().show()
