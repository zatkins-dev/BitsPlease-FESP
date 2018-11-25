<<<<<<< HEAD
from rockets.component import Component
from rockets.sas import SAS, AdvancedSAS
from rockets.thruster import *
from rockets.commandmodule import CommandModule
from rockets.tank import Tank, TestTank
from rockets.rocket import Rocket
import rockets.testrocket
=======
import os
_ASSETS_PATH = ""
if os.path.exists(os.path.abspath("assets")):
    _ASSETS_PATH = os.path.abspath("assets")
elif os.path.exists(os.path.abspath("../assets")):
    _ASSETS_PATH = os.path.abspath("../assets")

from .component import Component
from .sas import SAS, AdvancedSAS
from .tank import Tank, TestTank
from .commandmodule import CommandModule
from .thruster import *
from .rocket import Rocket
from . import testrocket


>>>>>>> project-4
