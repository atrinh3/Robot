"""

"""

import serial
import time
import os

# Manager class that will control the dispenser of a liquid.
class DispenseManager:
    LOW_THRESHOLD = 0.25 #%
    ARDUINO_BOARD = "-m mega2560"

    def __init__(self, liquid, amount=0, maximum=1000, arduino=ARDUINO_BOARD, threshold=LOW_THRESHOLD):
        self.ingredient = liquid

        self.container_max = maximum
        self.liquid_left = amount # mL
        self.threshold = threshold
        self.low = False

        self.ser = None
        self.arduino_board = arduino
        self.arduino_is_setup = False


    @property
    def __repr__(self):
        return ("Ingredient:{};Level:{};ArduinoSetup:{}".format(
            self.ingredient, self.level, self.arduino_is_setup))

    @property
    def ingredient(self):
        return self.ingredient

    @property
    def get_remaining_liquid(self):
        return self.liquid_left

    @property
    def is_low(self):
        return self.low

    def update_remaining_liquid(self, new):
        if new < self.threshold:
            self.low = True
        else:
            self.low = False
        self.level = new
    
    def setup_arduino(self):
        print("Setting up arduino board.")
        self.ser = serial.Serial("/dev/ttyACM1")
        os.system("ino build {}".format(self.arduino_board))
        os.system("ino upload {}".format(self.arduino_board))
        if self.test_arduino():
            self.arduino_is_setup = True
            print("Arduino setup completed.")
            return True
        else:
            print("Arduino setup failed.")
            return False

    def test_arduino(self, timeout=5):
        start = time.time()
        self.ser.write("Testing...&")
        while True:
            test_time = time.time()
            if test_time - start > timeout:
                print("Arduino test failed. No response detected.")
                return False
            try:
                line = self.ser.readline().decode('utf-8','ignore')
                if line.decode == "Testing...":
                    return True
            except:
                print("Failed to get response from Arduino. Trying again...")
                time.sleep(0.5)

    def send_dispense_signal(self, amount, attempts=5):
        if self.arduino_is_setup:
            if (amount < self.liquid_left):
                print("Sending signal to dispense {}mL of {}.".format(
                    amount, self.ingredient))
                self.ser.write("{}&".format(amount))
                self.update_remaining_liquid(self.liquid_left - amount)
                return True
            else:
                print("Not enough liquid to dispense. Cannot dispense liquid")
                return False
        else:
            print("Arduino is not set up yet.")
            if attempts > 0:
                print("Setting up Arduino connection. Attempt {}/5.".format(
                    6 - attempts))
                self.setup_arduino()
                self.send_dispense_signal(amount, attempts-1)
            else:
                print("Failed to set up Arduino.")
                return False

