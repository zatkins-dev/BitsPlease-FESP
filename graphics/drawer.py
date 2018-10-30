import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
import functools
import math


class Drawer:
    @classmethod
    def draw(cls, screen, toDraw, offset):
        if hasattr(toDraw, 'sprite') and toDraw.sprite != None:
            Drawer.drawSprite(screen, toDraw, offset)
        elif isinstance(toDraw, pm.Poly):
            Drawer.drawPoly(screen, toDraw, offset)
        elif isinstance(toDraw, pm.Circle):
            Drawer.drawCircle(screen, toDraw, offset)

    @classmethod
    def drawMultiple(cls, screen, list, offset):
        for shape in list:
            Drawer.draw(screen, shape, offset)

    @classmethod
    def drawPoly(cls, screen, shape, offset):
        newVerts = []
        max = screen.get_size()
        for v in shape.get_vertices():
            # Get pymunk global coordinates
            newV = v.rotated(shape.body.angle) + shape.body.position + offset
            newVerts.append([cls.intVec2d(newV)[0],
                             max[1]-(cls.intVec2d(newV)[1])])
        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(max, y),
                                      newVerts, False)
        if isOnScreen:
            pg.draw.polygon(screen, pg.Color('blue'), newVerts)

    @classmethod
    def drawCircle(cls, screen, shape, offset):
        r = shape.radius
        pos = cls.intVec2d(shape.body.position + offset)
        max = Vec2d(screen.get_size())
        # TODO: check this in a less naive way
        verts = [pos + (r*a, r*b) for a in [-1, 0, 1] for b in [-1, 0, 1]]
        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(max, y),
                                      verts, False)

        if isOnScreen:
            pos = cls.intVec2d(pos)
            pg.draw.circle(screen, pg.Color('blue'), [pos[0], max[1]-pos[1]], int(r))

    @classmethod
    def drawSprite(cls, screen, component, offset):
        pos = cls.intVec2d(component.body.position + offset)
        max = Vec2d(screen.get_size())

        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(max, y),
                                      [pos], False)

        if isOnScreen:
            newSprite = pg.transform.rotozoom(component.sprite, math.degrees(component.body.angle), 1)

            screen.blit(newSprite, (pos[0] - newSprite.get_width()/2, max[1] - pos[1] - newSprite.get_height()/2))

    @classmethod
    def getOffset(cls, screen, rocket):
        position = rocket.position
        centerOfScreen = cls.intVec2d(Vec2d(screen.get_size())/2)
        return centerOfScreen - position

    @classmethod
    def to_pygame(cls, shape, coords, offset):
        return tuple(coords.rotated(shape.body.angle)
                     + shape.body.position
                     + offset)

    @classmethod
    def intVec2d(cls, v):
        return Vec2d(int(v[0]), int(v[1]))

    @classmethod
    def inRange(cls, max, coords):
        return (0 <= coords[0] <= max[0]) and (0 <= coords[1] <= max[1])
