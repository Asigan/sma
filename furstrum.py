from pygame import Vector2

import core
from toolbox_tore import draw_circle_in_tore


class Fustrum(object):
    def __init__(self,r,parent):
        self.radius=r
        self.parent=parent
        self.perceptionList=[]
        self.inTore = False

    def inside(self,obj):
        if hasattr(obj,'position'):
            sizeobj = 0

            if hasattr(obj,"size"):
                sizeobj = obj.size
            elif hasattr(obj, "mass"):
                sizeobj = obj.mass
            if obj.position.distance_to(self.parent.position) < self.radius+sizeobj:
                return True
            if self.inTore:
                addVector = Vector2(0, 0)
                coeff = 1
                if obj.position.length() < self.parent.position.length(): coeff=-1
                addVector = coeff*Vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
                if obj.position.distance_to(self.parent.position+addVector) < self.radius+sizeobj:
                    return True
        return False

    def show(self):
        core.Draw.circle((255,255,0), self.parent.position, self.radius, width=1)