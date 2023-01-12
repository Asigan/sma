import random
import time

from pygame import Vector2

import core
from furstrum import Fustrum
from template.toolbox_tore import draw_circle_in_tore


class Body(object):
    def __init__(self):
        self.position=Vector2(random.randint(0,core.WINDOW_SIZE[0]),random.randint(0,core.WINDOW_SIZE[1]))
        self.vitesse = Vector2()
        self.vMax=0.5
        self.accMax=20
        self.faimMax = 10000
        self.faim = 0
        self.fatigueMax = 1000
        self.fatique = 0
        self.reproductionMax = 2000
        self.reproduction = 0
        self.dateNaissance = time.time()
        # on va considérer en secondes
        self.esperanceVie = 10
        self.dead = False
        self.tempsSommeil = 2
        self.fatigueMoinsParSieste = 30
        self.still = 0
        self.mutationPotential = 2
        self.dedoubler = False

        self.size=10
        self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.acc=Vector2()

    def set_champ_vision(self, nb):
        self.champVision = nb
        self.furstrum = Fustrum(nb, self)

    def update(self):
        self.evolutionParametres()
        if time.time()-self.dateNaissance >= self.esperanceVie:
            self.dead = True
            print("fin de vie")
        if self.faim >= self.faimMax:
            self.dead = True
            print("mort de faim")
        if self.still==0 and self.fatique >= self.fatigueMax:
            print("début de la sieste")
            self.still = time.time()

        if self.still != 0 and time.time()-self.still >=self.tempsSommeil:
            print("fin de la sieste")
            self.still = 0
            self.fatique -= self.fatigueMoinsParSieste
            self.fatique = self.fatique if self.fatique<0 else 0

        if self.reproduction >= self.reproductionMax:
            self.dedoubler=True

        if self.acc.length() > self.accMax/self.size:
            self.acc.scale_to_length(self.accMax / self.size)

        self.vitesse=self.vitesse+self.acc

        if self.vitesse.length() > self.vMax:
            self.vitesse.scale_to_length(self.vMax)

        self.position=self.position+self.vitesse
        if self.still!=0:
            self.acc *=0
            self.vitesse *=0

        core.Draw.line((255,255,255),self.position,self.position+self.acc*100,10)

        self.acc=Vector2()

        self.edge()

    def evolutionParametres(self):
        if self.still==0: self.fatique += 100/100
        self.faim += 100/500
        self.reproduction += 100/400

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

    def edge_tore(self):
        if self.position.x <= self.size or self.position.x + self.size >= core.WINDOW_SIZE[0]:
            self.position.x = self.position.x % core.WINDOW_SIZE[0]
        if self.position.y <= self.size or self.position.y + self.size >= core.WINDOW_SIZE[1]:
            self.position.y = self.position.y % core.WINDOW_SIZE[1]