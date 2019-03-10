import serial

class ArmController:
    default_length = 10 # inches
    move_signal = "%"
    stop_signal = "$"


    def __init__(self, length=default_length, angle=0):
        self.length = length
        self.angle = angle
        self.target = 0
        self.in_motion = False

    @property
    def get_length(self):
        return self.length

    def set_length(self, new_len):
        self.length = new_len
    
    @property
    def get_angle(self):
        return self.angle

    def set_angle(self, new_angle):
        self.angle = new_angle
    
    @property
    def get_target(self):
        return self.target

    def set_target(self, new_target):
        self.target = new_target

    @property
    def in_motion(self):
        return self.in_motion
    
    def put_in_motion(self):
        self.in_motion = True

    # TODO: Need way to connect multiple arduinos to Pi.  Maybe i2c?
    def arduino_connection(self):
        pass

    
    def send_move_signal(self, angle):
        serial.write(move_signal + angle + move_signal)
    
    # TODO: send signal to arduino to stop wherever it currently is. 
    # Should read angle and update angle.
    def send_stop_signal(self):
        serial.write(stop_signal)


