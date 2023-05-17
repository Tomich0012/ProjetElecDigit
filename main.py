from machine import Pin, I2C
import utime
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import neopixel
import sys
import select

poller = select.poll()
poller.register(sys.stdin, 1)

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
trigger = Pin(27, Pin.OUT)
echo = Pin(26, Pin.IN)

PIN = 15  
NUM_LEDS = 28 
strip = neopixel.NeoPixel(Pin(PIN), NUM_LEDS)

strip[0] = (0, 0, 0)
strip.write()
alerte = 5
distance = 0

def read_from_port():
    if poller.poll(0):
        line = sys.stdin.buffer.readline()
        if line:
            data = line.decode('utf-8')
            return data
        
def dechiffre():
    global alerte

    data = read_from_port()
    if data is not None:
        new_alert = float(data)
        if new_alert != alerte:
            alerte = new_alert


def redSpecialEffect():
    global distance
    while distance < alerte:
        write_to_lcd(distance)  
        for i in range(NUM_LEDS):
            strip[i] = (255, 0, 0)
        strip.write()
        utime.sleep_ms(200)  
        for i in range(NUM_LEDS):
            strip[i] = (0, 0, 0)
        strip.write()
        utime.sleep_ms(200)
        distance = ultra()   

        
def write_to_lcd(distance):
    lcd.clear()
    if distance < 100:
        lcd.putstr(str(int(distance)) + " cm")
    else:
        lcd.putstr(str(round(distance/100, 1)) + " m")
        
def ultra():
    global distance

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
    distance_str = "{:.1f}".format(distance)
    
    print(distance_str + "," + str(alerte), end='\n')

    return distance

def changerLedColor(color):
    for i in range(NUM_LEDS):
        strip[i] = color
    strip.write()

def checkDistance():
    if distance < alerte:
        redSpecialEffect()
    else:
        changerLedColor((0, 255, 0))
        
while True:
    dechiffre()
    distance = ultra() 
    checkDistance()  
    write_to_lcd(distance) 
    utime.sleep_ms(500)



