import unittest
from graphics import Video, Zoom, Explosion, Drawer
Video.init()

from rockets.testrocket import genRocket
from rockets import Rocket, CommandModule, UpGoer2000, DeltaVee, SandSquid, AdvancedSAS, RightRCS, LeftRCS, TestTank
import pymunk as pm
import pygame as pg
from time import sleep
from physics import Physics, CelestialBody, TimeScale

import time

from audioManager import AudioManager

class RocketTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)

    def test_default_rocket(self):
        self.rocket = genRocket(self.space)

        # test if rocket was actually added to our space
        self.assertEqual(self.rocket.space, self.space)

        # test if the components were actually added to the rocket
        self.assertIs(self.rocket.components, self.baseComponents)

    def test_rocket_constructor(self):
        # test initial conditions... destroyed, saslock, etc.
        self.assertFalse(self.rocket.destroyed)
        self.assertFalse(self.rocket.isAngleLocked)
        self.assertEqual(self.rocket.throttle, 0)

        # test that the component lists are the same
        self.assertCountEqual(self.rocket.components, self.baseComponents)

        # test that components bodies were made to be the rocket
        for component in self.rocket.components:
            self.assertIs(component.body, self.rocket)


    def test_append_component(self):
        self.newTank = TestTank(self.rocket)
        self.rocket.addComponent(self.newTank)
        self.assertIn(self.newTank, self.rocket.components)
        self.tearDown()

    def test_lists(self):
        self.c1 = UpGoer2000(self.rocket)
        self.rocket.addComponent(self.c1)
        self.assertIn(self.c1, self.rocket.components)
        self.assertIn(self.c1, self.rocket.thrusters)
        self.assertNotIn(self.c1, self.rocket.SASmodules)
        self.assertNotIn(self.c1, self.rocket.RCSThrusters)
        self.assertNotIn(self.c1, self.rocket.tanks)

        self.c2 = DeltaVee(self.rocket)
        self.rocket.addComponent(self.c2)
        self.assertIn(self.c2, self.rocket.components)
        self.assertIn(self.c2, self.rocket.thrusters)
        self.assertNotIn(self.c2, self.rocket.SASmodules)
        self.assertNotIn(self.c2, self.rocket.RCSThrusters)
        self.assertNotIn(self.c2, self.rocket.tanks)

        self.c3 = SandSquid(self.rocket)
        self.rocket.addComponent(self.c3)
        self.assertIn(self.c3, self.rocket.components)
        self.assertIn(self.c3, self.rocket.thrusters)
        self.assertNotIn(self.c3, self.rocket.SASmodules)
        self.assertNotIn(self.c3, self.rocket.RCSThrusters)
        self.assertNotIn(self.c3, self.rocket.tanks)

        self.c4 = RightRCS(self.rocket)
        self.rocket.addComponent(self.c4)
        self.assertIn(self.c4, self.rocket.components)
        self.assertNotIn(self.c4, self.rocket.thrusters)
        self.assertNotIn(self.c4, self.rocket.SASmodules)
        self.assertIn(self.c4, self.rocket.RCSThrusters)
        self.assertNotIn(self.c4, self.rocket.tanks)

        self.c5 = LeftRCS(self.rocket)
        self.rocket.addComponent(self.c5)
        self.assertIn(self.c5, self.rocket.components)
        self.assertNotIn(self.c5, self.rocket.thrusters)
        self.assertNotIn(self.c5, self.rocket.SASmodules)
        self.assertIn(self.c5, self.rocket.RCSThrusters)
        self.assertNotIn(self.c5, self.rocket.tanks)

        self.c6 = AdvancedSAS(self.rocket)
        self.rocket.addComponent(self.c6)
        self.assertIn(self.c6, self.rocket.components)
        self.assertNotIn(self.c6, self.rocket.thrusters)
        self.assertIn(self.c6, self.rocket.SASmodules)
        self.assertNotIn(self.c6, self.rocket.RCSThrusters)
        self.assertNotIn(self.c6, self.rocket.tanks)

        self.c7 = TestTank(self.rocket)
        self.rocket.addComponent(self.c7)
        self.assertIn(self.c7, self.rocket.components)
        self.assertNotIn(self.c7, self.rocket.thrusters)
        self.assertNotIn(self.c7, self.rocket.SASmodules)
        self.assertNotIn(self.c7, self.rocket.RCSThrusters)
        self.assertIn(self.c7, self.rocket.tanks)

    def test_thruster_list(self):
        self.thruster1 = UpGoer2000(self.rocket)
        self.rocket.addComponent(self.thruster1)
        self.assertIn(self.thruster1, self.rocket.thrusters)

        self.thruster2 = DeltaVee(self.rocket)
        self.rocket.addComponent(self.thruster2)
        self.assertIn(self.thruster2, self.rocket.thrusters)

        self.thruster3 = SandSquid(self.rocket)
        self.rocket.addComponent(self.thruster3)
        self.assertIn(self.thruster3, self.rocket.thrusters)

        self.thruster4 = RightRCS(self.rocket)
        self.rocket.addComponent(self.thruster4)
        self.assertNotIn(self.thruster4, self.rocket.thrusters)

        self.thruster5 = LeftRCS(self.rocket)
        self.rocket.addComponent(self.thruster5)
        self.assertNotIn(self.thruster5, self.rocket.thrusters)

    def test_rocket_throttle_bounds(self):
        self.rocket.throttle = 99
        self.assertEqual(self.rocket.throttle, 1)
        self.rocket.throttle = -99
        self.assertEqual(self.rocket.throttle, 0)
        self.rocket.throttle = 0
        self.assertEqual(self.rocket.throttle, 0)
        self.rocket.throttle = 0.5
        self.assertEqual(self.rocket.throttle, 0.5)

    def test_rocket_angle_locking(self):
        self.rocket.isAngleLocked = True
        self.assertTrue(self.rocket.isAngleLocked)
        self.rocket.removeComponent(self.rocket.SASmodules[0])
        self.assertFalse(self.rocket.isAngleLocked)
        self.rocket.isAngleLocked = True
        self.assertFalse(self.rocket.isAngleLocked)

    def test_rocket_reset(self):
        self.newTank = TestTank(self.rocket)

        self.rocket.addComponent(self.newTank)
        self.rocket.throttle = 0.5
        self.rocket.isAngleLocked = True
        self.rocket.destroyed = True
        self.rocket.reset()
        self.assertFalse(self.rocket.destroyed)
        self.assertEqual(self.rocket.throttle, 0)
        self.assertFalse(self.rocket.isAngleLocked)

class SolidThrusterTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.thruster = UpGoer2000(None)
        self.rocket = Rocket([self.thruster])
        self.space.add(self.rocket)
        self.space.add(self.thruster)

    def test_solid_thruster_contructor(self):
        self.assertEqual(self.thruster.fuel, self.thruster.maxFuel)

    def test_fuel(self):
        self.thruster.fuel = 50
        self.assertEqual(self.thruster.fuel, 50)

        self.thruster.fuel = -100
        self.assertEqual(self.thruster.fuel, 0)

    def test_apply_thrust_fuel(self):
        throttle = 1
        timeScale = 1
        prevFuel = self.thruster.fuel
        self.thruster.applyThrust(throttle, timeScale)
        newFuel = self.thruster.fuel

        self.assertAlmostEqual(newFuel, prevFuel - throttle * timeScale)

        throttle = .5
        timeScale = 64
        prevFuel = self.thruster.fuel
        self.thruster.applyThrust(throttle, timeScale)
        newFuel = self.thruster.fuel

        self.assertAlmostEqual(newFuel, prevFuel - throttle * timeScale)

    def test_reset(self):
        self.assertEqual(self.thruster.fuel, self.thruster.maxFuel)

class LiquidThrusterTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.thruster = SandSquid(None)
        self.tanks = [TestTank(None), TestTank(None)]
        self.rocket = Rocket([self.thruster] + self.tanks)
        self.space.add(self.rocket)
        self.space.add(self.thruster)

    def test_apply_thrust_fuel(self):
        throttle = 1
        timeScale = 1
        prevFuel = self.thruster.fuel
        self.thruster.applyThrust(throttle, timeScale)
        newFuel = self.thruster.fuel

        self.assertAlmostEqual(newFuel, prevFuel - throttle * timeScale)

        throttle = .5
        timeScale = 64
        prevFuel = self.thruster.fuel
        self.thruster.applyThrust(throttle, timeScale)
        newFuel = self.thruster.fuel

        self.assertAlmostEqual(newFuel, prevFuel - throttle * timeScale)

class AudioTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.rocket = Rocket([])
        self.audioManager = AudioManager()
        self.audioManager.silenceMusic()
        self.audioManager.init()

    def test_SoundEffects_thursterDefault(self):
        #Test throttle at 0 + no thrusters - Should not play
        self.rocket.throttle = 0
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + no thrusters - Should not play
        self.rocket.throttle = 1
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterUpgoer(self):
        self.rocket.addComponent(UpGoer2000(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 0)

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterDeltaVee(self):
        self.rocket.addComponent(DeltaVee(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 0)

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterSandSquid(self):
        self.rocket.addComponent(SandSquid(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 0)

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        self.audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_SASDefault(self):
        #With no SAS, no sound should play both times
        self.rocket.isAngleLocked = False
        self.audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        self.rocket.isAngleLocked = True
        self.audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertTrue(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

    def test_SoundEffects_SASActive(self):
        self.rocket.addComponent(AdvancedSAS(self.rocket))

        #With SAS inactive, no sound should play
        self.rocket.isAngleLocked = False
        self.audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #With SAS active, sound should play
        self.rocket.isAngleLocked = True
        self.audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertTrue(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        self.audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())



class TankTestCase(unittest.TestCase):
#TANK TESTS
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)
        self.newTank = TestTank(self.rocket)
    def test_tank_fuel(self):
        self.newTank.fuel = -100
        self.assertEqual(self.newTank.fuel, 0)
        self.newTank.fuel = 100
        self.assertEqual(self.newTank.fuel, 100)

    def test_tank_reset(self):
        self.newTank.fuel = 0
        self.tank_capacity = self.newTank.capacity
        self.newTank.reset()
        self.assertEqual(self.tank_capacity, self.newTank.fuel)

class SASTestCase(unittest.TestCase):
#SAS TESTS
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)
        self.theSAS = self.rocket.SASmodules[0]

    def test_sas_fuel(self):
        self.theSAS.fuel = -100
        self.assertEqual(self.theSAS.fuel, 0)
        self.theSAS.fuel = 100
        self.assertEqual(self.theSAS.fuel, 100)

    def test_sas_reset(self):
        self.sas_maxfuel = self.theSAS.fuel
        self.theSAS.fuel = 0
        self.theSAS.reset()
        self.assertEqual(self.sas_maxfuel, self.theSAS.fuel)

class TimescaleTestCase(unittest.TestCase):
    def setUp(self):
        self.timescale = TimeScale()

    def test_scale_faster(self):
        scale = self.timescale.scale
        self.timescale.faster()

        self.assertEqual(scale * 2, self.timescale.scale)

    def test_scale_slower(self):
        scale = self.timescale.scale
        self.timescale.slower()

        self.assertEqual(scale / 2.0, self.timescale.scale)

    def test_scale_set(self):
        returnVal = self.timescale._set_scale(self.timescale._MAX_SCALE)
        self.assertEquals(self.timescale.scale, self.timescale._MAX_SCALE)
        self.assertTrue(returnVal)

        returnVal = self.timescale._set_scale(self.timescale._MIN_SCALE)
        self.assertEquals(self.timescale.scale, self.timescale._MIN_SCALE)
        self.assertTrue(returnVal)

        prevScale = self.timescale.scale
        returnVal = self.timescale._set_scale(self.timescale._MAX_SCALE + 1)
        self.assertEqual(prevScale, self.timescale.scale)
        self.assertFalse(returnVal)

        self.timescale._set_scale(self.timescale._MIN_SCALE - 1)
        self.assertEqual(prevScale, self.timescale.scale)
        self.assertFalse(returnVal)

    def test_scale_reset(self):
        baseScale = self.timescale.scale
        self.timescale._set_scale(self.timescale._MIN_SCALE)

        self.assertTrue(self.timescale.reset())
        self.assertEqual(self.timescale.scale, baseScale)

class ExplosionTestCase(unittest.TestCase):
    def setUp(self):
        self.explosion = Explosion(1, range(5))

    def test_explosion_loop(self):
        numImages = len(self.explosion.images)
        for i in range(numImages * 2):
            self.assertEqual(i % numImages, self.explosion.current_frame)
            self.assertEqual(i % numImages, self.explosion.image)

            self.explosion.update_frame()

class ZoomTestCase(unittest.TestCase):
    #ZOOM TESTS
    def setUp(self):
        self.zoom = Zoom()

    def test_zoom_zoom(self):
        curzoom = self.zoom.zoom
        self.zoom.zoom = 2**-17
        self.assertEqual(curzoom, self.zoom.zoom)
        self.zoom.zoom = 80000
        self.assertEqual(curzoom, self.zoom.zoom)
        self.zoom.zoom = 2
        self.assertEqual(2, self.zoom.zoom)

    def test_zoom_zoomin_zoomout(self):
        curzoom = self.zoom.zoom
        self.zoom.zoom_in()
        self.assertEqual(curzoom*2, self.zoom.zoom)
        self.zoom.zoom_out()
        self.assertEqual(curzoom, self.zoom.zoom)

    def test_zoom_reset(self):
        self.zoom.reset()
        self.assertEqual(self.zoom.zoom, 1)

class PhysicsTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)

    def test_gravity(self):
        c1 = CelestialBody('earth', self.space, 10**20, 796375, (0, 0), 0.99999, (128,200,255), 100000, pm.Body.DYNAMIC)
        testPosition = pm.Vec2d(0, 1000)

        self.assertEqual(Physics.gravity(c1, testPosition), pm.Vec2d(0, 66738400))

    def test_netGravity(self):
        c1 = CelestialBody('earth', self.space, 10**20, 796375, (0, 1000), 0.99999, (128,200,255), 100000, pm.Body.DYNAMIC)
        c2 = CelestialBody('moon', self.space, 10**15, 796375, (1000, 0), 0.99999, (128,200,255), 100000, pm.Body.DYNAMIC)
        testPosition = (0, 0)

        self.assertEqual(Physics.netGravity([c1,c2], testPosition), pm.Vec2d(66.7384, 66738400))

class DrawerTestCase(unittest.TestCase):
    def setUp(self):
        self.drawer = Drawer()
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)
    def test_drawer_inRange(self):
        coords =[-1, 99]
        themax = [77, 77]
        self.assertFalse(Drawer.inRange(themax, coords))
        coords =[5, 5]
        self.assertTrue(Drawer.inRange(themax, coords))


if __name__ == '__main__':
    unittest.main()
