import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
from physics import CelestialBody
from graphics.explosion import Explosion
import functools
import math


class Drawer:
    _maxZoom = 8
    _minZoom = 2**-16

    _zoom = float(1)

    @classmethod
    def reset_zoom(cls):
        cls._zoom = 1

    @classmethod
    def draw(cls, screen, toDraw, offset):
        if isinstance(toDraw, CelestialBody):
            Drawer.drawCelestialBody(screen, toDraw, offset)
        elif hasattr(toDraw, 'sprite') and toDraw.sprite is not None:
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
        max = Vec2d(screen.get_size())
        for v in shape.get_vertices():
            # Get pymunk global coordinates
            newV = (v.rotated(shape.body.angle) + shape.body.position + offset)*cls._zoom
            newVerts.append([cls.intVec2d(newV)[0],
                             max[1]-(cls.intVec2d(newV)[1])])
        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(max, y),
                                      newVerts, False)
        if isOnScreen:
            pg.draw.polygon(screen, pg.Color('blue'), newVerts)

    @classmethod
    def drawCircle(cls, screen, shape, offset):
        r = shape.radius*cls._zoom
        pos = cls.to_pygame(shape, Vec2d(0, 0), offset)
        max = Vec2d(screen.get_size())

        # find the center of the screen (1/2 screen diagonal)
        center = cls.intVec2d(max/(2*cls._zoom))

        # check for farthest possible distance where we could see the planet:
        #       1/2 screen diagonal + r = distance from circle
        # as long as the distance is less than this, we should draw the circle
        isOnScreen = pos.get_distance(center) <= (r + center.get_length())

        if isOnScreen:
            # print("drawing circle: ", (screen, pg.Color('blue'),[pos[0], max[1]-pos[1]], int(r)))
            pos = cls.intVec2d(pos)
            pg.draw.circle(screen, pg.Color('blue'),
                           [pos[0], max[1]-pos[1]], int(r))

    @classmethod
    def drawCelestialBody(cls, screen, cb, offset):
        pos = cls._zoom*(cb.body.position + offset)
        screenSize = Vec2d(screen.get_size())
        screenCenter = cls.intVec2d(screenSize/(2*cls._zoom))
        isOnScreen = pos.get_distance(screenCenter) \
                     <= (cb.radius*cls._zoom + screenCenter.get_length())
        if isOnScreen:
            if cls._zoom < 2.0**-4:
                cls.drawCircle(screen, cb.shape, offset)
                return

            rocket_pos = screenCenter - offset
            point_query = cb.shape.point_query(rocket_pos)
            if point_query[0] < screenCenter.length:
                # planet should appear
                closestPoint = point_query[1].point
                normal = point_query[1].gradient.rotated(math.pi)
                tangent = normal.rotated(math.pi/2)
                antitangent = normal.rotated(-math.pi/2)
                points = [closestPoint - screenCenter.length*(tangent),
                          closestPoint - screenCenter.length*(antitangent),
                          closestPoint - screenCenter.length*(antitangent - normal),
                          closestPoint - screenCenter.length*(tangent - normal)]
                flipY = lambda x, y_max: Vec2d(x[0],y_max-x[1])
                polyPoints = list(map(lambda p: flipY(cls.to_pygame(None, p, offset), screenSize[1]), points))
                pg.draw.polygon(screen, pg.Color("blue"), polyPoints)

    @classmethod
    def drawExplosion(cls, screen, sprite, position, size, offset):
        position = cls._zoom*(offset + position - cls.intVec2d((size[0]/2, size[1]/2)))
        size = cls.intVec2d(Vec2d(size)*cls._zoom)
        explosionSprite = sprite.get_draw()
        if explosionSprite is None:
            return
        scaledSprite = pg.transform.smoothscale(explosionSprite, size)

        screen.blit(scaledSprite, tuple(position))

    @classmethod
    def drawSprite(cls, screen, component, offset):
        pos = cls.to_pygame(component, Vec2d(0, 0), offset)
        screenSize = Vec2d(screen.get_size())

        isOnScreen = cls.inRange(screenSize, pos)

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
            if component.body is not None:
                center = cls._zoom*Vec2d((maxX+minX)/2, (maxY+minY)/2).rotated(component.body.angle)
            else:
                center = cls._zoom*Vec2d((maxX+minX)/2, (maxY+minY)/2)
            # finds the bounding box for the geometry, and transforms the
            # sprite to fit within the geometry
            scaledSprite = pg.transform.scale(component.sprite,
                                              (int(maxX-minX), int(maxY-minY)))
            # removed for better looking alternative
            # if component.destroyed:
            #     if cls.explode is None:
            #         cls.explode = Explosion()
            #     scaledSprite = pg.transform.smoothscale(cls.explode.image, (int(maxX-minX), int(maxY-minY)))
            #     rotSprite = pg.transform.rotozoom(scaledSprite, math.degrees(component.body.angle), cls._zoom)
            #     drawX = int(pos[0] + center[0] - rotSprite.get_width()/2)
            #     drawY = int(pos[1] - center[1] - rotSprite.get_height()/2)
            #     screen.blit(rotSprite, (drawX,drawY))
            #     cls.explode.update_frame()
            #     return
            # now rotate the sprited
            if component.body is not None:
                rotSprite = pg.transform.rotozoom(scaledSprite, math.degrees(component.body.angle), cls._zoom)
            else:
                rotSprite = pg.transform.rotozoom(scaledSprite, 0, cls._zoom)

            # the position we draw the sprite at will be the
            # position of the rocket,
            drawX = int(pos[0] + center[0] - rotSprite.get_width()/2)
            drawY = int(pos[1] - center[1] - rotSprite.get_height()/2)

            # zWidth = int(rotSprite.get_width()*cls._zoom)
            # zHeight = int(rotSprite.get_height()*cls._zoom)
            #
            # cls._zoomedSprite = pg.transform.smoothscale(rotSprite,
            #                                         (zWidth, zHeight))

            screen.blit(rotSprite, (drawX, drawY))

    @classmethod
    def drawBackground(cls, celestialBodies, rocket):
        # find the closest celestial body in the list, then draw its atmosphere color
        closestBody = min(celestialBodies, key=lambda x: (x.body.position - rocket.position).get_length())

        atmColor = closestBody.atmosphereColor

        if atmColor is not None:
            # find the distance from the surface of the body
            altitude = (closestBody.body.position - rocket.position).get_length() - closestBody.radius
            
            if altitude < closestBody.atmosphereHeight:
                # normalize the height to a 0-1 scale
                relHeight = (altitude / closestBody.atmosphereHeight)
                
                # find the opacity, in a quadratically decreasing fasion
                atmOpacity = -1*(relHeight)**2 + 1

                # check if the atmosphere color has an opacity, and combine with it
                if len(atmColor) is 4:
                    atmOpacity *= atmColor[3]

                # create a background surface, and blit the background over it
                surf = pg.display.get_surface()
                surfSize = surf.get_size()
                background = pg.Surface(surfSize)
                background.fill((atmColor[0], atmColor[1], atmColor[2]))
                background.set_alpha(int(255*atmOpacity))
                surf.blit(background, (0,0))


    @classmethod
    def getOffset(cls, screen, rocket):
        position = rocket.position
        centerOfScreen = cls.intVec2d(Vec2d(screen.get_size())/(2*cls._zoom))
        return cls.intVec2d(centerOfScreen - position)

    @classmethod
    def to_pygame(cls, shape, coords, offset):
        if shape is None:
            return cls.intVec2d(cls._zoom*Vec2d(coords + offset))
        result = cls._zoom*Vec2d(coords.rotated(shape.body.angle)
                                            + shape.body.position
                                            + offset)
        return cls.intVec2d(result)

    @classmethod
    def intVec2d(cls, v, func=int):
        return Vec2d(func(v[0]), func(v[1]))

    @classmethod
    def inRange(cls, max, coords):
        return (0 <= coords[0] <= max[0]) and (0 <= coords[1] <= max[1])
