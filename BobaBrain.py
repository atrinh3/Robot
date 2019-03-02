"""
Summary: BobaKat Pyton script that will coordinate activity and send 
         info to Arduinos
Author: Alan L. Trinh
Last Modified: 12/8/2018
"""
import time
import os
import logging 
import serial
from qrtools import QR

ORDER_PARAMETERS = 4

GRAB_ANGLE = 0
RELEASE_ANGLE = 90

FOREARM_RESET = 0
FOREARM_CUP = 0
FOREARM_DELIVER = 0

BICEP_RESET = 0
BICEP_CUP = 0
BICEP_DELIVER = 0


# This is the order class. May want to put this in a separate file later.
class Order:
    def __init__(self, name_input, flavor_input="original", ice_input="normal", sugar_input="normal"):
        self.name = name_input
        self.flavor = flavor_input
        self.ice = ice_input
        self.sugar = sugar_input
        self.completed = False
    
    def __repr__(self):
        return ("{Name=%s;Flavor=%s;Ice=%s;Sugar=%s}", 
            self.name,
            self.flavor, 
            self.ice, 
            self.sugar)

    def set_flavor(self, flavor):
        try:
            self.flavor = flavor
        except Exception:
            logging.debug("Invalid flavor input.")

    def set_sugar_level(self, level):
        try:
            if level == "more":
                self.sugar = level
            if level == "normal":
                self.sugar = level
            if level == "less":
                self.sugar = level
        except Exception:
            logging.debug("Invalid sugar level input.")

    def set_ice_level(self, level):
        try:
            if level == "more":
                self.ice = level
            if level == "normal":
                self.ice = level
            if level == "less":
                self.ice = level
        except Exception:
            logging.debug("Invalid ice level input.")

    def validate(self):
        """
        TODO: Verify the chosen options are available.
        """

    def finish_order(self):
        self.completed = True
            

class BobaBrain:
    def __init__(self, name="BobaKat", order_count_start=0, 
                 boba=100, ice=100, sugar=100, tea=100):
        self.name = name
        self.order_count = order_count_start
        self.cup_location = [0, 0, 0]
        self.delivery_location = [0, 0, 0]
        self.boba_amount = boba
        self.ice_amount = ice
        self.sugar_amount = sugar
        self.tea_amount = tea
        self.order_in_progress = False
        self.holding = False

    def __repr__(self):
        return ("{Name:%s;Cur_Count:%i;Cup_Loc:%s;Deliv_Loc:%s;Boba:%f;Ice:%f;Sugar:%f;Tea:%f;In_Work:%s;Holding:%s}",
            self.name,
            self.order_count,
            str(self.cup_location),
            str(self.delivery_location),
            self.boba_amount,
            self.ice_amount,
            self.sugar_amount,
            self.tea_amount,
            str(self.order_in_progress),
            str(self.holding))

    @property
    def get_current_order_count(self):
        return self.order_count

    @property
    def get_cup_location(self):
        return self.cup_location

    @property
    def get_delivery_location(self):
        return self.delivery_location

    @property
    def get_remaining_boba(self):
        return self.boba_amount

    @property
    def get_remaining_ice(self):
        return self.ice_amount

    @property
    def get_remaining_sugar(self):
        return self.sugar_amount

    @property
    def get_remaining_tea(self):
        return self.tea_amount

    @property
    def is_working(self):
        return self.order_in_progress

    @property
    def is_holding(self):
        return self.holding

    def update_order_count(self, new_order_count):
        self.order_count = new_order_count

    def update_cup_location(self, new_cup_location):
        self.cup_location = new_cup_location

    def update_deliver_location(self, new_delivery_location):
        self.delivery_location = new_delivery_location

    def update_boba(self, amount):
        self.boba_amount = amount

    def update_ice(self, amount):
        self.ice_amount = amount

    def update_sugar(self, amount):
        self.sugar_amount = amount

    def update_tea(self, amount):
        self.tea_amount = amount

    def locate_cup(self):
        """
        TODO: First, put in known coordinates to reach.  Send coordinates 
            to respective Arduino's controlling motors.
            
            Can either use the assign_angle method or combine the two if
            it's not going to be used anywhere else (like the robot base
            or delivery).

        TODO: Future, add vision to allow realtime recognition and search.
            This would cleaner if assign_angle funciton is separate.
        """
        cuplocation = [0,0,0]
        self.update_cup_location(cuplocation)


#serial_connection = "/dev/..."
#bicep_connection = "/dev/ttyAC01"
#forearm_connection = "/dev/ttyAC02"

baudrate = 9600




#scanner_serial = 
#bicep_serial = serial.Serial(bicep_connection, baudrate)
#forearm_serial = serial.Serial(forearm_connection, baudrate)



def main():
    # Boot Arduinos
    establish_arduino_connections()

    
    pass


def establish_arduino_connections():
    """
    TODO: Find com line to Arduino and connect to it to allow uploading 
          arduino code.
    """
    bicep_serial = serial.Serial(bicep_connection, baudrate)
    forearm_serial = serial.Serial(forearm_connection, baudrate)
    

"""
Waits for information to come from the scanner.  When data is recieved,
it will try to make an order with the incomming string.  If sucessful,
the order will be returned and break out of the while loop. Otherwise,
the order that just came in will be ignored and the scanner will continue
to be active.
"""
def scan_for_order():
    """
    TODO: This code will receive information from the scanner to convert into
          an order that will be transmitted to the Arduino.

          Maybe add a physical button to push that will turn on the scanner
          for 5-10s.  Once a scan happens, turn off the scanner until the 
          button is pressed again.
    """
    serial_scanner = Serial(serial_connection, 9600)
    while 1:
        if serial_scanner.available() > 0:
            scanned_order = Order(serial_scanner.readline())
            if scanned_order:
                return scanned_order    


# A "scan event" will be the moment the scanner detects and scans a code.
# The scanner will get an order that looks like:
#     "Name:Flavor:Ice:Sugar"
#     "Alan:ThaiTea:normal:less"
# Need to separate by ":" and create order with it.
def scan_event(scanner_string):
    o = scanner_string.split(":")
    try:
        assert (len(o) == ORDER_PARAMETERS, "Order was invalid.")
        """
        TODO: Make an order.validate class function
              order = Order(o[0], o[1], o[2])
              assert order.validate() == True, "Order was invalid. Deleting order."
        """
        return Order(o[0], o[1], o[2], o[3])
    except AssertionError as error:
        logging.debug(error)
        return False

    


def grab_cup():
    """
    TODO: Simple function to close only the hand controlled by servo.
    """
    # v Pseudocode v
    assign_angle(WRIST, RELEASE_ANGLE)
    assign_angle(BICEP, BICEP_CUP)
    assign_angle(FOREARM, FOREARM_CUP)
    time.sleep(3)
    assign_angle(WRIST, GRAB_ANGLE)

def deliver_cup():
    pass

def move_arm(bicep_pin, forearm_pin, target_coordinates):
    """
    TODO: Takes [x, y, z] coordinates and arm pins to determine how to
          make the arms move.

          ex -
          assign_angle(bicep, 45)
    """


# Pick an arm segment (given by the param "arm_segment_serial_connection"), 
# and set a new target angle (given by the param "target_angle").
# This function will return True if successful, false otherwise.
def assign_angle(arm_pin, arm_segment_serial_connection, target_angle):
    # flush out output buffer
    # send a signal char to indicate incoming info is important
    # send EOM char
    arm_segment_serial_connection.write("$$%0.2f##\n", target_angle)
    # Watchdog timer pseudocode:
    timer = time.time()
    assign_recieved = False
    assign_complete = False
    while 1:
        try:
            assert (arm_segment_serial_connection.readline() == 
                "Angle assignment recieved",
                "Error - arm pin " + arm_pin + " did not get an assignment.")
            logging.info("Setting arm pin %i to target angle %f.", 
                arm_pin, target_angle)
            assign_recieved = True
        except AssertionError as error:
            logging.debug(error)
            break
    if assign_recieved:
        # Watchdog timer psuedocode:
        timer = time.time()
        while 1:
            try:
                assert (arm_segment_serial_connection.readline() == 
                    "Angle setting successful.", 
                    "Angle setting unsucessful.")
                logging.info("Arm pin %i is now at %0.2f degrees.")
                assign_complete = True
            except AssertionError as error:
                if time.time() - timer > 10:
                    logging.debug(error)
                    break
    try:
        assert (assign_complete == True, "Angle assignment was not successful.")
        return True
    except AssertionError as error:
        #Logging.debug(error):
        return False








