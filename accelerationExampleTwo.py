# A simple program that changes the Finch buzzer based on x-axis orientation.
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

    # Make it buzz - beak up yields higher frequencies, beak down yields lower
    tweety.buzzer(0.1, (880 - int(x*770.0)));

    # Get obstacles to use to exit loop
    left, right = tweety.obstacle()
    
tweety.close()
