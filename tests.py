import unittest
from graphics import Video
Video.init()

from rockets.testrocket import genRocket
from rockets import Rocket, CommandModule, UpGoer2000, DeltaVee, SandSquid, AdvancedSAS, RightRCS, LeftRCS, TestTank
import pymunk as pm


class RocketTestCase(unittest.TestCase):
    def setUp(self):
        self.space = pm.Space(threaded=True)
        self.baseComponents = [CommandModule(None), UpGoer2000(None), AdvancedSAS(None), RightRCS(None), LeftRCS(None)]
        self.rocket = genRocket(self.space)

    def test_default_rocket(self):

        # test if rocket was actually added to our space
        self.assertEqual(self.rocket.space, self.space)

        # test if the components were actually added to the rocket
        for i in range(len(self.baseComponents)):
            test_type = type(self.baseComponents[i])
            contains_type = False
            for c in self.rocket.components:
                if isinstance(c, test_type):
                    contains_type = True
            self.assertEqual(contains_type, True)

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

    def test_apply_thrust_fuel

if __name__ == '__main__':
    unittest.main()