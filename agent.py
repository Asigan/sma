import random

from pygame import Vector2


import core
import toolbox_tore
from body import Body
from item import Item


class Agent(object):
    def __init__(self, body):
        self.body=body
        self.uuid=random.randint(100000,999999999)
        self.barycentre_last = Vector2(0,0)

    def deplacement_aleatoire(self, coeff):
        target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while target.length() == 0:
            target = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        target.scale_to_length(target.length()*coeff)
        return target

    def attracted(self, position, coeff, inverse_prop=False, power=1):
        target = self.closest_position_in_tore(position) - self.body.position
        if inverse_prop and target.length()>0.1:
            target.scale_to_length(1/(target.length()**power))
        if target.length()>0.1:
            target.scale_to_length(target.length() * coeff)
        return target

    def repulsed(self, position, coeff, inverse_prop=False, power=1):
        target = self.body.position - self.closest_position_in_tore(position)
        if inverse_prop and target.length()>0.1:
            target.scale_to_length(1/(target.length()**power))
        if target.length() > 0.1:
            target.scale_to_length(target.length() * coeff)
        return target

    def barycentre(self, liste):
        sum_pos = Vector2(0,0)
        for i in liste: sum_pos+=i
        return sum_pos/len(liste)

    def filtrePerception(self, perceptionList):
        agents=[]
        items=[]
        for i in self.body.fustrum.perceptionList:
            i.dist = self.shortest_distance_in_tore(i.body.position)
            if isinstance(i,Body):
                agents.append(i)
            elif isinstance(i, Item):
                items.append(i)

        agents.sort(key=lambda x: x.dist, reverse=False)
        items.sort(key=lambda x: x.dist, reverse=False)
        return agents,items

    def shortest_distance_in_tore(self, obj_pos):
        return self.body.position.distance_to(self.closest_position_in_tore(obj_pos))


    def closest_position_in_tore(self, obj_pos):
        if not self.body.fustrum.inTore: return obj_pos
        return toolbox_tore.closest_position_in_tore(self.body.position, obj_pos)

    def update(self):
        self.body.parent.acc = Vector2(0,0)
        target = self.deplacement_aleatoire(0.1)
        self.body.parent.acc += target

    def show(self):
        self.body.show()

