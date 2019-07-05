# A simple program that changes the Finch LED based on orientation.

from finch import Finch
from random import randint

# Instantiate the Finch object and connect to Finch
tweety = Finch()

left, right = tweety.obstacle()

# Do the following while no obstacles are detected by Finch
while not left and not right:
    # Get the accelerations
    x, y, z, tap, shake = tweety.acceleration()

    # Print the acceleration data
    print("X is %.2f gees, Y is %.2f gees, Z is %.2f gees, tap is %r shake is %r" % (x, y, z, tap, shake));

    # Use the acceleration data to set the LED:
    # beak up
    if x < -0.7 and y > -0.3 and y < 0.3 and z > -0.3 and z < 0.3:
        tweety.led(255,0,0);
    # beak down
    elif x > 0.7 and y > -0.3 and y < 0.3 and z > -0.3 and z < 0.3:
        tweety.led(0,255,0);
    # level
    elif x > -0.5 and x < 0.5 and y > -0.5 and y < 0.5 and z > 0.7:
        tweety.led(0,0,255);
    # upside down
    elif x > -0.5 and x < 0.5 and y > -0.5 and y < 0.5 and z < -0.7:
        tweety.led(0,255,255);
    # left wheel down
    elif x > -0.5 and x < 0.5 and y > 0.7 and z < 0.5 and z > -0.5:
        tweety.led(255,255,0);
    # right wheel down
    elif x > -0.5 and x < 0.5 and y < -0.7 and z < 0.5 and z > -0.5:
        tweety.led(255,0,255);

    # Get obstacles to use to exit loop
    left, right = tweety.obstacle()
    
tweety.close()
