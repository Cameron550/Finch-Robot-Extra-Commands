# Functions to control Finch robot.

# The Finch is a robot for computer science education. Its design is the result
# of a four year study at Carnegie Mellon's CREATE lab.

# http://www.finchrobot.com
# See included examples and documentation for how to use the API

import time
import finchconnection
import random

class Finch():

    def __init__(self):
        self.connection = finchconnection.ThreadedFinchConnection()
        self.connection.open()


    def led(self, *args):
        """Control three LEDs (orbs).

          - hex triplet string: led('#00FF8B'),
            0-255 RGB values: led(0, 255, 139)
            or a general colors name(lowercase).
        """

        color_list = {'red':(255,0,0), 'yellow':(255,255,0), 'green':(0,255,0),
                      'purple':(128,0,128), 'blue':(0,0,255), 'grey':(128,128,128),
                      'white':(255,255,255), 'black':(0,0,0), 'pink':(255,192,203),
                      'orange':(255,165,0), 'brown':(165,42,42)}

        my_color = args[0]

        if my_color in color_list.keys():
            r, g, b = [int(x) % 256 for x in color_list[my_color]]

        elif len(args) == 3:
            r, g, b = [int(x) % 256 for x in args]

        elif (len(args) == 1 and isinstance(args[0], str)):
            color = args[0].strip()

            if len(color) == 7 and color.startswith('#'):
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)

            else:
                print("Please enter an acceptable value. An acceptable value is a hexadecimal code, an RGB value, or simply a general colors name(lowercase).")
                return

        else:
            print("Please enter an acceptable value. An acceptable value is a hexadecimal code, an RGB value, or simply a general colors name(lowercase).")
            return


        self.connection.send(b'O', [r, g, b])


    def buzzer(self, duration, frequency):
        """ Outputs sound. Does not wait until a note is done beeping.

        duration - duration to beep, in seconds (s).
        frequency - integer frequency, in hertz (HZ).
        """
        millisec = int(duration * 1000)
        self.connection.send(b'B',
                [(millisec & 0xff00) >> 8, millisec & 0x00ff,
                 (frequency & 0xff00) >> 8, frequency & 0x00ff])


    def buzzer_with_delay(self, duration, frequency):
        """ Outputs sound. Waits until a note is done beeping.

        duration - duration to beep, in seconds (s).
        frequency - integer frequency, in hertz (HZ).
        """
        millisec = int(duration * 1000)
        self.connection.send(b'B',
                [(millisec & 0xff00) >> 8, millisec & 0x00ff,
                 (frequency & 0xff00) >> 8, frequency & 0x00ff])
        time.sleep(duration*1.05)


    def light(self):
        """ Get light sensor readings. The values ranges from 0.0 to 1.0.

            returns - a tuple(left, right) of two real values
         """
        self.connection.send(b'L')
        data = self.connection.receive()
        if data is not None:
            left = data[0] / 255.0
            right = data[1] / 255.0
            return left, right


    def obstacle(self):
        """Get obstacle sensor readings.

        returns - a tuple(left,right) of two boolean values
        """
        self.connection.send(b'I')
        data = self.connection.receive()
        if data is not None:
            left = data[0] != 0
            right = data[1] != 0
            return left, right


    def temperature(self, unit = 'celsius'):
        """ Returns temperature in degrees Celsius, or if selected, can
            return the temperature in Fahrenheit or Kelvin. """

        self.connection.send(b'T')
        data = self.connection.receive()
        if data is not None:

            celsius = (data[0] - 127) / 2.4 + 25;
            fahrenheit = (celsius * 9/5) + 32
            kelvin = celsius + 273.15

            if unit != 'celsius':

                if unit == 'Fahrenheit' or unit == 'fahrenheit':
                    return fahrenheit

                elif unit == 'Kelvin' or unit == 'kelvin':
                    return kelvin

                else:
                    print('The unit you entered is unavailable. \n Here are the available units: celcius(default), fahrenheit, kelvin')
                    return celsius

            else:
                return celsius


    def convert_raw_accel(self, a):
        """Converts the raw acceleration obtained from the hardware into G's"""

        if a > 31:
            a -= 64
        return a * 1.6 / 32.0


    def acceleration(self):
        """ Returns the (x, y, z, tap, shake).  x, y, and z, are
            the acceleration readings in units of G's, and range
            from -1.5 to 1.5.
            When the finch is horisontal, z is close to 1, x, y close to 0.
            When the finch stands on its tail, y, z are close to 0,
            x is close to -1.
            When the finch is held with its left wing down, x, z are close to 0,
            y is close to 1.
            tap, shake are boolean values -- true if the correspondig event has
            happened.
        """

        self.connection.send(b'A')
        data = self.connection.receive()
        if data is not None:
            x = self.convert_raw_accel(data[1])
            y = self.convert_raw_accel(data[2])
            z = self.convert_raw_accel(data[3])
            tap = (data[4] & 0x20) != 0
            shake = (data[4] & 0x80) != 0
            return (x, y, z, tap, shake)


    def wheels(self, left, right):
        """ Controls the left and right wheels.

        Values must range from -1.0 (full throttle reverse) to
        1.0 (full throttle forward).
        use left = right = 0.0 to stop.
        """

        dir_left = int(left < 0)
        dir_right = int(right < 0)
        left = min(abs(int(left * 255)), 255)
        right = min(abs(int(right * 255)), 255)
        self.connection.send(b'M', [dir_left, left, dir_right, right])


    def estimate_distance(self, time, speed, unit = 'feet'):

        """Estimates the distance finch will travel given time in seconds finch
           is allowed to travel and the speed the wheel() function is set at"""

        distance_units = ['inches', 'centimeters', 'meters']

        feet_per_second = 0.8 * speed
        distance = feet_per_second * time

        if unit != 'feet':

            if unit in distance_units:

                if unit == 'inches':
                    return (distance * 12)

                elif unit == 'centimeters':
                    return (distance * 30.48)

                elif unit == 'meters':
                    return (distance / 3.281)

            else:
                print("That is an incorrect or unavailable unit. The accepted units are: inches, centimeters, meters")

        else:
            return str(distance) + ' feet'


    def estimate_time(self, distance):
        """Insert distance in feet to estimate time of travel"""

        seconds_per_feet = 1.25
        time = distance * seconds_per_feet

        return str(time) + ' seconds'


    def halt(self):
        """ Set all motors and LEDs to off. """
        self.connection.send(b'X', [0])


    def stop_and_start(self, t):
        """Stops all motors and LEDs for a set amount of time then starts again."""
        self.connection.close()
        time.sleep(t)
        self.connection.open()


    def close(self):
        self.connection.close()

