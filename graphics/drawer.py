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

        # find the center of the screen (1/2 screen diagonal)
        centerOfScreen = cls.intVec2d(Vec2d(screen.get_size())/2)
        # find the rocket position in pymunk space
        rocketPos = -1 * (offset - centerOfScreen)

        # check for farthest possible distance where we could see the planet:
        #       1/2 screen diagonal + r = distance from circle
        # as long as the distance is less than this, we should draw the circle
        isOnScreen = rocketPos.get_distance(shape.body.position) < r + centerOfScreen.get_length()

        if isOnScreen:
            pos = cls.intVec2d(pos)
            pg.draw.circle(screen, pg.Color('blue'), [pos[0], max[1]-pos[1]], int(r))

    @classmethod
    def drawSprite(cls, screen, component, offset):
        pos = cls.intVec2d(component.body.position + offset)
        screenSize = Vec2d(screen.get_size())

        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(screenSize, y),
                                      [pos], False)

        if isOnScreen:
            # translate the sprite to be the same size as the component...
            verts = component.get_vertices()
            Xs = list(map(lambda x: x[0], verts))
            Ys = list(map(lambda y: y[1], verts))
            minX = min(Xs)
            maxX = max(Xs)
            minY = min(Ys)
            maxY = max(Ys)

            # find the center of the geometry, and rotate it
            center = Vec2d((maxX+minX)/2, (maxY+minY)/2).rotated(component.body.angle)
            
            # finds the bounding box for the geometry, and transforms the sprite to fit within the geometry
            scaledSprite = pg.transform.scale(component.sprite, (int(maxX-minX), int(maxY-minY)))

            # now rotate the sprite
            rotSprite = pg.transform.rotozoom(scaledSprite, math.degrees(component.body.angle), 1)

            # the position we draw the sprite at will be the position of the rocket, 
            drawX = pos[0] + center[0] - rotSprite.get_width()/2
            drawY = pos[1] - center[1] - rotSprite.get_height()/2

            screen.blit(rotSprite, (drawX, drawY))

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
