# BitsPlease-FESP: Flat Earth Space Program
What lies before you is a prototype for a 2D rocket-bulding space exploration game.
Current functionality includes physical interaction between planets and a rocket 
such as collision and gravity, as well as basic control of the rocket. There is also
a basic fuel system, meaning that you can lose control of aspects of the rocket
when fuel is exhausted. 

To run this prototype, you'll need [Python3](https://www.python.org/downloads/ "Python Foundation Download Page") as well as a few dependencies. Once you have those dependencies, you can run the file `__main__.py` or `main.py`, which will start the program.

### Documentation
See [BitsPlease-FESP GitHub Pages](https://zatkins-school.github.io/BitsPlease-FESP/) for documentation and artifacts.

### Dependencies:
 * [Pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation "Pygame Getting Started Page") `pip install pygame`
 * [Pymunk](http://www.pymunk.org/en/latest/installation.html "Pymunk Installation Instructions") `pip install pymunk`

### Controls:
 * Left SHIFT - Increase Thrust Throttle
 * Left CTRL - Decrease Thrust Throttle
 * Z - Full Throttle
 * X - Cut Thrust
 * A - Rotate Counter-Clockwise
 * D - Rotate Clockwise
 * V - Enable SAS, locking rocket to the current angle of rotation.
 
 ### Known Bugs:
  * Zooming in the rocket builder leads to incorrectly placed objects
  * Rocket can look like it is "inside of the planet" at a small set of certain zoom levels/positions
  * Trajectory line can visibly change to be incorrect at a small set of certain zoom levels
  * Rocket Holding-Angle adjustements at a high-time scale do not work correctly. This functionality was actually removed from the game at     all time scales greater than 1x due to this
  * Removing the last SAS module while SAS is on doesn't disable SAS, although this is functionally impossible to reproduce while playing     the game
  * OS display scaling causes objects to be renedred in the incorrect location on screen if scaling is not set to 100%

