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
        self.rocket = Rocket(self.baseComponents)

    def test_default_rocket(self):
        # test if rocket was actually added to our space
        self.assertEqual(self.rocket.space, self.space)

        # test if the components were actually added to the rocket
        self.assertIs(self.rocket.components, self.baseComponents)

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


if __name__ == '__main__':
    unittest.main()
        
