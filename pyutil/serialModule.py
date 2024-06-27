#! /usr/bin/env python
import threading, time, serial

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
            self.ser = serial.Serial(tty, baud, timeout=1)
            self.isPortOpen = True
            print('_________Opened Serial Port_________')
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