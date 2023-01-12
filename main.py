import random
from pygame.math import Vector2
import core
from agent import Agent
from body import Body

from agents.carnivore_agent import Carnivore
from bodies.carnivore_body import CarnivoreBody
from bodies import *
from vivarium.Vegetal import Vegetal
from vivarium.agents.decomposeur_agent import Decomposeur
from vivarium.agents.herbivore_agent import Herbivore
from vivarium.agents.superpredateur_agent import Superpredateur
from vivarium.bodies.decomposeur_body import DecomposeurBody
from vivarium.bodies.herbivore_body import HerbivoreBody
from vivarium.bodies.superpredateur_body import SuperpredateurBody
from vivarium.cadavres import Cadavre


def setup():
    print("Setup START---------")
    core.fps = 30
    core.WINDOW_SIZE = [800, 800]
    core.fullscreen=False

    nbCarnivores = 0
    nbHerbivores = 0
    nbSuperpredateurs = 1
    nbDecomposeurs = 0
    nbVegetaux = 0

    core.memory("agents", [])
    core.memory("carnivores", [])
    core.memory("herbivores", [])
    core.memory("superpredateurs", [])
    core.memory("decomposeurs", [])
    core.memory("vegetaux", [])
    core.memory("cadavres", [])

    for i in range(0,nbCarnivores):
        c = Carnivore(CarnivoreBody())
        core.memory('carnivores').append(c)
        core.memory('agents').append(c)
    for i in range(nbHerbivores):
        c = Herbivore(HerbivoreBody())
        core.memory('herbivores').append(c)
        core.memory('agents').append(c)
    for i in range(nbSuperpredateurs):
        c = Superpredateur(SuperpredateurBody())
        core.memory('superpredateurs').append(c)
        core.memory('agents').append(c)
    for i in range(nbDecomposeurs):
        c = Decomposeur(DecomposeurBody())
        core.memory('decomposeurs').append(c)
        core.memory('agents').append(c)
    for i in range(nbVegetaux):
        core.memory('vegetaux').append(Vegetal())




    print("Setup END-----------")


def computePerception(agent):
    for a in core.memory('agents'):
        fustrum = a.body.parent.furstrum
        fustrum.perceptionList = []
        for b in core.memory('agents'):
            if a.uuid!=b.uuid:
                if fustrum.inside(b.body.parent):
                    fustrum.perceptionList.append(b.body.parent)

def computeDecision(agent):
    for a in core.memory('agents'):
        a.update()


def applyDecision(agent):
    for a in core.memory('agents'):
        a.body.update()


def updateEnv():
    # for a in core.memory("agents"):
    #     for c in core.memory('agents'):
    #         if c.uuid != a.uuid:
    #             if a.body.parent.position.distance_to(c.body.parent.position) <= a.body.parent.size+c.body.parent.size:
    #                 if a.body.parent.size < c.body.parent.size:
    #                     c.body.parent.size+= a.body.parent.size / 2
    #                     core.memory("agents").remove(a)
    #                 else:
    #                     a.body.parent.size += c.body.parent.size / 2
    #                     core.memory("agents").remove(c)
    for c in core.memory("carnivores"):
        if c.body.parent.dead:
            cadavre = Cadavre(c.body.parent.position)
            core.memory("cadavres").append(cadavre)
            core.memory("carnivores").remove(c)
            core.memory("agents").remove(c)
            continue
        if c.body.parent.dedoubler:
            print("a dedoubler")
            newCar = c.body.dedoubler()
            print(newCar)
            core.memory("carnivores").append(newCar)
            core.memory("agents").append(newCar)
        for h in core.memory('herbivores'):
            if h.body.parent.position.distance_to(c.body.parent.position) <= h.body.parent.size + c.body.parent.size:
                c.body.parent.faim -= h.body.parent.size
                cadavre = Cadavre(h.body.parent.position)
                core.memory("cadavres").append(cadavre)
                core.memory("herbivores").remove(h)
                core.memory("agents").remove(h)

    for h in core.memory('herbivores'):
        if h.body.parent.dead:
            cadavre = Cadavre(h.body.parent.position)
            core.memory("cadavres").append(cadavre)
            core.memory("herbivores").remove(h)
            core.memory("agents").remove(h)
            continue
        if h.body.parent.dedoubler:
            newHer = h.body.dedoubler()
            core.memory("herbivores").append(newHer)
            core.memory("agents").append(newHer)
        for v in core.memory('vegetaux'):
            if v.position.distance_to(h.body.parent.position) <= h.body.parent.size + v.mass:
                h.body.parent.faim -= v.mass
                core.memory("vegetaux").remove(v)
                cadavre = Cadavre(v.position)
                core.memory("cadavres").append(cadavre)


    for s in core.memory("superpredateurs"):
        if s.body.parent.dead:
            cadavre = Cadavre(s.body.parent.position)
            core.memory("cadavres").append(cadavre)
            core.memory("superpredateurs").remove(s)
            core.memory("agents").remove(s)
            continue
        if s.body.parent.dedoubler:
            newHer = s.body.dedoubler()
            core.memory("superpredateurs").append(newHer)
            core.memory("agents").append(newHer)

        for c in core.memory("carnivores"):
            if s.body.parent.position.distance_to(c.body.parent.position) <= s.body.parent.size+c.body.parent.size:
                s.body.parent.faim -= c.body.parent.size
                cadavre = Cadavre(c.body.parent.position)
                core.memory("cadavres").append(cadavre)
                core.memory("carnivores").remove(c)
                core.memory("agents").remove(c)

    for s in core.memory("decomposeurs"):
        if s.body.parent.dead:
            core.memory("decomposeurs").remove(s)
            core.memory("agents").remove(s)
            continue
        if s.body.parent.dedoubler:
            newHer = s.body.dedoubler()
            core.memory("decomposeurs").append(newHer)
            core.memory("agents").append(newHer)


def reset():
    core.memory("agents", [])

    for i in range(0, 5):
        core.memory('agents').append(Agent(Body()))


def run():
    if core.getKeyPressList('r'):
        reset()
    core.cleanScreen()

    # Display
    for agent in core.memory("agents"):
        agent.show()

    for item in core.memory("vegetaux"):
        item.show()

    for item in core.memory("cadavres"):
        item.show()

    for agent in core.memory("agents"):
        computePerception(agent)

    for agent in core.memory("agents"):
        computeDecision(agent)

    for agent in core.memory("agents"):
        applyDecision(agent)

    updateEnv()

core.main(setup, run)