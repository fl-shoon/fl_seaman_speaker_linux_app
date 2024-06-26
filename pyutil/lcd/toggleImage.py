# -*- coding: utf-8 -*-
import threading, serial, time, sys
import RPi.GPIO as GPIO #type: ignore

IMG = 21
baud_rate = 115200

GPIO.setmode(GPIO.BCM)
GPIO.setup(IMG, GPIO.IN, pull_up_down=GPIO.PUD_UP)
prev_img = GPIO.input(IMG)
print(f"original state of user input: {prev_img}")
time.sleep(0.5)

class SerialModule:
    def __init__(self):
        self.toggleImg = False
        self.isPortOpen = False
        self.recvData = bytearray()
        self.event = threading.Event()

    def recv(self, timeout=3):
        time_start = time.time()
        time_end = time_start
        self.event.clear()
        self.recvData.clear()
        result = False

        while not self.event.is_set():
            time_end = time.time()
            if (time_end - time_start > timeout):
                result = False
                self.stop()
                print("lcd display response timeout:{0}sec".format(timeout))
                break

            buff = self.ser.read()

            if len(buff) > 0:
                self.recvData.extend(buff)
                if (self.recvData.find(b'\n')) >= 0:
                    result = True
                    self.stop()
                    break

        return (result, self.recvData)

    def send(self, data):
        self.ser.write(data)

    def stop(self):
        self.event.set()

    def open(self, tty, baud=115200):
        try:
            self.ser = serial.Serial(tty, baud, timeout=0.1)
            self.isPortOpen = True
        except Exception as e:
            self.isPortOpen = False

        return self.isPortOpen

    def switchImage(self, fname):
        self.ser.read_all()
        self.ser.write(open(fname, "rb").read())

    def close(self):
        self.stop()
        if (self.isPortOpen):
            self.ser.close()
        self.isPortOpen = False
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        serialModule = SerialModule()
        serialModule.open("/dev/ttyACM0", baud_rate)
        time.sleep(1)
        while True:
            input_img = GPIO.input(IMG)
            print(f"user input: {input_img}")
            time.sleep(0.5)

            if serialModule.isPortOpen:
                if input_img == GPIO.LOW:
                    serialModule.toggleImg = not serialModule.toggleImg
                    serialModule.send('test'.encode())
                    time.sleep(0.5)
                    result, data = serialModule.recv(10)
                    print(result)

                    if serialModule.toggleImg: showImage = "face.png"
                    else: showImage = "logo.png"
                    serialModule.switchImage(showImage)
                    time.sleep(0.5)
                    result, data = serialModule.recv(10)
                    print(result)
                
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        serialModule.close()
        print(f"port open or not: {serialModule.isPortOpen}")
        GPIO.cleanup()
        

        
