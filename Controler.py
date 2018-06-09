import RPi.GPIO as GPIO
import serial, time

class Controler():
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup((11,12,13),GPIO.OUT)
        p = GPIO.PWM(11, 2)
        p.start(50)
        
        self.ser=serial.Serial('/dev/ttyUSB0',9600,timeout=3)
        print(self.ser.isOpen())

    def __del__(self):
        self.ser.close()
        GPIO.cleanup()

    def SendCmd(self, strCmd):                
        GPIO.output((12,13), 0)
        time.sleep(0.5)
        strCmd = strCmd + '\r\n'
        print('Send: ' + strCmd)
        self.ser.write(strCmd.encode())
        strRead = self.ser.readline()
        print('Read:' + strRead.decode())
        time.sleep(0.5)
        GPIO.output((12,13), 1)
        time.sleep(1)
        
    def FindID(self, strID):
        self.SendCmd('AT+DVID' + strID)


if __name__ == '__main__':
    tx = Controler()
    tx.FindID('0001')
    tx.FindID('0002')
    tx.FindID('0003')
    del tx




