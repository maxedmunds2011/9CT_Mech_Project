# Add imports here (machine, time, etc.)
from machine import Pin, ADC # Connects the Raspberry Pi pins to Thonny
from time import sleep # Allows for the use of the sleep() function


# Add variables here (temperature_control, moisture_control, led_control, buzzer_control, etc.)
temperature = ""
humidity = ""
issue = ""

digital = Pin(18,Pin.IN, Pin.PULL_UP) # This is the setup for the sound sensor
red_led = Pin(16, Pin.OUT) # This is setup for the test LED
yellow_led = Pin(17, Pin.OUT)
green_led = Pin(19, Pin.OUT)
blue_led = Pin(20, Pin.OUT)
buzzer = Pin(21, Pin.OUT)

red_led.value(0) # The LED begins off
yellow_led.value(0)
green_led.value(0)
blue_led.value(0)
buzzer.value (0)

def clap_detect():
    print()


def too_high():
    while True:
        clap_detect()       
        if clap_detect == True:
            red_led.value(0)
            buzzer.value(0)
            break
        else:
            red_led.value(1)
            sleep(60)
            buzzer.value(1)
        if temperature <= 22:
            break

def warning():
    while True:
        clap_detect()       
        if clap_detect == True:
            yellow_led.value(0)
            break
        else:
            yellow_led.value(1)
        if temperature != 22 or 15:
            break

def just_right():
    while True:
        clap_detect()       
        if clap_detect == True:
            green_led.value(0)
            break
        else:
            green_led.value(1)
        if temperature <= 15 or temperature >= 22:
            break

def too_low():
    while True:
        clap_detect()       
        if clap_detect == True:
            blue_led.value(0)
            buzzer.value(0)
            break
        else:
            blue_led.value(1)
            sleep(60)
            buzzer.value(1)
        if temperature >= 15:
            break

def main():
    while True:

        """ This is where the temperature reading will go """
        if temperature > 22:
            issue = "temperature"
            too_high()         
        elif temperature == 22 or temperature == 15:
            issue = "temperature"
            warning()
        elif 15 > temperature > 22:
            issue = "temperature"
            just_right()
        else:
            issue = "temperature"
            too_low()


        """ This is where humidity will go """
        if humidity > "60%":
            issue = "humidity"
            too_high()
        elif "50%" >= humidity >= "60%" or "30%" >= humidity >= "35%":
            issue = "humidity"
            warning()
        elif "35%" > humidity > "50%":
            issue = "humidity"
            just_right()
        else:
            issue = "humidity"
            too_low()        