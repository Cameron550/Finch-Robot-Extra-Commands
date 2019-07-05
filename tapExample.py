# A simple program that randomly changes the LED when the Finch is tapped or shaken
# Try it by setting the Finch on a table and tapping the top
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

    # If a tap or shake has been detected recently, set the LED to a random color
    if tap or shake:
        tweety.led(randint(0,255), randint(0, 255), randint(0,255))

    # Get obstacles to use to exit loop
    left, right = tweety.obstacle()
    
tweety.close()
