import sys
import os
import pygame as pg
import random

class AudioManager(object):
    """The AudioManager utility class is designed to manage both the music in
    the background of the game and specific sound effects in the game.

        **Class Variables:**
            *SOUND_PATH*:  A String with the file pathway to the sound assets
            *MUSIC_LIST*:  A List of the music file names
    """

    SOUND_PATH = os.path.abspath("assets/sound/")
    MUSIC_LIST = ["Sci-fiPulseLoop.wav", "Astrometrics_-_02_-_Fire_in_the_Mountains.mp3", "bensound-scifi.mp3"]
    @staticmethod
    def audioInitializer():
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
        pg.mixer.init()
        #start the initial music
        pg.mixer.music.load(os.path.join(AudioManager.SOUND_PATH, "Sci-fiPulseLoop.wav"))
        pg.mixer.music.play(1)

    @staticmethod
    def musicChecker():
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
            pg.mixer.music.load(os.path.join(AudioManager.SOUND_PATH, random.choice(AudioManager.MUSIC_LIST)))
            pg.mixer.music.play(1)
