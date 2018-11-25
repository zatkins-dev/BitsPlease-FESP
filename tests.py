import unittest

from rockets.testrocket import genRocket
from rockets import Rocket, CommandModule, UpGoer2000, AdvancedSAS, RightRCS, LeftRCS, TestTank
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

        def test_remove_component(self):
            compToRemove = self.baseComponents[0]
            self.rocket.removeComponent(compToRemove)
            self.assertNotIn(compToRemove, self.rocket.components)

            self.assertRaises(ValueError, self.rocket.removeComponent, compToRemove)
        
        def test_rocket_throttle_bounds(self):
            self.rocket.throttle = 99
            self.assertEqual(self.rocket.throttle, 1)
            self.rocket.throttle = -99
            self.assertEqual(self.rocket.throttle, 0)
