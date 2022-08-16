#Micro-Python Driver for Winstar LCD Module WH1602B1-SLL-JWV
#Refer Datasheet for more details.
#Written By Mayank Manas, Univerity of Westminster

from machine import Pin
import utime


class LCD:
    def __init__(self, RS, CSB, SCL, SDA):
        self.RS=Pin(RS, Pin.OUT)
        self.CSB=Pin(CSB, Pin.OUT)
        self.SCL=Pin(SCL, Pin.OUT)
        self.SDA=Pin(SDA, Pin.OUT)
        self.delay_us=20
        self.cursor,self.blink= False,False
    
    def initialise(self):
        utime.sleep_ms(20)              #Initial Delay
        self.RS.value(0)
        self.CSB.value(1)
        self.SCL.value(1)
        self.SDA.value(1)
        utime.sleep_us(self.delay_us)
        self.writeCommand(0b00111000)		#Function Set
        utime.sleep_us(self.delay_us)
        self.writeCommand(0b00001000)		#Display off
        utime.sleep_us(self.delay_us)
        self.writeCommand(0b00000001)		#Display Clear
        utime.sleep_ms(1)
        self.writeCommand(0b00000110)		#Entry mode set
        utime.sleep_us(self.delay_us)
        self.writeCommand(0b00001100)  	    #Display On
        utime.sleep_us(self.delay_us)

    def writeCommand(self, command):
        bMask=128
        self.CSB.value(0)
        self.RS.value(0)
        while bMask:
            self.SCL.value(0)
            utime.sleep_us(self.delay_us)
            self.SDA.value(command & bMask)
            self.SCL.value(1)
            utime.sleep_us(self.delay_us)
            bMask=bMask>>1

        self.RS.value(1)
        self.CSB.value(1)

    def writeData(self,char):
        bMask=128
        self.CSB.value(0)
        self.RS.value(1)
        while bMask:
            self.SCL.value(0)
            utime.sleep_us(self.delay_us)
            self.SDA.value(char & bMask)
            self.SCL.value(1)
            utime.sleep_us(self.delay_us)
            bMask=bMask>>1
        self.RS.value(1)
        self.CSB.value(1)

    def print(self,string):
        for char in string:
            self.writeData(ord(char))

    def clear(self):
        self.writeCommand(0b00000001)
        utime.sleep_ms(1)

    def home(self):
        self.writeCommand(0b00000010)
        utime.sleep_ms(1)
    
    def cursor(self,blink=True):
        self.cursor=True
        if blink:
            self.writeCommand(0b00001111)
            self.blink=True
        else:
            self.writeCommand(0b00001110)
            self.blink=False

    def noCursor(self):
        self.writeCommand(0b00001100)

    def display(self):
        if not self.cursor:
            self.writeCommand(0b00001100)
        elif self.blink:
            self.writeCommand(0b00001111)
        else:
            self.writeCommand(0b00001110)

    def noDisplay(self):
        self.writeCommand(0b00001000)

    