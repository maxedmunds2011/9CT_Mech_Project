# Imports
""" While simple to grasp, these imports are essential in containing in-built functions that allow the program to actially function. """
from machine import Pin, PWM, Timer # This is the main import for the Raspberry Pi Pico, it allows me to use the GPIO pins, PWM and Timers
from utime import sleep # Allows me to use the sleep function to pause the program for a certain amount of time
from dht import DHT11 # Allows me to measure temperature and humidity using the DHT11 sensor

# Pin Setup
""" The setup of these pins is the most important part of this program - it links the physical components such as the sensors and
wiring to the code where something can be outputted from these components. The setup of the pins is done normally with one ground pin
and one power pin, represented by the numbers shown below. The other pins are used to read the data from the sensors and output the
data into valuable information that dictates the state of LEDs and buzzers. """
digital = Pin(18, Pin.IN, Pin.PULL_UP) # This sets up the sound sensor on pin 18 as an input with a pull-up resistor
dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP)) # This sets up the DHT11 sensor on pin 14 as an input with a pull-up resistor

pwm1 = PWM(Pin(13)) # This sets up the first buzzer, for the temperature
pwm1.duty_u16(0) # Sets the duty cycle of the first buzzer to 0, which means it is off
pwm2 = PWM(Pin(9)) # This sets up the second buzzer, for the humidity
pwm2.duty_u16(0) # Sets the duty cycle of the second buzzer to 0, which means it is off

# All of these pins use two RGB LEDs, a single device that can output three primary colours and four more secondary colours through turning multiple on at once
t_blue_led = Pin(26, Pin.OUT) # This sets up the blue LED for temperature indication
t_red_led = Pin(27, Pin.OUT) # This sets up the red LED for temperature indication
t_green_led = Pin(28, Pin.OUT) # This sets up the green LED for temperature indication

h_red_led = Pin(15, Pin.OUT) # This sets up the red LED for humidity indication
h_green_led = Pin(12, Pin.OUT) # This sets up the green LED for humidity indication
h_blue_led = Pin(11, Pin.OUT) # This sets up the blue LED for humidity indication

# Global Variables
""" These variables are essential in controlling many different aspects of the program, primarily as timers that continue as the loop 
repeats over and over again, but also as booleans that create gates depending on the state of the program. One example of this is the
buzzer_silenced variable, which is used to check if the buzzer has been silenced by a clap. If it has, then the buzzer will not be 
activated again until the cooldown period has passed. """
buzzerstart1_timer = Timer() # This sets up a timer for the first buzzer, for the temperature
buzzerstart2_timer = Timer() # This sets up a timer for the second buzzer, for the humidity
buzzerwait_timer = Timer() # This sets up a timer for the buzzer and clap detection to wait after a clap has been detected
buzzer1_on = False # This variable is used to check if the first buzzer is on or off
buzzer2_on = False # This variable is used to check if the second buzzer is on or off
buzzer_silenced = False # This variable is used to check if the buzzer has been silenced by a clap
clap_silenced = False # This variable is used to check if the clap detection has been silenced by a clap, ensuring that claps don't stack

# List
""" This is just a simple, untampered list that creates the led flashing by linking to a function focused on later. """
LEDs = [t_blue_led, t_red_led, t_green_led, h_red_led, h_green_led, h_blue_led] # A list of all LEDs stated earlier in the pin setup

# Buzzer Functions
""""""
def toggle_buzzer1(timer):
    if pwm1.duty_u16() == 0:
        pwm1.duty_u16(32768)
    else:
        pwm1.duty_u16(0)
        
def toggle_buzzer2(timer):
    if pwm2.duty_u16() == 0:
        pwm2.duty_u16(32768)
    else:
        pwm2.duty_u16(0)

def minute1(timer):
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer1)
    
def minute2(timer):
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer2)
    
def start_buzzer1():
    global buzzer1_on
    buzzer1_on = True
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute1)
    
def start_buzzer2():
    global buzzer2_on
    buzzer2_on = True
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute2)  
    
def stop_buzzer1():
    global buzzer1_on
    buzzer1_on = False
    buzzerstart1_timer.deinit()
    pwm1.duty_u16(0)
    
def stop_buzzer2():
    global buzzer2_on
    buzzer2_on = False
    buzzerstart2_timer.deinit()
    pwm2.duty_u16(0) 

# Clap Functions
"""  """
def minute_5(timer):
    global buzzer_silenced, clap_silenced
    buzzer_silenced = False
    clap_silenced = False
    
def cooldown():
    buzzerwait_timer.init(mode=Timer.ONE_SHOT, period=5 * 60 * 1000, callback=minute_5)

def sound_detected(pin):
    global clap_silenced, buzzer_silenced
    if clap_silenced == False:
        buzzer_silenced = True
        clap_silenced = True
        stop_buzzer1()
        stop_buzzer2()
        cooldown()

digital.irq(trigger=Pin.IRQ_RISING, handler=sound_detected)

# LED Functions
"""  """
def all_leds_off():
    for x in LEDs:
        (x).value(0)

def too_high(t=False, h=False):
    if t:
        if buzzer_silenced == False:
            pwm1.freq(800)
            start_buzzer1()
        t_red_led.value(1)
    if h:
        if buzzer_silenced == False:
            pwm2.freq(800)
            start_buzzer2()
        h_red_led.value(1)

def warning(t=False, h=False):
    if t:
        stop_buzzer1()
        t_red_led.value(1)
        t_green_led.value(1)
    if h:
        stop_buzzer2()
        h_red_led.value(1)
        h_green_led.value(1)

def just_right(t=False, h=False):
    if t:
        stop_buzzer1()
        t_green_led.value(1)
    if h:
        stop_buzzer2()
        h_green_led.value(1)

def too_low(t=False, h=False):
    if t:
        if buzzer_silenced == False:
            pwm1.freq(500)
            start_buzzer1()
        t_blue_led.value(1)
    if h:
        if buzzer_silenced == False:
            pwm2.freq(500)
            start_buzzer2()
        h_blue_led.value(1)

# Main Loop
"""  """
while True:
    all_leds_off()
    
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi))
    print() 
    
    if temp > 22:
        too_high(t=True)   
    elif temp == 22 or temp == 15:
        warning(t=True)
    elif 15 < temp < 22:
        just_right(t=True)
    else:
        too_low(t=True)

    if humi > 60:
        too_high(h=True)
    elif (55 <= humi <= 60) or (30 <= humi <= 35):
        warning(h=True)
    elif 35 < humi <= 55:
        just_right(h=True)
    else:
        too_low(h=True)

    sleep(2)