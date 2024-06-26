#! /usr/bin/env python
import RPi.GPIO as GPIO # type: ignore
import threading, time, pygame
from pyutil.constants import LCD, SERVO, UP, DOWN, AUDO
from pyutil.serialModule import SerialModule as serialMod

stop_event = threading.Event()

class App():
    def __init__(self) :
        print('_________App has started________su_')
        """
        Set default values of lcd and servo to None
        for checking if the code is running for first time.
        """
        self.isSerialPortOpen = False
        self.setup()
        # pygame.mixer.init()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO, GPIO.OUT)
        GPIO.setup(LCD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(AUDO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Initialize PWM on the servo pin with a frequency of 50Hz (standard for most servos)
        self.pwm = GPIO.PWM(SERVO, 50)
        self.pwm.start(0)

        print('_________GPIO pins initialized_________')
        
        self.serialModule = serialMod()
        self.isSerialPortOpen = self.serialModule.isPortOpen

        print('_________Opened Serial Port_________')
    
    def run(self):
        try:
            # self.play_audio("assets/silent.wav")
            # time.sleep(0.5)

            self.serialModule.send('test'.encode())
            time.sleep(0.5)
            result, data = self.serialModule.recv(10)
            print(result)

            self.serialModule.switchImage("assets/logo.png")
            time.sleep(0.5)

            while not stop_event.is_set(): 
                input_img = GPIO.input(LCD)
                print(f"user input lcd: {input_img}")
                time.sleep(0.5)

                input_servo_up = GPIO.input(UP)
                print(f"user input servo up: {input_servo_up}")
                time.sleep(0.5)

                input_servo_down = GPIO.input(DOWN)
                print(f"user input lcd: {input_servo_down}")
                time.sleep(0.5)

                if self.serialModule.isPortOpen:
                    if input_img == GPIO.LOW:
                        self.serialModule.toggleImg = not self.serialModule.toggleImg
                        self.serialModule.send('test'.encode())
                        time.sleep(0.5)
                        result, data = self.serialModule.recv(10)
                        print(result)

                        if self.serialModule.toggleImg: showImage = "assets/face.png"
                        else: showImage = "assets/logo.png"
                        self.serialModule.switchImage(showImage)
                        time.sleep(0.5)
                        result, data = self.serialModule.recv(10)
                        print(result)
                    
                if GPIO.input(UP) == GPIO.LOW:
                    self.set_angle(0)
                    time.sleep(0.5)

                if GPIO.input(DOWN) == GPIO.LOW:
                    self.set_angle(180)
                    time.sleep(0.5)
                
                if GPIO.input(AUDO) == GPIO.LOW:
                    self.play_audio("assets/short44100c2.wav")
                    time.sleep(0.5)

        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                print('\nProgram interrupted by user.')
            else:
                print(f"An error occurred: {e}")
        finally:
            self.stop()
            
    def set_angle(self, angle):
        """Helper function that controls the servo angle."""
        duty_cycle = 2 + (angle / 18)
        GPIO.output(SERVO, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(SERVO, False)
        self.pwm.ChangeDutyCycle(0)
    
    def play_audio(self, fname):
        pygame.mixer.music.load(fname)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    def stop(self):
        self.serialModule.close()
        self.pwm.stop()
        # pygame.mixer.music.pause()
        # pygame.mixer.music.stop()
        print(f"\nport open or not: {self.isSerialPortOpen}")
        stop_event.set()

if __name__ == "__main__":
    App().run()

# from subprocess import run
# run(f"sudo python -m pip install -r requirements.txt --break-system-packages", shell=True)