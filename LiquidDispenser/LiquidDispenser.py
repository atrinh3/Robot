"""

"""

import serial
import time
import os

# Manager class that will control the dispenser of a liquid.
class DispenseManager:
    LOW_THRESHOLD = 0.25 #%
    ARDUINO_BOARD = "-m mega2560"

    def __init__(self, liquid, arduino=ARDUINO_BOARD, amount=0, maximum=1000, 
                 threshold=LOW_THRESHOLD):
        self.ingredient = liquid

        # Required for operation
        self.ser = None
        self.arduino_board = arduino
        self.arduino_is_setup = False

        # Nice to have / Future implementation
        self.container_max = maximum
        self.remaining_liquid = amount # mL
        self.threshold = threshold
        self.low = False


    @property
    def __repr__(self):
        return ("Ingredient:{};Remaining:{};Low:{};ArduinoSetup:{}".format(
                    self.ingredient, 
                    self.remaining_liquid, 
                    self.low, 
                    self.arduino_is_setup))

    @property
    def ingredient(self):
        return self.ingredient

    @property
    def get_remaining_liquid(self):
        return self.remaining_liquid

    @property
    def is_low(self):
        return self.low

    def update_remaining_liquid(self, new):
        if new < self.threshold:
            self.low = True
        else:
            self.low = False
        self.remaining_liquid = new
    
    
    def setup_arduino(self):
        """Sets up serial communication line with the Arduino. then
        performs a quick test.  If an invalid response is received, 
        the Arduino will be reflashed and retested.  If that fails,
        this will fail out.

        :param self: Dispenser object
        :return: Boolean based on test result
        """        
        print("Setting up serial communication with arduino board.")
        self.ser = serial.Serial("/dev/ttyACM0")
        
        if self.test_arduino():
            self.arduino_is_setup = True
            print("Arduino setup completed.")
            return True
        else:
            print("Arduino setup failed - reflashing Arduino.")
            self.arduino_is_setup = reflash_arduino
            return self.arduino_is_setup


    #TODO: This requires the src.ino file to be included in the
    #       working folder.
    def reflash_arduino(self):
        """Reflash the src.ino files onto the Arduino.  Then the Arduino
        will be re-tested.

        :param self: Dispenser object
        :return: Boolean based on re-test result
        """
        os.system("ino build {}".format(self.arduino_board))
        os.system("ino upload {}".format(self.arduino_board))
        
        #TODO: Play with the sleep time to see if it's necessary
        time.sleep(5)
        return self.test_arduino()


    #TODO: IF this is finniky, can add a retry recursion
    def test_arduino(self, timeout=2):
        """Sends the Arduino a message and expects a certain reply back.

        :param self: Dispenser object
        :param timeout: Time to wait for a response until test fails
        :return: Boolean based on test result
        """
        test_message = "Are you there\r\n"
        self.ser.write(test_message.encode())
        start_time = time.time()
        while True:
            test_time = time.time()
            try:
                test_reply = self.ser.readline().decode('utf-8')
                if test_reply.decode == "I am here":
                    return True
            except Exception as e:
                print(e)
                return False
            if test_time - start_time > timeout:
                print("Arduino test failed. No response detected.")
                return False


    def simple_dispense(self, t=1):
        """No feedback loops invovled.  Will simply send signal to the 
        Arduino to open the valve, and then close it after a set time.

        :param t: Time to keep the valve open in seconds
        :return: None
        """
        open_msg = "Open valve\r\n"
        close_msg = "Close valve\r\n"

        self.ser.write(open_msg.encode())
        time.sleep(1)
        if not validate_response(self.ser.readline(), "Valve open"):
            print("Valve was not opened")
        
        time.sleep(t)
        
        self.ser.write(close_msg.encode())
        time.sleep(1)
        if not validate_response(self.ser.readline(), "Valve closed"):
            print("Valve was not closed!")
            #TODO: This is a significant error.


    def validate_response(actual, expected):
        """Verifies that a message received from the Arduino is as 
        expected.

        :param actual: UTF-8 encoded message from Arduino
        :param expected: Decoded message expected from the Arduino
        """
        decoded = actual.decode()
        print(decoded)
        if decoded != expected:
            print(ERROR - Invalid response received!)
            return False
        return True
    

    # This is a future implementation.  Currently have no resources to
    # do the checks that this function is trying to accomplish.
    #TODO: IF this is finniky, can add a retry recursion
    #TODO: In the future, try to find a way to convert time into amount.
    #       Maybe feedback loop with weight somewhere
    def send_dispense_signal(self, amount, time=1):
        if self.arduino_is_setup:
            if (amount < self.remaining_liquid):
                print("Sending signal to dispense {}mL of {}.".format(
                    amount, self.ingredient))
                self.ser.write("{}&".format(amount))
                self.update_remaining_liquid(self.remaining_liquid - amount)
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

