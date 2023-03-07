from machine import Pin, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
trigger = Pin(21, Pin.OUT)
echo = Pin(20, Pin.IN)



ledRed = machine.Pin(2, machine.Pin.OUT)
ledGreen = machine.Pin(3, machine.Pin.OUT)

ledGreen.off()
ledRed.off()
alerte = 8
#int(input('Quelle est la distance min?') )

def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   distance = "{:.1f}".format(distance)   
   print(distance + " cm")   
   return str(distance)

def checkDistance(cm):
    if float(cm) < alerte:
        ledGreen.off()
        ledRed.on()
    else:
        ledGreen.on()
        ledRed.off()
        
while True:
    lcd.clear()
    cm = ultra()
    checkDistance(cm)
    lcd.putstr(cm)
    utime.sleep_ms(500)
    
    
    

    

  
    
