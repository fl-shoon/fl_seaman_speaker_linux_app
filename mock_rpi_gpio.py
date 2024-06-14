import logging
from pyutil.constants import LCD, SERVO

class MockGPIO:
    BCM = 'BCM'
    OUT = 'OUT'
    HIGH = 1
    LOW = 0
    states = [LOW, HIGH]

    def __init__(self):
        self.btn = None
    
    def setmode(self, mode):
        logging.debug(f"GPIO mode set to {mode}")
    
    def setup(self, pin, mode):
        logging.debug(f"GPIO pin {pin} set to {mode}")
    
    def write(self, pin, state):
        try:
            logging.debug(f"GPIO pin {pin} value has been set to {self.states[state]}")
        except IndexError:
            logging.debug("Please enter only 0 or 1")
            self.read(pin)

    def listenBtn(self):
        try:
            user_input = input("Enter l for lcd btn and s for servo btn: ")
            if user_input.lower() == 'q':
                return 'stop'
            str_input = str(user_input)
            if str_input.lower() == 'l': 
                self.btn = LCD
                return self.btn
            elif str_input.lower() == 's': 
                self.btn = SERVO
                return self.btn
            else: 
                logging.debug("Invalid input. Please enter a valid alphabet.")
                self.listenBtn()
        except ValueError:
            logging.debug("Invalid input. Please enter a valid alphabet.")
            self.listenBtn()
    
    def read(self, pin):
        try:
            user_input = input(f"Enter state...0/1...for GPIO pin {pin}: ")
            if user_input.lower() == 'q':
                return 'stop'
            integer_input = int(user_input)
            return integer_input
        except ValueError:
            logging.debug("Invalid input. Please enter an integer.")
            self.read(pin)
    
    def pwm(self, pin):
        logging.debug(f"pwm value set at pin {pin}")
        def start(frequency):
            logging.debug(f"pwn started with pwm {frequency}")
        def stop():
            logging.debug("pwn stopped")

        self.start = start
        self.stop = stop
    
    def cleanup(self):
        print("GPIO cleanup")

# Export the mock class as RPi.GPIO
GPIO = MockGPIO()
