import unittest

from rockets.testrocket import genRocket

import pymunk as pm

class RocketTestCase(unittest.TestCase):
        def setUp(self):
            self.space = pm.Space(threaded=True)
            self.rocket = genRocket(self.space)

        def test_default_rocket(self):
            self.assertEqual(self.rocket.space, self.space)