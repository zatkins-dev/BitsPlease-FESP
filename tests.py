import unittest

from rockets.testrocket import genRocket
from rockets import Rocket, TestTank
import pymunk as pm

class RocketTestCase(unittest.TestCase):
        def setUp(self):
            self.space = pm.Space(threaded=True)
            self.rocket = genRocket(self.space)

        def test_default_rocket(self):
            self.assertEqual(self.rocket.space, self.space)

        def test_append_component(self):
            self.newTank = TestTank(self.rocket)
            self.rocket.addComponent(self.newTank)
            self.assertIn(self.newTank, self.rocket.components)
            self.tearDown()

        def tearDown(self):
            self.rocket.reset() 