import sys
import os
import pygame as pg
import random

class AudioManager():
    """
    The AudioManager utility class is designed to manage both the music in
    the background of the game and specific sound effects in the game. 
    """
    #: An :py:class:`string` object with the file pathway to the sound assets
    _SOUND_PATH = os.path.abspath("assets/sound/") if os.path.exists(os.path.abspath("assets/sound/")) else os.path.abspath("../assets/sound/")
    #: A list of the music file names
    _MUSIC_LIST = ["Sci-fiPulseLoop.wav", "Astrometrics_-_02_-_Fire_in_the_Mountains.mp3", "Deep_Space_Destructors_-_01_-_Journey_To_The_Space_Mountain.mp3", "bensound-scifi.mp3"]
    @classmethod
    def init(cls):
        """
        Initializes the audio engine and starts playing with the Sci-fiPulseLoop background music.
        """
        # initialize the music
        pg.mixer.pre_init(44100, 16, 2, 4096)
        pg.mixer.init()
        #s tart the initial music
        cls._MUSIC_LIST = ["Sci-fiPulseLoop.wav", "Astrometrics_-_02_-_Fire_in_the_Mountains.mp3", "Deep_Space_Destructors_-_01_-_Journey_To_The_Space_Mountain.mp3", "bensound-scifi.mp3"]

        #Set up Sound Effects
        cls._ThrusterSound = pg.mixer.Sound(os.path.join(cls._SOUND_PATH, "rocketLaunch.ogg"))
        cls._SASSound = pg.mixer.Sound(os.path.join(cls._SOUND_PATH, "22453__nathanshadow__space-ambient.wav"))

        pg.mixer.Channel(1).set_volume(30.0)
        pg.mixer.music.load(os.path.join(cls._SOUND_PATH, "Sci-fiPulseLoop.wav"))
        pg.mixer.music.play(0)
        pg.mixer.music.set_volume(.75)

    @classmethod
    def musicChecker(cls):
        """
        Detects when the current background music has stopped and will play the
        next background song.
        """
        if(pg.mixer.music.get_busy() == False):
            pg.mixer.music.load(os.path.join(cls._SOUND_PATH, random.choice(cls._MUSIC_LIST)))
            pg.mixer.music.play(0)
            pg.mixer.music.set_volume(0.75)

    @classmethod
    def sasSoundEffect(cls, statusConst):
        """
        Plays an SAS sound effect until stopped.

        :param statusConst: If SAS is active
        :type statusConst: boolean
        """
        if not pg.mixer.Channel(1).get_busy() and statusConst:
            pg.mixer.Channel(1).play(cls._SASSound, loops=1)
        elif pg.mixer.Channel(1).get_busy() and not statusConst:
            pg.mixer.Channel(1).stop()

    @classmethod
    def thrusterSoundEffect(cls, status, amount):
        """
        Plays an Thruster sound effect until stopped.

        :param status: If thruster is on rocket
        :type status: boolean
        :param amount: Amount of thruster power
        :type amount: double
        """
        if(status):
            if not pg.mixer.Channel(2).get_busy():
                pg.mixer.Channel(2).play(cls._ThrusterSound, loops=1)
            pg.mixer.Channel(2).set_volume(amount)
        else:
            pg.mixer.Channel(2).stop()

    @classmethod
    def silenceMusic(cls):
        """
        Stops the music.
        """
        pg.mixer.Channel(2).stop()
        pg.mixer.Channel(1).stop()
        pg.mixer.music.stop()
