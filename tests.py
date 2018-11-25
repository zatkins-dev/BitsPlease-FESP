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
        self.setUp()
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

        # test initial conditions... destroyed, saslock, etc.
        self.assertFalse(self.rocket.destroyed)
        self.assertFalse(self.rocket.isAngleLocked)
        self.assertEqual(self.rocket.throttle, 0)

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
        self.rocket.isAngleLocked = True
        self.assertEqual(self.rocket.isAngleLocked, False)

    def test_rocket_reset(self):
        self.newTank = TestTank(self.rocket)
        self.rocket.addComponent(self.newTank)
        self.rocket.throttle = 0.5
        self.rocket.isAngleLocked = True
        self.rocket.reset()
        self.assertEqual(self.rocket.throttle, 0)
        self.assertEqual(self.rocket.isAngleLocked, False)

    #TANK TESTS
    def test_tank_fuel(self):
        self.newTank = TestTank(self.rocket)
        self.newTank.fuel = -100
        self.assertEqual(self.newTank.fuel, 0)
        self.newTank.fuel = 100
        self.assertEqual(self.newTank.fuel, 100)

    def test_tank_reset(self):
        self.newTank = TestTank(self.rocket)
        self.newTank.fuel = 0
        self.tank_capacity = self.newTank.capacity
        self.newTank.reset()
        self.assertEqual(self.tank_capacity, self.newTank.fuel)

    #SAS TESTS
    def test_sas_fuel(self):
        self.theSAS = self.rocket.SASmodules[0]
        self.theSAS.fuel = -100
        self.assertEqual(self.theSAS.fuel, 0)
        self.theSAS.fuel = 100
        self.assertEqual(self.theSAS.fuel, 100)
if __name__ == '__main__':
    unittest.main()