import pygame as pg
import pymunk as pm
from pymunk.vec2d import Vec2d
from physics import CelestialBody
from graphics.explosion import Explosion
import functools
import math
from graphics.zoom import Zoom


class Drawer:
    """
    Static class for drawing game components to pygame
    """

    #: Maximum zoom level, 8x normal zoom
    _maxZoom = 8

    #: Minimum zoom level, (2^-16)x normal zoom
    _minZoom = 2**-16

    #: :class:`Zoom` object for handling current zoom level
    zoom = Zoom()

    @classmethod
    def draw(cls, screen, toDraw, offset):
        """
        Draws an object to the screen

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param toDraw: Object to draw
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """

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
        """
        Calls :py:meth:`.draw` on a list of drawable objects

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param toDraw: list of drawable objects
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """
    
        for shape in list:
            Drawer.draw(screen, shape, offset)

    @classmethod
    def drawPoly(cls, screen, shape, offset):
        """
        Draws a :py:class:`pymunk.Poly` object

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param shape: `Poly` object to draw
        :type shape: :py:class:`pymunk.Poly`
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """

        newVerts = []
        max = Vec2d(screen.get_size())
        for v in shape.get_vertices():
            # Get pymunk global coordinates
            newV = (v.rotated(shape.body.angle) + shape.body.position + offset)*cls.zoom.zoom
            newVerts.append([cls.intVec2d(newV)[0],
                             max[1]-(cls.intVec2d(newV)[1])])
        isOnScreen = functools.reduce(lambda x, y: x or Drawer.inRange(max, y),
                                      newVerts, False)
        if isOnScreen:
            pg.draw.polygon(screen, pg.Color('blue'), newVerts)

    @classmethod
    def drawCircle(cls, screen, shape, offset):
        """
        Draws a :py:class:`pymunk.Circle` object

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param shape: `Circle` object to draw
        :type shape: :py:class:`pymunk.Circle`
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """
        r = shape.radius*cls.zoom.zoom
        pos = cls.to_pygame(shape, Vec2d(0, 0), offset)
        max = Vec2d(screen.get_size())

        # find the center of the screen (1/2 screen diagonal)
        center = cls.intVec2d(max/(2*cls.zoom.zoom))

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
        """
        Draws a :py:class:`...physics.CelestialBody` object

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param cb: `CelestialBody` object to draw
        :type cb: :py:class:`..physics.CelestialBody`
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """
        pos = cls.zoom.zoom*(cb.body.position + offset)
        screenSize = Vec2d(screen.get_size())
        screenCenter = cls.intVec2d(screenSize/(2*cls.zoom.zoom))
        isOnScreen = pos.get_distance(screenCenter) \
                     <= (cb.radius*cls.zoom.zoom + screenCenter.get_length())
        if isOnScreen:
            if cls.zoom.zoom < 2.0**-4:
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
        """
        Draws a :py:class:`..Explosion` object

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param sprite: Explosion object to draw
        :type sprite: :py:class:`..Explosion`
        :param (int,int) position: Position in pymunk coordinates to draw the explosion
        :param (int,int) size: Size of explosion
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        """
        position = cls.zoom.zoom*(offset + position - cls.intVec2d((size[0]/2, size[1]/2)))
        size = cls.intVec2d(Vec2d(size)*cls.zoom.zoom)
        explosionSprite = sprite.get_draw()
        if explosionSprite is None:
            return
        scaledSprite = pg.transform.smoothscale(explosionSprite, size)

        screen.blit(scaledSprite, tuple(position))

    @classmethod
    def drawSprite(cls, screen, component, offset):
        """
        Draws a :py:class:`...rockets.component` object

        :param screen: Pygame surface to draw to
        :type screen: :py:class:`pygame.Surface`
        :param shape: `Component` object to draw
        :type shape: :py:class:`...rockets.Component`
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d` 
        """
        pos = cls.to_pygame(component, Vec2d(0, 0), offset)
        screenSize = Vec2d(screen.get_size())

        isOnScreen = cls.inRange(screenSize, pos)

        if isOnScreen:
            # translate the sprite to be the same size as the component...
            verts = component.get_vertices()
            minX, maxX, minY, maxY = cls.getXYMinMax(verts)

            # find the center of the geometry, and rotate it
            if component.body is not None:
                center = cls.zoom.zoom*Vec2d((maxX+minX)/2, (maxY+minY)/2).rotated(component.body.angle)
            else:
                center = cls.zoom.zoom*Vec2d((maxX+minX)/2, (maxY+minY)/2)
            # finds the bounding box for the geometry, and transforms the
            # sprite to fit within the geometry
            scaledSprite = pg.transform.scale(component.sprite,
                                              (int(maxX-minX), int(maxY-minY)))

            if component.body is not None:
                rotSprite = pg.transform.rotozoom(scaledSprite, math.degrees(component.body.angle), cls.zoom.zoom)
            else:
                rotSprite = pg.transform.rotozoom(scaledSprite, 0, cls.zoom.zoom)

            # the position we draw the sprite at will be the
            # position of the rocket,
            drawX = int(pos[0] + center[0] - rotSprite.get_width()/2)
            drawY = int(pos[1] - center[1] - rotSprite.get_height()/2)

            screen.blit(rotSprite, (drawX, drawY))

    @classmethod
    def getXYMinMax(cls, vertices):
        """
        Helper function to get size for scaled sprite for :py:meth:`.drawSprite`

        :param [(float,float)] vertices: List of component vertices
        :returns: Tuple of (minX, maxX, minY, maxY)
        :rtype: (int, int, int, int)
        """
        Xs = list(map(lambda x: x[0], vertices))
        Ys = list(map(lambda y: y[1], vertices))
        minX = min(Xs)
        maxX = max(Xs)
        minY = min(Ys)
        maxY = max(Ys)

        return (minX, maxX, minY, maxY)
    
    @classmethod
    def scaleSpriteToVerts(cls, sprite, vertices):
        """
        Helper function to scaled sprite for :py:meth:`.drawSprite`

        :param sprite: Sprite image to draw
        :type sprite: :py:class:`pygame.Surface` 
        :param [(float,float)] vertices: List of component vertices
        :returns: Scaled sprite image
        :rtype: :py:class:`pygame.Surface`
        """
        minX, maxX, minY, maxY = cls.getXYMinMax(vertices)
        return pg.transform.scale(sprite, (int(maxX - minX), int(maxY - minY)))

    @classmethod
    def drawBackground(cls, closestBody, altitude):
        """
        Draws the planetary atmosphere of the closest body to the rocket based on altitude.

        :param closestBody: :py:class:`CelestialBody` closest to the rocket
        :type closestBody: :py:class:`...physics.CelestialBody`
        :param float altitude: Height of the rocket above `closestBody`
        """

        atmColor = closestBody.atmosphereColor

        if atmColor is not None and altitude < closestBody.atmosphereHeight:
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
        """
        Calculates the offset between pymunk and pygame coordinates such that the rocket is rendered in the center of the screen.

        :param screen: Current display surface
        :type screen: :py:class:`pygame.Surface` 
        :param rocket: Rocket to place in the center of the screen
        :type rocket: :py:class:`...rockets.Rocket`
        :returns: Offset to add to pymunk coordinates
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """

        position = rocket.position
        centerOfScreen = cls.intVec2d(Vec2d(screen.get_size())/(2*cls.zoom.zoom))
        return cls.intVec2d(centerOfScreen - position)

    @classmethod
    def to_pygame(cls, shape, coords, offset):
        """
        Convert local pymunk shape coordinates to pygame if shape is not :py:type:`None`, else convert global pymunk coordinates to pygame.

        :param shape: Shape local coordinates are in reference to
        :type shape: :py:class:`pymunk.Shape`
        :param coords: Coordinates to convert
        :type coords: :py:class:`pymunk.vec2d.Vec2d`
        :param offset: Offset bewteen pymunk and pygame coordinates
        :type offset: :py:class:`pymunk.vec2d.Vec2d`
        :returns: Coordinates converted to pygame
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """

        if shape is None:
            return cls.intVec2d(cls.zoom.zoom*Vec2d(coords + offset))
        result = cls.zoom.zoom*Vec2d(coords.rotated(shape.body.angle)
                                            + shape.body.position
                                            + offset)
        return cls.intVec2d(result)

    @classmethod
    def intVec2d(cls, v, func=int):
        """
        Helper function that applies function to each element of `v`. Default function is :py:func:`int`.

        :param v: `Vec2d` to apply function to
        :type v: :py:class:`pymunk.vec2d.Vec2d`
        :param func: Function to apply to elements of `v`
        :type func: :py:class:`types.FunctionType`
        :returns: Vector `v` after function application
        :rtype: :py:class:`pymunk.vec2d.Vec2d`
        """

        return Vec2d(func(v[0]), func(v[1]))

    @classmethod
    def inRange(cls, max, coords):
        """
        Helper function that checks if coordinates are between (0,0) and `max`.

        :param max: `Vec2d` of maximum coordinates
        :type v: :py:class:`pymunk.vec2d.Vec2d`
        :param max: `Vec2d` of coordinates to check
        :type v: :py:class:`pymunk.vec2d.Vec2d`
        :returns: `True` if `coords` is in range, `False` otherwise.
        :rtype: bool
        """

        return (0 <= coords[0] <= max[0]) and (0 <= coords[1] <= max[1])
