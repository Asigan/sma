import json
import os
import random
import time

from pygame.math import Vector2
import core
from agent import Agent
from body import Body

from agents.carnivore_agent import Carnivore
from bodies.carnivore_body import CarnivoreBody
from Vegetal import Vegetal
from agents.decomposeur_agent import Decomposeur
from agents.herbivore_agent import Herbivore
from agents.superpredateur_agent import Superpredateur
from bodies.decomposeur_body import DecomposeurBody
from bodies.herbivore_body import HerbivoreBody
from bodies.superpredateur_body import SuperpredateurBody
from cadavres import Cadavre


def statsPopulation():
    if not core.getKeyPressList("i"): return
    core.memory("lastRefresh", time.time())
    print("-------------Simulation stats-------------")
    print("Nb d'agents :", len(core.memory("agents")))
    for typeAgent in core.memory("typesAgents"):
        print("-----", len(core.memory(typeAgent)), typeAgent, "(","%.2f" % (100*len(core.memory(typeAgent))/len(core.memory("agents"))), "%)")

    for typeAgent in core.memory("typesAgents"):
        print("Stats des ", typeAgent)
        agents = core.memory(typeAgent)
        if len(agents)==0:
            print("Plus d'individus dans cette population")
            continue
        for attr in agents[0].body.__dict__:
            if isinstance(getattr(agents[0].body, attr), Vector2): continue
            if attr in ["furstrum", "faim", "fatigue", "reproduction", "dateNaissance", "dead", "still",
                        "mutationPotential", "aDedoubler", "isEating", "wantToEat", "color", "targets", "fatique", "dist", "last_tick"]:
                continue
            attrMax = getattr(agents[0].body, attr)
            indexMax = 0
            attrMoy = getattr(agents[0].body, attr)
            attrMin = getattr(agents[0].body, attr)
            indexMin = 0
            for i in range(1, len(agents)):
                attrcur = getattr(agents[i].body, attr)
                attrMoy += attrcur
                if attrMax < attrcur:
                    indexMax = i
                    attrMax = attrcur
                if attrMin > attrcur:
                    indexMin = i
                    attrMin = attrcur
            if len(agents)>1:
                print("-------", attr, " -> Max: ", attrMax, "(", agents[indexMax].uuid, "), Moy:", attrMoy/len(agents), ", Min:", attrMin, "(", agents[indexMin].uuid,")")
            else:
                print("-------", attr, " -> valeur ", attrMoy)




def setup():
    print("Setup START---------")
    # print(os.getcwd())


    core.fps = 30
    core.WINDOW_SIZE = [800, 800]
    core.fullscreen=False

    nbCarnivores = 0
    nbHerbivores = 1
    nbSuperpredateurs = 0
    nbDecomposeurs = 0
    nbVegetaux = 50

    core.memory("agents", [])
    core.memory("typesAgents", ["superpredateurs", "carnivores", "herbivores", "decomposeurs"])
    core.memory("typesTargets", ["carnivores", "herbivores", "vegetaux", "cadavres"])
    core.memory("carnivores", [])
    core.memory("herbivores", [])
    core.memory("superpredateurs", [])
    core.memory("decomposeurs", [])
    core.memory("vegetaux", [])
    core.memory("cadavres", [])
    core.memory("respawnPerSec", 0)
    core.memory("respawns", 0)
    core.memory("refreshStats", 5)
    core.memory("lastRefresh", time.time()-5)
    load('scenario.json')
    # for i in range(0,nbCarnivores):
    #     c = Carnivore(CarnivoreBody())
    #     core.memory('carnivores').append(c)
    #     core.memory('agents').append(c)
    # for i in range(nbHerbivores):
    #     c = Herbivore(HerbivoreBody())
    #     core.memory('herbivores').append(c)
    #     core.memory('agents').append(c)
    # for i in range(nbSuperpredateurs):
    #     c = Superpredateur(SuperpredateurBody())
    #     core.memory('superpredateurs').append(c)
    #     core.memory('agents').append(c)
    # for i in range(nbDecomposeurs):
    #     c = Decomposeur(DecomposeurBody())
    #     core.memory('decomposeurs').append(c)
    #     core.memory('agents').append(c)
    # for i in range(nbVegetaux):
    #     core.memory('vegetaux').append(Vegetal())

    print("Setup END-----------")

def load(path):
    with open(path) as f:
        data = json.load(f)

    for i in range(data["carnivores"]["nb"]):
        c = Carnivore(CarnivoreBody())
        adaptToParameters(c, data["carnivores"]["parametres"])
        core.memory('carnivores').append(c)
        core.memory('agents').append(c)

    for i in range(data["herbivores"]["nb"]):
        c = Herbivore(HerbivoreBody())
        adaptToParameters(c, data["herbivores"]["parametres"])
        core.memory('herbivores').append(c)
        core.memory('agents').append(c)

    for i in range(data["superpredateurs"]["nb"]):
        c = Superpredateur(SuperpredateurBody())
        adaptToParameters(c, data["superpredateurs"]["parametres"])
        core.memory('superpredateurs').append(c)
        core.memory('agents').append(c)
    for i in range(data["decomposeurs"]["nb"]):
        c = Decomposeur(DecomposeurBody())
        adaptToParameters(c, data["decomposeurs"]["parametres"])
        core.memory('decomposeurs').append(c)
        core.memory('agents').append(c)

    for i in range(data["vegetaux"]["nb"]):
        core.memory("vegetaux").append(Vegetal())

    for i in range(data["cadavres"]["nb"]):
        core.memory("cadavres").append(Cadavre(Vector2(0,0)))

    core.memory("respawnPerFrame", float(data["vegetaux"]["respawnPerFrame"]))



def adaptToParameters(agent, data):
    for element in data:
        value = 0
        if len(data[element]) == 2:
            value = random.random()*(float(data[element][1])-float(data[element][0])) + float(data[element][0])

        if hasattr(agent.body, element):
            agent.body.__setattr__(element, value)

def computePerception(agent):
    fustrum = agent.body.furstrum
    fustrum.perceptionList = []
    for b in core.memory('agents'):
        if agent.uuid!=b.uuid:
            if fustrum.inside(b.body):
                fustrum.perceptionList.append(b.body)
    for i in core.memory('vegetaux'):
        if fustrum.inside(i):
            fustrum.perceptionList.append(i)
    for i in core.memory('cadavres'):
        if fustrum.inside(i):
            fustrum.perceptionList.append(i)
def computeDecision(agent):
    for a in core.memory('agents'):
        a.update()


def applyDecision(agent):
    for a in core.memory('agents'):
        a.body.update()


def updateEnv():
    for typeAgent in core.memory("typesAgents"):
        agents = core.memory(typeAgent)
        if len(agents)>0:
            typeTarget = agents[0].body.targets[0]
            leaveBodies = True
            if typeTarget=="cadavres":
                leaveBodies = False
            updateEat(typeAgent, typeTarget, leaveBodies)

        updateDeath(typeAgent)
        updateDedoublement(typeAgent)
    respawns = core.memory("respawns")
    respawns += core.memory("respawnPerFrame")
    for i in range(int(respawns)):
        core.memory("vegetaux").append(Vegetal())
    respawns %= 1
    core.memory("respawns", respawns)




def reset():
    core.memory("agents", [])
    for i in range(0, 5):
        core.memory('agents').append(Agent(Body()))

def updateEat(eaters, eaten, leaveBodies):
    for eater in core.memory(eaters):
        if not eater.body.wantToEat:
            continue
        for eaten_el in core.memory(eaten):
            position_target = 0
            mass_target = 0
            if hasattr(eaten_el, "body"):
                position_target = eaten_el.body.position
                mass_target = eaten_el.body.size
            elif hasattr(eaten_el, "position"):
                position_target = eaten_el.position
                mass_target = eaten_el.mass

            if position_target.distance_to(eater.body.position) <= eater.body.size + mass_target:
                eater.body.eat(mass_target)
                core.memory(eaten).remove(eaten_el)
                if hasattr(eaten_el, "body"):
                    core.memory("agents").remove(eaten_el)
                if not leaveBodies: return

                cadavre = Cadavre(position_target)
                core.memory("cadavres").append(cadavre)

def call_debug():
    print("debug")
def updateDeath(typeagent):
    for agent in core.memory(typeagent):
        if not agent.body.dead:
            continue
        cadavre = Cadavre(agent.body.position)
        core.memory("cadavres").append(cadavre)
        core.memory(typeagent).remove(agent)
        core.memory("agents").remove(agent)
        continue

def updateDedoublement(typeagent):
    for agent in core.memory(typeagent):
        if agent.body.aDedoubler:
            newHer = agent.dedoubler()
            core.memory(typeagent).append(newHer)
            core.memory("agents").append(newHer)



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
    statsPopulation()




core.main(setup, run)