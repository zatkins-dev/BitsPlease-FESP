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
        """
        #initialize the music
        pg.init()
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        #start the initial music
        self._SOUND_PATH = os.path.abspath("assets/sound/") if os.path.exists(os.path.abspath("assets/sound/")) else os.path.abspath("../assets/sound/")
        self._MUSIC_LIST = ["Sci-fiPulseLoop.wav", "Astrometrics_-_02_-_Fire_in_the_Mountains.mp3", "Deep_Space_Destructors_-_01_-_Journey_To_The_Space_Mountain.mp3", "bensound-scifi.mp3"]

        #Set up Sound Effects
        self._ThrusterSound = pg.mixer.Sound(os.path.join(self._SOUND_PATH, "rocketLaunch.ogg"))
        self._SASSound = pg.mixer.Sound(os.path.join(self._SOUND_PATH, "22453__nathanshadow__space-ambient.wav"))

        pg.mixer.Channel(1).set_volume(30.0)
        pg.mixer.music.load(os.path.join(self._SOUND_PATH, "Sci-fiPulseLoop.wav"))
        pg.mixer.music.play(0)
        pg.mixer.music.set_volume(.75)

    def musicChecker(self):
        """
        Detects when the current background music has stopped and will play the
        next background song.
        """
        if(pg.mixer.music.get_busy() == False):
            pg.mixer.music.load(os.path.join(self._SOUND_PATH, random.choice(self._MUSIC_LIST)))
            pg.mixer.music.play(0)
            pg.mixer.music.set_volume(0.75)

    def sasSoundEffect(self, statusConst):
        """
        Plays an SAS sound effect until stopped.

        :param statusConst: If SAS is active
        :type statusConst: boolean
        """
        if(pg.mixer.Channel(1).get_busy() == False and statusConst == True):
            pg.mixer.Channel(1).play(self._SASSound, loops=1)
        elif(pg.mixer.Channel(1).get_busy() == True and statusConst == False):
            pg.mixer.Channel(1).stop()

    def thrusterSoundEffect(self, status, amount):
        """
        Plays an SAS sound effect until stopped.

        :param status: If thruster is on rocket
        :type status: boolean
        :param amount: Amount of thruster power
        :type amount: double
        """
        if(status):
            if(pg.mixer.Channel(2).get_busy() == False):
                pg.mixer.Channel(2).play(self._ThrusterSound, loops=1)
            pg.mixer.Channel(2).set_volume(amount)
        else:
            pg.mixer.Channel(2).stop()

    def silenceMusic(self):
        """Stops the music.
        """
        pg.mixer.Channel(2).stop()
        pg.mixer.Channel(1).stop()
        pg.mixer.music.stop()
