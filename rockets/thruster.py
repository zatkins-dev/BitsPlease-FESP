from pymunk.vec2d import Vec2d

from rockets import *
from pymunk import Body as Body
import pygame as pg
import os
from abc import ABC, abstractmethod
from . import _ASSETS_PATH


class Thruster(Component):
    """
    Thruster Interface for creation of thrusters. Individual named
    thrusters inherit from and implement this class. Most of the implementation
    is already done within this interface, with key parts left out for the 
    subclasses to make their own.
    """

    def __init__(self, body, transform=None, radius=0):
        """
        Constructor for a Thruster. The important things done in this constructor include
        creating the Component base using the vertices defined in the getInfo method, and 
        setting the density and initial fuel of the thruster also using values from the 
        getInfo method.

        :param pymunk.Body body: The body to attatch this thruster to.
        :param pymunk.Transform transform: The transform to apply to the Thruster on creation.
        :param float radius: The radius to give to the Thruster's corners.
        """
        Component.__init__(self, body, self.getInfo()["vertices"], self.getInfo()["density"], transform, radius)

        self.fuel = self.getInfo()["maxFuel"]

    @property
    def vertices(self):
        """
        The vertices of this specific type of thruster. This returns the value defined in
        the getInfo method.
        """
        return self.getInfo()["vertices"]

    @property
    def thrustForce(self):
        """
        The magnitude of the thrust of this specific type of thruster. This returns the value
        defined in the getInfo method.
        """
        return self.getInfo()["thrustForce"]

    
    @property
    def thrustVector(self):
        """
        The direction that the thruster will apply thrust. This returns the value defined
        in the getInfo method.
        """
        return self.getInfo()["thrustVector"]

    @property
    def sprite(self):
        """
        The sprite to use to render the thruster. This returns the value defined in the getInfo method.
        """
        return self.getInfo()["sprite"]
    
    @property
    def maxFuel(self):
        """
        The maximum ammount of fuel that the thruster starts with. This returns the value
        defined in the getInfo method.
        """
        return self.getInfo()["maxFuel"]

    @property
    def fuel(self):
        """
        The current ammout of fuel that the thruster has. Cannot be set below zero.
        """
        return self._fuel

    @fuel.setter
    def fuel(self, newFuel):
        if newFuel >= 0:
            self._fuel = newFuel
        else:
            self._fuel = 0

    def thrust(self):
        """
        Returns the scaled thrust vector of the Thruster.
        """
        return self.thrustForce * self.thrustVector

    def applyThrust(self, throttle, timescale):
        """
        Applies thrust to the rocket, scaling the thrust to a throttle value between 0 and 1. The 
        thrust provided and fuel consumed are then scaled by the provide timescale.

        :param float throttle: The ammount to throttle the thrust by, between 0 and 1
        :param float timescale: The ammount to scale the thrust provided and fuel consumed.
        """
        if self.fuel > 0 and 0 < throttle <= 1:
            self.body.apply_impulse_at_local_point(throttle * self.thrust() * timescale, (self.center_of_gravity.x, self.center_of_gravity.y))
            self.fuel -= 1 * throttle * timescale
    
    


    

    def reset(self):
        """
        Resets properties of the underlying component and the fuel of the thruster to restart the simulation
        """
        super().reset()
        self._fuel = self.maxFuel

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """
        This method is what will define the properties of a specific Thruster subclass.
        It should return a dictionary with the following values:

        +----------------+-------------------------------------------------+
        | Dictionary Key |              Dictionary Value Type              |
        +================+=================================================+
        |    vertices    |   (*List of* :py:class:`pymunk.vec2d.Vec2d`)    |
        +----------------+-------------------------------------------------+
        |   thrustForce  |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        |  thrustVector  |        (:py:class:`pymunk.vec2d.Vec2d`)         |
        +----------------+-------------------------------------------------+
        |                | (:py:class:`pygame.surface.Surface`) It is      |
        |     sprite     | advised this be stored as a class variable, and |
        |                | returned by this method to improve performance. |
        +----------------+-------------------------------------------------+
        |     maxFuel    |             (*float*) Should always be 0        |
        +----------------+-------------------------------------------------+
        |     density    |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        """
        pass

    @classmethod
    def getDisplayInfo(cls):
        """
        Returns a dictionary containing the "Thrust" and "Thrust Vector" of the rocket
        with units attatched for display to the screen or user.
        """
        inf = cls.getInfo()
        return {
            "Thrust": str(inf["thrustForce"]) + "N",
            "Thrust Vector": str(tuple(inf["thrustVector"])),
        }


class RCSThruster(Thruster):
    """
    An RCS Thruster is intended to be a smaller thruster, that pulls
    fuel from the rocket's SAS fuel instead of its own supply and is
    used for rotation instead of direct motion.
    """

    def __init__(self, body, transform=None, radius=0):
        """
        RCSThruster constructor. Initializes the underlying component and sets the 
        density of the thruster from the value defined in the getInfo method.

        :param pymunk.Body body: The body to attatch this thruster to.
        :param pymunk.Transform transform: The transform to apply to the Thruster on creation.
        :param float radius: The radius to give to the Thruster's corners.
        """
        Component.__init__(self, body, self.getInfo()["vertices"], self.getInfo()["density"], transform, radius)

        self.fuel = 0
    
    def applyThrust(self):
        """
        The RCSThruster applies thrust differently from normal Thrusters. The
        RCSThruster will check if there is an SAS module on the host Rocket
        that it can draw fuel from before it fires.
        """
        sasModule = None
        for module in self.body.SASmodules:
            if module.fuel > 0:
                sasModule = module
                break
        if sasModule is not None:
            self.body.apply_impulse_at_local_point(self.thrust(), (self.center_of_gravity.x, self.center_of_gravity.y))
            sasModule.fuel -= 1

    @classmethod
    @abstractmethod
    def getInfo(cls):
        """
        This method is what will define the properties of a specific RCSThruster subclass.
        It is identical to the Thruster getInfo, but the maxFuel member is always 0.

        +----------------+-------------------------------------------------+
        | Dictionary Key |              Dictionary Value Type              |
        +================+=================================================+
        |    vertices    |   (*List of* :py:class:`pymunk.vec2d.Vec2d`)    |
        +----------------+-------------------------------------------------+
        |   thrustForce  |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        |  thrustVector  |        (:py:class:`pymunk.vec2d.Vec2d`)         |
        +----------------+-------------------------------------------------+
        |                | (:py:class:`pygame.surface.Surface`) It is      |
        |     sprite     | advised this be stored as a class variable, and |
        |                | returned by this method to improve performance. |
        +----------------+-------------------------------------------------+
        |     maxFuel    |          (*float*) Should always be 0           |
        +----------------+-------------------------------------------------+
        |     density    |                    (*float*)                    |
        +----------------+-------------------------------------------------+
        """
        pass

class LeftRCS(RCSThruster):
    """
    LeftRCS Thrusters will all share these properties:

    +----------------+--------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                           |
    +================+==============================================================================================================+
    |    vertices    | [(0, 37), (5, 37), (5, 42), (0, 42)]                                                                         |        
    +----------------+--------------------------------------------------------------------------------------------------------------+
    |   thrustForce  | 5000.0                                                                                                       |
    +----------------+--------------------------------------------------------------------------------------------------------------+
    |  thrustVector  | (-1, 0)                                                                                                      |
    +----------------+--------------------------------------------------------------------------------------------------------------+
    |     sprite     | `RCSLeft.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/RCSLeft.png>`_ |
    +----------------+--------------------------------------------------------------------------------------------------------------+
    |     maxFuel    | 0.0                                                                                                          |
    +----------------+--------------------------------------------------------------------------------------------------------------+
    |     density    | 45.0                                                                                                         |
    +----------------+--------------------------------------------------------------------------------------------------------------+
    """

    #: Holds the thruster sprite to prevent repeated loading. Sprite is 
    #: `RCSLeft.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/RCSLeft.png>`_
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "RCSLeft.png")).convert_alpha()

    @classmethod
    def getInfo(cls):
        """
        Returns the dictionary with info specified by Thruster.getInfo()
        """

        return {
            "vertices":     [(0, 37), (5, 37), (5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((-1, 0)),
            "sprite":       cls._sprite,
            "maxFuel":      0,
            "density":      45
        }

class RightRCS(RCSThruster):
    """
    RightRCS Thrusters will all share these properties:

    +----------------+----------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                             |
    +================+================================================================================================================+
    |    vertices    | [(0, 37), (-5, 37), (-5, 42), (0, 42)]                                                                         |        
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |   thrustForce  | 5000.0                                                                                                         |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |  thrustVector  | (1, 0)                                                                                                         |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     sprite     | `RCSRight.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/RCSRight.png>`_ |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     maxFuel    | 0.0                                                                                                            |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     density    | 45.0                                                                                                           |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    """

    #: Holds the thruster sprite to prevent repeated loading. Sprite is 
    #: `RCSRight.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/RCSRight.png>`_
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "RCSRight.png")).convert_alpha()

    @classmethod
    def getInfo(cls):
        """
        Returns the dictionary with info specified by Thruster.getInfo()
        """

        return {
            "vertices":     [(0, 37), (-5, 37), (-5, 42), (0, 42)],
            "thrustForce":  5000,
            "thrustVector": Vec2d((1, 0)),
            "sprite":       cls._sprite,
            "maxFuel":      0,
            "density":      45
        }

class UpGoer2000(Thruster):
    """
    UpGoer2000 Thrusters will all share these properties:

    +----------------+--------------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                                 |
    +================+====================================================================================================================+
    |    vertices    | [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)]                                                                   |        
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    |   thrustForce  | 50,000.0                                                                                                           |
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    |  thrustVector  | (1, 0)                                                                                                             |
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    |     sprite     | `UpGoer2000.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/UpGoer2000.png>`_ |
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    |     maxFuel    | 10,000                                                                                                             |
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    |     density    | 73.8                                                                                                               |
    +----------------+--------------------------------------------------------------------------------------------------------------------+
    """
    
    #: Holds the thruster sprite to prevent repeated loading. Sprite is 
    #: `UpGoer2000.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/UpGoer2000.png>`_
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "UpGoer2000.png")).convert_alpha()

    @classmethod
    def getInfo(cls):
        """
        Returns the dictionary with info specified by Thruster.getInfo()
        """

        return {
            "vertices":     [(4.2, 0), (-4.2, 0), (4.2, 46.9), (-4.2, 46.9)],
            "thrustForce":  50000,
            "thrustVector": Vec2d((0,1)),
            "sprite":       cls._sprite,
            "maxFuel":      10000,
            "density":      73.8
        }
                
class DeltaVee(Thruster):
    """
    DeltaVee is the biggest, *baddest* Thruster and will all share these properties:

    +----------------+----------------------------------------------------------------------------------------------------------------+
    | Dictionary Key |              Dictionary Value Type                                                                             |
    +================+================================================================================================================+
    |    vertices    | [(12, 0), (-12, 0), (12, 70), (-12, 70)]                                                                       |        
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |   thrustForce  | 500000.0                                                                                                       |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |  thrustVector  | (1, 0)                                                                                                         |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     sprite     | `DeltaVee.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/DeltaVee.png>`_ |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     maxFuel    | 40,000                                                                                                         |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    |     density    | 73.8                                                                                                           |
    +----------------+----------------------------------------------------------------------------------------------------------------+
    """
    
    #: Holds the thruster sprite to prevent repeated loading. Sprite is 
    #: `DeltaVee.png <https://github.com/zatkins-school/BitsPlease-FESP/blob/project-4/assets/sprites/DeltaVee.png>`_
    _sprite = pg.image.load(os.path.join(_ASSETS_PATH, "sprites", "DeltaVee.png")).convert_alpha()

    @classmethod
    def getInfo(cls):
        """
        Returns the dictionary with info specified by Thruster.getInfo()
        """
        return {
            "vertices":     [(12, 0), (-12, 0), (12, 70), (-12, 70)],
            "thrustForce":  500000,
            "thrustVector": Vec2d((0,1)),
            "sprite":       cls._sprite,
            "maxFuel":      40000,
            "density":      73.8
        }



#class SolidThruster(Thruster):


class SandSquid(Thruster):
    _sprite = pg.image.load(os.path.join("assets", "sprites", "SandSquid.png"))
    
    def __init__(self, body, transform=None, radius=0):
       Thruster.__init__(self, body, transform=transform,  radius=radius)

    @classmethod
    def getInfo(cls):
        return {
            "vertices":     [(5, 0), (-5, 0), (-5, 5), (5, 5)],
            "thrustForce":  55000,
            "thrustVector": Vec2d((0,1)),
            "sprite":       cls._sprite,
            "maxFuel":      1,
            "density":      73.8,
            "Interior Crocodile Alligator": "I drive a Chevrolet Movie Theater"
        }

    def updateFuel(self):
        totalFuel = 0
        for x in self.body.Tanks:
            totalFuel = totalFuel + x.fuel
        self.fuel = totalFuel


    def applyThrust(self, throttle, timescale):
        if 0 < throttle <= 1:
            for x in self.body.Tanks:
                if x.fuel > 0:
                    self.body.apply_impulse_at_local_point(throttle * self.thrust() * timescale, (self.center_of_gravity.x, self.center_of_gravity.y))
                    x.fuel -= 1 * throttle * timescale
                    self.updateFuel
                    return
    

