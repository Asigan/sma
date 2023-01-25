import random
import time

from pygame import Vector2

import core
from furstrum import Fustrum
from toolbox_tore import draw_circle_in_tore


class Body(object):
    def __init__(self):
        self.position=Vector2(random.randint(0,core.WINDOW_SIZE[0]),random.randint(0,core.WINDOW_SIZE[1]))
        self.vitesse = Vector2()
        self.vMax=0.5
        self.accMax=20
        self.faimMax = 100
        self.seuilfaim = self.faimMax/2
        self.faim = 0
        self.fatigueMax = 5
        self.seuilfatigue = self.fatigueMax/2
        self.fatigue = 0
        self.reproductionMax = 60
        self.reproduction = 0
        self.distanceFuite = 75
        self.dateNaissance = time.time()
        self.symbioseSP = 0
        self.symbioseC = 0
        self.symbioseH = 0
        self.symbioseD = 0
        self.symbioseV = 0
        # on va considérer en secondes
        self.esperanceVie = 100
        self.dead = False
        self.tempsSommeil = 2
        self.still = 0
        self.mutationPotential = 1
        self.aDedoubler = False

        self.isEating = 0
        self.wantToEat = False

        self.champVision = 100
        self.furstrum = Fustrum(self.champVision, self)

        self.size=10
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.acc=Vector2()
        self.last_tick = time.time()

        self.targets = []

    def mutation(self):
        mutat = (random.random()-1)*self.mutationPotential
        self.vMax += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.accMax += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.faimMax += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.seuilfaim += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.distanceFuite += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.symbioseC += mutat
        mutat = (random.random() - 1) * 0.1
        self.distanceFuite += mutat
        mutat = (random.random() - 1) * 0.1
        self.symbioseSP += mutat
        mutat = (random.random() - 1) * 0.1
        self.symbioseD += mutat
        mutat = (random.random() - 1) * 0.1
        self.symbioseV += mutat
        mutat = (random.random() - 1) * 0.1
        self.symbioseH += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.seuilfatigue += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.tempsSommeil += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.esperanceVie += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.reproductionMax += mutat
        mutat = (random.random() - 1) * self.mutationPotential
        self.champVision += mutat

    def set_champ_vision(self, nb):
        self.champVision = nb
        self.furstrum = Fustrum(nb, self)

    def update(self):
        self.evolutionParametres()
        if time.time()-self.dateNaissance >= self.esperanceVie:
            self.dead = True
        if self.faim >= self.faimMax:
            self.dead = True

        if self.still==0 and self.fatigue >= self.fatigueMax:
            self.still = time.time()

        if self.reproduction >= self.reproductionMax:
            self.aDedoubler=True

        if self.still>0 or self.isEating>0:
            self.acc *= 0
            self.vitesse *= 0.9

        if self.acc.length() > self.accMax/self.size:
            self.acc.scale_to_length(self.accMax / self.size)

        self.vitesse=self.vitesse+self.acc

        if self.vitesse.length() > self.vMax:
            self.vitesse.scale_to_length(self.vMax)

        self.position=self.position+self.vitesse


        core.Draw.line((255,255,255),self.position,self.position+self.acc*100,10)

        self.acc = Vector2()
        self.edge()

    def evolutionParametres(self):
        evol = time.time() - self.last_tick
        if self.still == 0:
            self.fatigue = min(self.fatigue+evol, self.fatigueMax)
        else:
            self.fatigue = max(self.fatigue-2*evol, 0)

        self.faim = min(self.faim+evol, self.faimMax)
        self.reproduction = min(self.reproduction+evol, self.reproductionMax)

        if self.still != 0 and (time.time() - self.still >= self.tempsSommeil or self.fatigue <= 0):
            self.still = 0

        if self.isEating > 0:
            self.isEating -= evol
            self.faim = max(self.faim-evol*6, 0)
            if self.faim == 0:
                self.isEating = 0

        self.last_tick += evol
    def show(self):
        self.furstrum.show()
        draw_circle_in_tore(self.position, self.size, width=0, color=self.color)

    def edge(self):
        if self.furstrum.inTore:
            self.edge_tore()
            return
        if self.position.x <=self.size:
            self.vitesse.x *= -1
        if self.position.x+self.size >= core.WINDOW_SIZE[0]:
            self.vitesse.x *= -1
        if self.position.y <= self.size:
            self.vitesse.y *= -1
        if self.position.y +self.size>= core.WINDOW_SIZE[1]:
            self.vitesse.y *= -1

    def eat(self, mass):
        self.isEating = mass
    def edge_tore(self):
        if self.position.x <= self.size or self.position.x + self.size >= core.WINDOW_SIZE[0]:
            self.position.x = self.position.x % core.WINDOW_SIZE[0]
        if self.position.y <= self.size or self.position.y + self.size >= core.WINDOW_SIZE[1]:
            self.position.y = self.position.y % core.WINDOW_SIZE[1]