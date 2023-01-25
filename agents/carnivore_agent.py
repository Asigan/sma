import random

from pygame import Vector2


import core

from agent import Agent


class Carnivore(Agent):
    def __init__(self, body):
        super().__init__(body)

    def update(self):
        superpredateurs,carnivores, herbivores, decomposeurs, vegetaux, cadavres = self.filtrePerception()
        if len(superpredateurs)>0:
            self.survie(superpredateurs)
        elif len(herbivores)>0:
            self.manger(herbivores)

        if self.body.acc.length() == 0:
            self.symbiose(superpredateurs, carnivores, herbivores, vegetaux)
            if self.body.acc.length() > 0.01:
                self.body.acc.scale_to_length(self.body.acc.length()/100)
            self.body.acc += self.deplacement_aleatoire(1)




    def dedoubler(self):
        return Carnivore(self.body.dedoubler())
