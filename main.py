# Load libraries
from machine import Pin, ADC
from time import sleep


# Initialization of GPIO18 as input
digital = Pin(18,Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)

led.value(0)

print("KY-038 Microphone test")

def sound():
    # Endless loop for reading out the ADC
    while True:
        digital_value = digital.value()
        print(digital_value)
        if digital_value == 1:
            led.value(0)
            sleep(0.1)
        else:
            led.value(1)

sound()