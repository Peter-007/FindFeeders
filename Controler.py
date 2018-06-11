#!/usr/bin/env python

#接线端子定义
# 无线模块   树莓派
#   IO-0    pin11
#   set     pin12
#   cs      pin13

import RPi.GPIO as GPIO
import serial, time

class Controler():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup((11,12,13),GPIO.OUT)
        GPIO.output((12,13), 0)
        time.sleep(0.3)
        
        self.ser=serial.Serial('/dev/ttyUSB0',9600,timeout=2)
        print(self.ser.isOpen())

    def __del__(self):
        self.ser.close()
        GPIO.cleanup()

    def SendCmd(self, strCmd, bOpen=True):
        GPIO.output(11, 1)
        GPIO.output((12,13), 0)
        time.sleep(0.5)
        strCmd = strCmd + '\r\n'
        print('Send: ' + strCmd)
        self.ser.write(strCmd.encode())
        strRead = self.ser.readline()
        print('Read:' + strRead.decode())
        GPIO.output((12,13), 1)
        time.sleep(0.1)
        
        for i in range(1):            
            GPIO.output(11, 0)
            time.sleep(0.1)
            GPIO.output(11, 1)
            time.sleep(0.1)
            
            if bOpen:
                GPIO.output(11, 0)
                time.sleep(0.1)
        
    def FindID(self, strID, bOpen=True):
        #self.SendCmd('AT+CLSS')
        self.SendCmd('AT+DVID' + strID, bOpen)

if __name__ == '__main__':
    tx = Controler()
    for i in range(1):
        print("****Open****")
        for i in range(9):
            tx.FindID('01' + '{:0>2d}'.format(i+1))

        print("****Close****")
        for i in range(9):
            tx.FindID('01' + '{:0>2d}'.format(i+1), False)





