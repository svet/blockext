# coding=utf-8
from __future__ import unicode_literals

import time

from blockext import *

import serial
import io

class Asuro:
    def __init__(self):
        self.foo = 0

        for tty in ['/dev/ttyUSB0', '/dev/ttyUSB1', 'none']:
            try:
                self.ser = serial.Serial(tty, 2400, timeout=10)
                #self.ser = serial.serial_for_url('socket://localhost:4444', timeout=10)
                break
            except:
                if tty == 'none':
                  print "Unable to find Serial Port, Please plug in cable or check cable connections."
                  exit()

        #self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))

    def _problem(self):
        if time.time() % 8 > 4:
            return "Your Asuro is not connected."

    def _is_connected(self):
        try:
            #self.ser.write("test")
            return True
        except:
            return False

    def _on_reset(self):
        print("""
        Reset! The red stop button has been clicked
        """)

    def asuro_cmd(self, cmd):
        self.ser.write(cmd)
        dummy = self.ser.read(len(cmd))
        time.sleep(0.5)
        out = ''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        print str(out)
        return out

    @predicate("Asuro bereit")
    def ready(self):
        print "Ready"

    @command("Fahre %n cm", is_blocking=True)
    def go(self, distance):
        self.asuro_cmd("[x" + str(distance) + "y100f]")
  
    @command("Drehe %n Grad links", is_blocking=True)
    def turn(self, degree):
        self.asuro_cmd("[x" + str(degree) + "y100l]")

    @command("Motoren an")
    def MotorOn(self):
        self.asuro_cmd("[d]")

    @command("Motoren aus")
    def MotorOff(self):
        self.asuro_cmd("[h]")

    @reporter("Taster")
    def get_bumper(self):
        return self.asuro_cmd("[s]") 

    @reporter("Batterie")
    def get_battery(self):
        return self.asuro_cmd("[V]") 

    @reporter("Chirp")
    def get_chirp(self):
        return self.asuro_cmd("[u]")


descriptor = Descriptor(
    name = "Asuro",
    port = 8000,
    #host = "localhost",
    blocks = get_decorated_blocks_from_class(Asuro)
)

extension = Extension(Asuro, descriptor)

if __name__ == "__main__":
    extension.run_forever(debug=True)

