class Dispenser:
    def __init__(self, amount=0):
        self.liquid_amount = amount # mL
        self.dispensing = False

    def get_remaining_liquid(self):
        return self.liquid_amount

    def update_remaining_liquid(self, new):
        self.liquid_amount = new

    def dispense(self, amount):
        self.liquid_amount = self.liquid_amount - amount

        
# send a signal to the Arduino to start the dispensing process.
# send a signal to the Arduino to end the dispensing process.