import unittest
from graphics import Video, Zoom
Video.init()

from rockets.testrocket import genRocket
from rockets import Rocket, CommandModule, UpGoer2000, DeltaVee, SandSquid, AdvancedSAS, RightRCS, LeftRCS, TestTank
import pymunk as pm
import pygame as pg
from time import sleep

from audio import AudioManager

class RocketTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)

    def test_default_rocket(self):
        # test if rocket was actually added to our space
        self.assertEqual(self.rocket.space, self.space)

        # test if the components were actually added to the rocket
        self.assertIs(self.rocket.components, self.baseComponents)

    def test_rocket_constructor(self):

        self.rocket = Rocket(genRocket)

        # test initial conditions... destroyed, saslock, etc.
        self.assertFalse(self.rocket.destroyed)
        self.assertFalse(self.rocket.isAngleLocked)
        self.assertEqual(self.rocket.throttle, 0)

        # test that the component lists are the same
        self.assertListEqual(self.rocket.components, self.baseComponents)

        # test that components bodies were made to be the rocket
        for component in self.rocket.components:
            self.assertIs(component.body, self.rocket)


    def test_append_component(self):
        self.newTank = TestTank(self.rocket)
        self.rocket.addComponent(self.newTank)
        self.assertIn(self.newTank, self.rocket.components)
        self.tearDown()

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
        self.assertEqual(self.rocket.isAngleLocked, True)
        self.rocket.removeComponent(self.rocket.SASmodules[0])
        self.assertEqual(self.rocket.isAngleLocked, False)

    def test_rocket_reset(self):
        self.newTank = TestTank(self.rocket)
        self.rocket.addComponent(self.newTank)
        self.rocket.throttle = 0.5
        self.rocket.isAngleLocked = True
        self.rocket.reset()
        self.assertEqual(self.rocket.tanks, [])
        self.assertEqual(self.rocket.throttle, 0)
        self.assertEqual(self.rocket.isAngleLocked, False)

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

class  AudioTestCase(unittest.TestCase):
    def setup(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = Rocket(self.baseComponents)
        self.audioManager = AudioManager()
        audioManager.silenceMusic()

    def test_SoundEffects_thursterDefault(self):
        #Test throttle at 0 + no thrusters - Should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + no thrusters - Should not play
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterUpgoer(self):
        self.rocket.addComponent(UpGoer2000(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterDeltaVee(self):
        self.rocket.addComponent(DeltaVee(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterSandSquid(self):
        self.rocket.addComponent(SandSquid(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterRightRCS(self):
        self.rocket.addComponent(RightRCS(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_thrusterLeftRCS(self):
        self.rocket.addComponent(LeftRCS(self.rocket))

        #Test throttle at 0 + thruster on rocket - should not play
        self.rocket.throttle = 0
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at 1 + thruster on rocket - should play at max volume
        self.rocket.throttle = 1
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), 1)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

        #Test throttle at .5 + thruster on rocket - should play at .5 volume
        self.rocket.throttle = .5
        audioManager.thrusterSoundEffect(len(self.rocket.thrusters) != 0, self.rocket.throttle)
        self.assertTrue(pg.mixer.Channel(2).get_busy())
        self.assertEqual(pg.mixer.Channel(2).get_volume(), .5)

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(2).get_busy())

    def test_SoundEffects_SASDefault(self):
        #With no SAS, no sound should play both times
        self.rocket.isAngleLocked = False
        audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        self.rocket.isAngleLocked = True
        audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

    def test_SoundEffects_SASActive(self):
        self.rocket.addComponent(AdvancedSAS(self.rocket))

        #With SAS inactive, no sound should play
        self.rocket.isAngleLocked = False
        audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

        #With SAS active, sound should play
        self.rocket.isAngleLocked = True
        audioManager.sasSoundEffect(len(self.rocket.SASmodules) != 0 and self.rocket.isAngleLocked)
        self.assertTrue(pg.mixer.Channel(1).get_busy())

        #Should stop sound effect
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.Channel(1).get_busy())

    def test_backgroundMusic(self):
        #No music should be playing, should now be playing music
        audioManager.musicChecker()
        self.assertTrue(pg.mixer.music.get_busy())

        #wait 5 seconds
        time.sleep(5)

        #Try to reset the song, it should not work
        audioManager.musicChecker()
        self.assertTrue(pg.mixer.music.get_pos() > 4500)

        #Should stop music
        audioManager.silenceMusic()
        self.assertFalse(pg.mixer.music.get_busy())

class  TankTestCase(unittest.TestCase):
#TANK TESTS
    def setup(self):
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

class  SASTestCase(unittest.TestCase):
#SAS TESTS
    def setup(self):
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

class ZoomTestCase(unittest.TestCase):
    #ZOOM TESTS
    def setup(self):
        self.theZoom = self.
if __name__ == '__main__':
    unittest.main()
