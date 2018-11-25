# BitsPlease-FESP: Flat Earth Space Program
What lies before you is a prototype for a 2D rocket-bulding space exploration game.
Current functionality includes physical interaction between planets and a rocket 
such as collision and gravity, as well as basic control of the rocket. There is also
a basic fuel system, meaning that you can lose control of aspects of the rocket
when fuel is exhausted. 

To run this prototype, you'll need [Python3](https://www.python.org/downloads/ "Python Foundation Download Page") as well as a few dependencies. Once you have those dependencies, you can run the file `__main__.py` or `main.py`, which will start the program.

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

