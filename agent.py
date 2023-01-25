import random

from pygame import Vector2


import core
import toolbox_tore
from body import Body
from bodies.carnivore_body import CarnivoreBody
from bodies.decomposeur_body import DecomposeurBody
from bodies.herbivore_body import HerbivoreBody
from bodies.superpredateur_body import SuperpredateurBody
from cadavres import Cadavre
from Vegetal import Vegetal


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

    def manger(self, nourriture):
        if self.body.seuilfaim*self.body.faimMax/100>self.body.faim:
            #print("pas faim: ",self.body.seuilfaim,">",self.body.faim)
            self.body.wantToEat = False
            return
        if len(nourriture)>0 :
            self.body.acc += self.attracted(nourriture[0].position, 1)
            self.body.wantToEat = True

    def survie(self, predateurs):
            self.body.acc += self.repulsed(predateurs[0].position, 10)
            self.body.wantToEat = False
            self.body.isEating = 0
    def symbiose(self, superpredateurs, carnivores, herbivores, vegetaux):
        if len(superpredateurs):
            self.body.acc += self.attracted(superpredateurs[0].position, self.body.symbioseSP)
        if len(carnivores):
            self.body.acc += self.attracted(carnivores[0].position, self.body.symbioseC)
        if len(herbivores):
            self.body.acc += self.attracted(herbivores[0].position, self.body.symbioseH)
        if len(vegetaux):
            self.body.acc += self.attracted(vegetaux[0].position, self.body.symbioseV)

    def filtrePerception(self):
        superpredateurs=[]
        carnivores = []
        herbivores = []
        decomposeurs = []
        vegetaux=[]
        cadavres=[]

        for i in self.body.furstrum.perceptionList:
            i.dist = self.shortest_distance_in_tore(i.position)
            if isinstance(i,SuperpredateurBody):
                superpredateurs.append(i)
            elif isinstance(i,CarnivoreBody):
                carnivores.append(i)
            elif isinstance(i,HerbivoreBody):
                herbivores.append(i)
            elif isinstance(i,DecomposeurBody):
                decomposeurs.append(i)
            elif isinstance(i, Vegetal):
                vegetaux.append(i)
            elif isinstance(i, Cadavre):
                cadavres.append(i)

        superpredateurs.sort(key=lambda x: x.dist, reverse=False)
        carnivores.sort(key=lambda x: x.dist, reverse=False)
        herbivores.sort(key=lambda x: x.dist, reverse=False)
        decomposeurs.sort(key=lambda x: x.dist, reverse=False)
        vegetaux.sort(key=lambda x: x.dist, reverse=False)
        cadavres.sort(key=lambda x: x.dist, reverse=False)

        return superpredateurs,carnivores, herbivores, decomposeurs, vegetaux, cadavres

    def shortest_distance_in_tore(self, obj_pos):
        return self.body.position.distance_to(self.closest_position_in_tore(obj_pos))


    def closest_position_in_tore(self, obj_pos):
        if not self.body.furstrum.inTore: return obj_pos
        return toolbox_tore.closest_position_in_tore(self.body.position, obj_pos)

    def update(self):
        self.body.acc = Vector2(0,0)
        target = self.deplacement_aleatoire(0.1)
        self.body.acc += target



    def show(self):
        self.body.show()

