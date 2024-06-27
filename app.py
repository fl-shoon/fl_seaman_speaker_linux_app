#! /usr/bin/env python
import RPi.GPIO as GPIO # type: ignore
import threading, time, pygame, serial
from pyutil.constants import LCD, SERVO, UP, DOWN, AUDO, baud_rate

class App():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Avoid reinitialization
            self.initialized = True
        
            print('_________App has started________')

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

            # pygame.mixer.init()

            self.isPortOpen = False
            self.toggleImg = False
            self.recvData = bytearray()
            self.stop_event = threading.Event()
            self.serial_event = threading.Event()

            serial_thread = threading.Thread(target=self.open, args=("/dev/ttyACM0",), kwargs={'baud': 115200, 'timeout': 3})
            serial_thread.start()
            serial_thread.join(15)

            print('_________Serial initialized_________')
            
            self.send('test'.encode())
            time.sleep(0.5)
            result, data = self.recv(10)
            print(result)

            self.switchImage("assets/logo.png")
            time.sleep(0.5)
            result, data = self.recv(10)
            print(result)

            print('_________Logo image displayed_________')

    def open(self, tty, baud=115200, timeout=0.1):
        try:
            self.ser = serial.Serial(tty, baud, timeout=timeout)
            time.sleep(timeout + 1)
            self.isPortOpen = self.ser.is_open
            print('_________Opened Serial Port_________')
        except Exception as e:
            self.isPortOpen = False

        return self.isPortOpen
    
    def recv(self, timeout=3):
        time_start = time.time()
        time_end = time_start
        self.serial_event.clear()
        self.recvData.clear()
        result = False

        while not self.serial_event.is_set():
            time_end = time.time()
            if (time_end - time_start > timeout):
                result = False
                self.serial_event.set()
                print("lcd display response timeout:{0}sec".format(timeout))
                break

            buff = self.ser.read()

            if len(buff) > 0:
                self.recvData.extend(buff)
                if (self.recvData.find(b'\n')) >= 0:
                    result = True
                    self.serial_event.set()
                    break

        return (result, self.recvData)
    
    def send(self, data):
        self.ser.write(data)

    def switchImage(self, fname):
        self.ser.read_all()
        self.ser.write(open(fname, "rb").read())
    
    def run(self):
        while not self.stop_event.is_set(): 
            input_img = GPIO.input(LCD)
            print(f"user input lcd: {input_img}")
            time.sleep(0.5)

            input_servo_up = GPIO.input(UP)
            print(f"user input servo up: {input_servo_up}")
            time.sleep(0.5)

            input_servo_down = GPIO.input(DOWN)
            print(f"user input lcd: {input_servo_down}")
            time.sleep(0.5)

            print(f"serial port open: {self.isPortOpen}")
            time.sleep(0.5)

            if self.isPortOpen:
                if input_img == GPIO.LOW:
                    self.toggleImg = not self.toggleImg
                    self.send('test'.encode())
                    time.sleep(0.5)
                    result, data = self.recv(10)
                    print(result)

                    if self.toggleImg: showImage = "assets/face.png"
                    else: showImage = "assets/logo.png"
                    self.switchImage(showImage)
                    time.sleep(0.5)
                    result, data = self.recv(10)
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

    def close(self):
        self.serial_event.set()
        if (self.isPortOpen):
            self.ser.close()
            self.isPortOpen = False
    
    def stop(self):
        self.close()
        self.stop_event.set()
        self.pwm.stop()
        # pygame.mixer.music.pause()
        # pygame.mixer.music.stop()
        print(f"\nport open or not: {self.isPortOpen}")