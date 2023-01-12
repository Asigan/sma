import random

from pygame import Vector2


import core

from vivarium.agent import Agent


class Carnivore(Agent):
    def __init__(self, body):
        self.parent = Agent(body)
        self.body=body
        self.uuid=random.randint(100000,999999999)

    def update(self):
        superpredateurs, herbivores, carnivores = self.filtrePerception()

        if len(superpredateurs)>0:
            self.body.parent.acc += self.parent.repulsed(superpredateurs[0].body.parent.position, 10000, True, 0)

        if len(herbivores)>0:
            self.body.parent.acc += self.parent.attracted(superpredateurs[0].body.parent.position, 500, True, 0)


    # def filtrePerception(self):
    #     agents, items = self.parent.filtrePerception(self.body.parent())
    #     superpredateurs = []
    #     herbivores = []
    #     carnivores = []
    #     for agent in agents:
    #         if isinstance(agent, SuperpredateurBody):
    #             superpredateurs.append(agent)
    #         elif isinstance(agent, HerbivoreBody):
    #             herbivores.append(agent)
    #         elif isinstance(agent, CarnivoreBody):
    #             carnivores.append(agent)
    #
    #     return superpredateurs, herbivores, carnivores

