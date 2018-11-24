import sys
import os
import pygame as pg
import random

class AudioManager():
    """The AudioManager utility class is designed to manage both the music in
    the background of the game and specific sound effects in the game.

        **Arguments:**
            None.

        **Class Variables:**
            *SOUND_PATH*:  A String with the file pathway to the sound assets
            *MUSIC_LIST*:  A List of the music file names
    """

    def __init__(self):
        """
        Initialize the audio mixer in pygame and begin with the initalized
        Sci-fiPulseLoop background music.

        **Preconditions:**
            1. The music is located in the SOUND_PATH location.

        **Postconditions:**
            1. The Sci-fiPulseLoop will be playing in the background

        **Returns:**
            Nothing.
        """
        #initialize the music
        pg.init()
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        #start the initial music
        self._SOUND_PATH = os.path.abspath("assets/sound/")
        self._MUSIC_LIST = ["Sci-fiPulseLoop.wav", "Astrometrics_-_02_-_Fire_in_the_Mountains.mp3", "bensound-scifi.mp3"]

        #Set up Sound Effects
        self._ThrusterSound = pg.mixer.Sound(os.path.join(self._SOUND_PATH, "rocketLaunch.ogg"))
        self._SASSound = pg.mixer.Sound(os.path.join(self._SOUND_PATH, "22453__nathanshadow__space-ambient.wav"))

        pg.mixer.Channel(1).set_volume(30.0)
        pg.mixer.music.load(os.path.join(self._SOUND_PATH, "Sci-fiPulseLoop.wav"))
        pg.mixer.music.play(1)
        pg.mixer.music.set_volume(.5)

    def musicChecker(self):
        """
        Detects when the current background music has stopped and will play the
        next background song.

        **Preconditions:**
            1. All Music in system is located in the SOUND_PATH location.

        **Postconditions:**
            1. Selected Music will be playing

        **Returns:**
            Nothing.
        """
        if(pg.mixer.music.get_busy() == False):
            pg.mixer.music.load(os.path.join(self._SOUND_PATH, random.choice(self._MUSIC_LIST)))
            pg.mixer.music.play(1)
            pg.mixer.music.set_volume(.5)

    def sasSoundEffect(self, statusConst):
        """
        Plays an SAS sound effect until stopped.

        **Preconditions:**
            1. Sound file located in SOUND_PATH file

        **Postconditions:**
            1. Sound playing as long as SAS is active.

        **Returns:**
            Nothing.
        """
        if(pg.mixer.Channel(1).get_busy() == False and statusConst == True):
            pg.mixer.Channel(1).play(self._SASSound, loops=1)
        elif(pg.mixer.Channel(1).get_busy() == True and statusConst == False):
            pg.mixer.Channel(1).stop()

    def thrusterSoundEffect(self, amount):
        """
        Plays an SAS sound effect until stopped.

        **Preconditions:**
            1. Sound file located in SOUND_PATH file

        **Postconditions:**
            1. Sound playing as long as SAS is active.

        **Returns:**
            Nothing.
        """
        if(pg.mixer.Channel(2).get_busy() == False):
            pg.mixer.Channel(2).play(self._ThrusterSound, loops=1)
        pg.mixer.Channel(2).set_volume(amount)
