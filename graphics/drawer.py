import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
from physics import CelestialBody
import functools
import math
import numpy
import pygame.surfarray


class Drawer:
    _maxZoom = 8
    _zoom = float(1)

    @classmethod
    def get_zoom(cls):
        return Drawer._zoom

    @classmethod
    def set_zoom(cls, zoom):
        Drawer._zoom = zoom

    zoom = property(get_zoom, set_zoom)

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
            print(rocket_pos)
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
                print("points", points)
                print("gradient, tangent, antitangent", normal, tangent, antitangent)
                flipY = lambda x, y_max: Vec2d(x[0],y_max-x[1])
                polyPoints = list(map(lambda p: flipY(cls.to_pygame(None, p, offset), screenSize[1]), points))
                print ("mapped points: ", polyPoints)
                pg.draw.polygon(screen, pg.Color("blue"), polyPoints)


            # viewVerts = [Vec2d(x,y) + screenCenter - offset for x in [-screenCenter[0], screenCenter[0]] for y in [-screenCenter[1], screenCenter[1]]]
            # segmentQueryInfos = []
            # for i in [0,3]:
            #     for j in [1,2]:
            #         queryInfo = bb.intersects_segment(viewVerts[i], viewVerts[j])
            #         if queryInfo.shape is not None:
            #             segmentQueryInfos.append(queryInfo)
            # print("gen'd verts", viewVerts)
            # print("segmentQueries: ", segmentQueryInfos)

            # if segmentQueryInfos == []:
            #     return
            # print("segment queries non-empty")
            # newPolyPoints = list(map(lambda p: cls.to_pygame(None, p.point, offset), segmentQueryInfos))
            # print("mapped query points to pg: ", newPolyPoints)
            # for vert in viewVerts:
            #     if cb.shape.point_query(vert)[0] < 0:
            #         newPolyPoints.append(cls.to_pygame(None, vert, offset))
            #         print("added xtra point: ", cls.to_pygame(None, vert, offset))
            # pg.draw.polygon(screen, pg.Color("blue"), newPolyPoints)
            # print("drawing circle")
            # # get relevant sprite area
            # # topleft = -cls.intVec2d(cls.pymunk_to_surface(scaleFactor,
            # #                                              sprite_surf,
            # #                                              -offset-screenCenter,
            # #                                              cb.body.position))
            # flipY = lambda x, y_max: Vec2d(x[0],x[1]-y_max)
            # zero_pm = cb.body.position - cb.radius*Vec2d(1,1)
            # topleft_pm = -offset
            # topleft = cls.intVec2d(flipY((topleft_pm - zero_pm) / scaleFactor, y), func=math.ceil)
            # print ("zero_pm: {0}\ntopleft_pm: {1}".format(zero_pm, topleft_pm))
            
            # size_s = cls.intVec2d(screenSize / (cls._zoom * scaleFactor), func=math.ceil)

            # size_s[0] = max([0, size_s[0]])
            # size_s[0] = min([size_s[0], x])

            # size_s[1] = max([0, size_s[1]])
            # size_s[1] = min([size_s[1], y])

            # viewRect = pg.Rect(tuple(topleft),tuple(size_s))
            # viewRect = image_rect.clip(viewRect)
            # if viewRect == pg.Rect(0,0,0,0):
            #     return
            # print ("topleft_sp: {0}".format(topleft))
            # print ("size_sp: {0}".format(size_s))
            # print ("viewRect: {0}".format(viewRect))
            # subsprite = image.subsurface(viewRect).copy()

            # scaledSize = cls.intVec2d(scaleFactor*cls._zoom*size_s)
            # print ("scaled size: {0}".format(scaledSize))
            # # scale sprite image to be the right size
            # scaledSprite = pg.transform.rotozoom(subsprite, 0, scaleFactor*cls._zoom)
            # blit_pos_y = screenSize[1] - scaledSize[1]
            # screen.blit(scaledSprite, (0, blit_pos_y))

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
            center = cls._zoom*Vec2d((maxX+minX)/2, (maxY+minY)/2).rotated(component.body.angle)

            # finds the bounding box for the geometry, and transforms the
            # sprite to fit within the geometry
            scaledSprite = pg.transform.scale(component.sprite,
                                              (int(maxX-minX), int(maxY-minY)))

            # now rotate the sprited
            rotSprite = pg.transform.rotozoom(scaledSprite, math.degrees(component.body.angle), cls._zoom)

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
    def getOffset(cls, screen, rocket):
        position = rocket.position
        centerOfScreen = cls.intVec2d(Vec2d(screen.get_size())/(2*cls._zoom))
        return cls.intVec2d(centerOfScreen - position)

    @classmethod
    def to_pygame(cls, shape, coords, offset):
        if shape is None:
            return cls.intVec2d(cls._zoom*Vec2d(coords + offset))
        return cls.intVec2d(cls._zoom*Vec2d(coords.rotated(shape.body.angle)
                                            + shape.body.position
                                            + offset))

    @classmethod
    def surface_to_pymunk(cls, scaleFactor, surface, coords, position_offset):
        return scaleFactor*(Vec2d(coords) - Vec2d(surface.get_size()).rotated(math.pi)/2) + Vec2d(position_offset)

    @classmethod
    def pymunk_to_surface(cls, scaleFactor, surface, coords, position_offset):
        return (Vec2d(coords) - Vec2d(position_offset))/scaleFactor \
                + Vec2d(surface.get_size()).rotated(math.pi)/2

    @classmethod
    def intVec2d(cls, v, func=int):
        return Vec2d(func(v[0]), func(v[1]))

    @classmethod
    def inRange(cls, max, coords):
        return (0 <= coords[0] <= max[0]) and (0 <= coords[1] <= max[1])