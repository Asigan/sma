import random
import time

from pygame import Vector2

import core
from vivarium.agents.decomposeur_agent import Decomposeur
from vivarium.furstrum import Fustrum
from vivarium.body import Body
from vivarium.toolbox_tore import draw_circle_in_tore


class DecomposeurBody(Body):
    def __init__(self):
        self.parent = Body()
        self.parent.size = 2
        self.parent.vMax = 0.5
        self.parent.accMax = 20
        self.parent.faimMax = 100
        self.parent.faim = random.randint(0, self.parent.faimMax / 2)
        self.parent.fatigueMax = 100
        self.parent.fatique = random.randint(0, self.parent.fatigueMax / 2)
        self.parent.reproductionMax = 100
        self.parent.reproduction = random.randint(0, self.parent.reproductionMax / 2)
        self.parent.dateNaissance = time.time()
        # on va considérer en secondes
        self.parent.esperanceVie = 100
        self.parent.set_champ_vision(2)
        self.parent.color = (0, 0, 255)

    def dedoubler(self):
        c = DecomposeurBody()
        v = Vector2(random.randint(-5, 5), random.randint(-5, 5))
        c.position = self.parent.position + v
        mutation = 0.1 * random.randint(-self.parent.mutationPotential, self.parent.mutationPotential)
        c.faimMax = self.parent.faimMax + mutation
        mutation = 0.1 * random.randint(-self.parent.mutationPotential, self.parent.mutationPotential)
        c.fatigueMax = self.parent.fatigueMax + mutation
        mutation = 0.1 * random.randint(-self.parent.mutationPotential, self.parent.mutationPotential)
        c.reproductionMax = self.parent.reproductionMax + mutation
        mutation = 0.1 * random.randint(-self.parent.mutationPotential, self.parent.mutationPotential)
        c.parent.vMax = self.parent.vMax + mutation
        self.parent.dedoubler = False
        self.parent.reproduction = 0
        return Decomposeur(c)

    def update(self):
        self.parent.update()

    def show(self):
        self.parent.show()
