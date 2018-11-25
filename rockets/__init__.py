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


