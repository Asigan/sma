import core
from pygame import Vector2


def draw_line_in_tore(position1, position2, color=(255,255,255)):
    newPos = closest_position_in_tore(position1, position2)
    v = Vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
    newPos1 = Vector2(position1.x, position1.y)
    core.Draw.line(color, position1, newPos, 1)
    if newPos.x > v.x:
        newPos.x = newPos.x - v.x
        newPos1.x = newPos1.x - v.x
    elif newPos.x < 0:
        newPos.x = newPos.x + v.x
        newPos1.x = newPos1.x + v.x
    if newPos.y > v.y:
        newPos.y = newPos.y + v.y
        newPos1.y = newPos1.y + v.y
    elif newPos.y < 0:
        newPos.y = newPos.y + v.y
        newPos1.y = newPos1.y + v.y
    core.Draw.line(color, newPos1, newPos, 1)

def draw_circle_in_tore(center, radius, width=1, color=(255,255,255)):
    core.Draw.circle(color, center, radius, width)
    newCenter = Vector2(center.x, center.y)
    v = Vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
    if newCenter.x+radius > v.x:
        newCenter.x = newCenter.x - v.x
    elif newCenter.x-radius < 0:
        newCenter.x = newCenter.x + v.x
    if newCenter.y+radius > v.y:
        newCenter.y = newCenter.y - v.y
    elif newCenter.y - radius < 0:
        newCenter.y = newCenter.y + v.y
    core.Draw.circle(color, newCenter, radius, width)


def shortest_distance_in_tore(pos1, obj_pos):
    return pos1.distance_to(closest_position_in_tore(pos1, obj_pos))


def closest_position_in_tore(pos1, obj_pos):
    v = Vector2(core.WINDOW_SIZE[0], core.WINDOW_SIZE[1])
    positions = [obj_pos,
                 obj_pos+v,
                 obj_pos-v,
                 Vector2(obj_pos.x+v.x, obj_pos.y),
                 Vector2(obj_pos.x, obj_pos.y + v.y),
                 Vector2(obj_pos.x - v.x, obj_pos.y),
                 Vector2(obj_pos.x, obj_pos.y - v.y)
                 ]
    shortest = 0
    for i in range(1, len(positions)):
        if pos1.distance_to(positions[i]) < pos1.distance_to(positions[shortest]):
            shortest = i
    return positions[shortest]
