import RPi.GPIO as GPIO # type: ignore

import threading, logging, time
from pyutil.constants import LCD, SERVO, LED, UP, DOWN, ledOutput

# try:
#     import RPi.GPIO as GPIO # type: ignore
# except (ImportError, RuntimeError):
#     from mock_rpi_gpio import GPIO

stop_event = threading.Event()

class Core():
    def __init__(self) :
        logging.debug('_________App has started_________')
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LCD, GPIO.OUT)
        GPIO.setup(SERVO, GPIO.OUT)
        GPIO.setup(ledOutput, GPIO.OUT)
        GPIO.setup(LED, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Initialize PWM on the servo pin with a frequency of 50Hz (standard for most servos)
        self.pwm = GPIO.PWM(SERVO, 50)
        self.pwm.start(0)

        logging.debug('_________GPIO pins initialized_________')
        
        """
        Set default values of lcd and servo to None
        for checking if the code is running for first time.
        """
        self.led = GPIO.input(LED)
        self.lcd = None
        self.servo = None
        self.toggle = False

    def start(self):
        """
        The program will be running continuously 
        until 'q' is pressed.
        """
        try:
            while not stop_event.is_set(): 
                if GPIO.input(LED) != self.led:
                    self.led = GPIO.input(LED)
                    self.toggleLED()
                    time.sleep(0.5)
                    
                if GPIO.input(DOWN) == GPIO.LOW:
                    self.set_angle(0)
                    time.sleep(0.5)

                if GPIO.input(UP) == GPIO.LOW:
                    self.set_angle(180)
                    time.sleep(0.5)
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                logging.error('Program interrupted by user.')
            else:
                logging.error(f"An error occurred: {e}")
        finally:
            self.stopThread()
            
    def toggleLED(self):
        GPIO.output(ledOutput, GPIO.input(LED))
    
    # def toggleImage(self):
    #     self.toggle = not self.toggle
    #     if self.toggle:
    #         self.showImage("assets/face.png")
    #     else:
    #         self.showImage("assets/logo.png")

    def on_lcd_btn_press(self, gpioValue):
        """
        Controlling lcd display from here.
        """
        logging.debug(f"LCD Button {LCD} pressed")
        if self.lcd is None:
            GPIO.output(LCD, GPIO.LOW)
            time.sleep(0.5)
            if gpioValue == GPIO.HIGH:
                logging.debug("LCD Button is set to HIGH")
                GPIO.output(LCD, gpioValue)
                self.lcd = gpioValue
        else:
            if self.lcd != gpioValue:
                logging.debug(f"self.lcd : {self.lcd}")
                logging.debug(f"User Input : {gpioValue}")
                GPIO.output(LCD, gpioValue)
                self.lcd = gpioValue
                return
            logging.debug("LCD Button is set to LOW")
            GPIO.output(LCD, GPIO.LOW)
            self.lcd = GPIO.LOW
            time.sleep(0.5)
                    
    def set_angle(self, angle):
        """Helper function that controls the servo angle."""
        duty_cycle = 2 + (angle / 18)
        GPIO.output(SERVO, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(SERVO, False)
        self.pwm.ChangeDutyCycle(0)
    
    def stopThread(self):
        self.pwm.stop()
        GPIO.cleanup()
        stop_event.set()
    
    def stopCore(self):
        while True:
            user_input = input("Enter 'q' to quit: ")
            if user_input.lower() == 'q':
                logging.debug('Exiting...')
                self.stopThread()
                break

starter_thread = threading.Thread(target=Core().start())

starter_thread.start()

class App():
    def run():
        Core().stopCore()
        if starter_thread:
            starter_thread.join()