# Add imports here (machine, time, etc.)
from machine import Pin, Timer, PWM # Connects the Raspberry Pi pins to Thonny
from time import sleep # Allows for the use of the sleep() function
from utime import sleep
from dht import DHT11


# Add variables here (temperature_control, moisture_control, led_control, buzzer_control, etc.)
temperature = ""
humidity = ""
issue = ""
current_led = ""

digital = Pin(18,Pin.IN, Pin.PULL_UP) # This is the setup for the sound sensor
red_led = Pin(27, Pin.OUT)
yellow_led = Pin(16, Pin.OUT)
green_led = Pin(28, Pin.OUT)
blue_led = Pin(26, Pin.OUT)
dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
pwm = PWM(Pin(9)) 

red_led.value(0) # The LED begins off
yellow_led.value(0)
green_led.value(0)
blue_led.value(0)

pwm.freq(800)

def minute(timer): # This timer correlates to the mode seen later
    while True: # Ensures that the buzzer continues even after the timer has reset
        pwm.duty_u16(32768) # Half of 35535, half volume
        sleep(1) 
        pwm.duty_u16(0) # no volume, creates an alarm sound
        sleep(1)

def condition_read():
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi))
    print()
    sleep(2)

def clap_detect():
    while True: # Continues until break occurs
        digital_value = digital.value() # Creating a variable based on the sound sensor input
        print(digital_value) # Used as a test to see the difference in binary

        if digital_value == 1: # The digital value at 1 represents a noise being made
            (current_led).value(0)
            sleep(0.1)
        else:
            (current_led).value(1)


def too_high():
    timer = Timer() # Assigns the timer to the in-built function
    timer.init(mode=Timer.PERIODIC, period = 60000, callback=minute)
    while temperature > 22 or humidity > 60:
        current_led = red_led
        clap_detect()    

        if clap_detect == True:
            red_led.value(0)
            # buzzer.value(0)
            break

        red_led.value(1)
        condition_read()


def warning():
    while True:
        current_led = yellow_led
        clap_detect()   

        if clap_detect == True:
            yellow_led.value(0)
            break
        else:
            yellow_led.value(1)

        condition_read()
        if issue == "temperature":
            if temperature != 22 or temperature != 15:
                break
        elif issue == "humidity":
            if humidity < 30 or 35 < humidity < 55 or humidity > 60:
                break


def just_right():
    while True:
        current_led = green_led
        clap_detect()       

        if clap_detect == True:
            green_led.value(0)
            break
        else:
            green_led.value(1)

        condition_read()
        if issue == "temperature":
            if temperature <= 15 or temperature >= 22:
                break
        elif issue == "humidity":
            if humidity <= 35 or humidity >= 55:
                break


def too_low():
    while True:
        current_led = blue_led
        clap_detect()       

        if clap_detect == True:
            blue_led.value(0)
            # buzzer.value(0)
            break
        else:
            blue_led.value(1)
            sleep(60)
            # buzzer.value(1)

        condition_read()
        if issue == "temperature":
            if temperature >= 15:
                break
        elif issue == "humidity":
            if humidity >= 35:
                break


def main():
    while True:
        # Perform measurement
        condition_read()
        temperature = dht11_sensor.temperature()
        humidity = dht11_sensor.humidity()

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
        if humidity > 60:
            issue = "humidity"
            too_high()
        elif 55 >= humidity >= 60 or 30 >= humidity >= 35:
            issue = "humidity"
            warning()
        elif 35 > humidity > 55:
            issue = "humidity"
            just_right()
        else:
            issue = "humidity"
            too_low()        

main()