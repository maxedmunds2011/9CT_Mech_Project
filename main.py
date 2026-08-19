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
""" These functions are used to control the buzzers, which are used to indicate when temperature and humidity are too high or too low.
There is one buzzer for each sensor, therefore there are two pathways of code that are identical, however the sensor they are supporting
is different. The buzzers are controlled by PWM, which allows for the frequency and duty cycle to be adjusted, creating different sounds.
The toggle_buzzer functions are used to create a beeping sound instead of a continuous beep. The minute functions are used to start the
beeping sound with the timer indicating the tempo of the buzzer. The start_buzzer and stop_buzzer functions are used to start and stop
their respective buzzers, however while the stop_buzzer function is straight away, the start_buzzer function only activates a one minute
timer until the buzzer starts beeping as an extra warning to the user that the temperature or humidity is too high or too low. 

For the double functions, I will explain only the first one."""
def toggle_buzzer1(timer): # Linked to the minute functions
    if pwm1.duty_u16() == 0: # If the buzzer is off, after 500 milliseconds it will turb back on
        pwm1.duty_u16(32768) # The buzzer at half duty cycle, which is the maximum volume for the buzzer
    else:
        pwm1.duty_u16(0) # The buzzer back to off, creating a beeping sound with the 500 millisecond timer
        
def toggle_buzzer2(timer):
    if pwm2.duty_u16() == 0:
        pwm2.duty_u16(32768)
    else:
        pwm2.duty_u16(0)

def minute1(timer): # Another timer function, related this time to the start_buzzer functions
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer1) # This is the timer to call back the toggle_buzzer function every 500 milliseconds, creating a beeping sound  
    
def minute2(timer):
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer2)
    
def start_buzzer1():
    global buzzer1_on # The in-built global function allows variables outside of a function to be used inside the function
    buzzer1_on = True # Sets to true so that this function doesn't keep repeating itself
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute1) # This is the timer to call back the minute function only once after 60 seconds, where the beeping will begin
    
def start_buzzer2():
    global buzzer2_on
    buzzer2_on = True
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute2)  
    
def stop_buzzer1():
    global buzzer1_on
    buzzer1_on = False # Sets to false to that the buzzer can be activated again if the temperature or humidity is still too high or too low
    buzzerstart1_timer.deinit() # Turns off the timer to the minute function
    pwm1.duty_u16(0) # If the buzzer is on, this will make sure it is turned off
    
def stop_buzzer2():
    global buzzer2_on
    buzzer2_on = False
    buzzerstart2_timer.deinit()
    pwm2.duty_u16(0) 

# Clap Functions
""" The clap functions work in a similar way to the buzzer functions, however they only contain one chain of code as they are used to 
silence all buzzers no matter the state. The minute_5 function is used to reset the buzzer and the ability to read claps after 5 minutes,
ample time for the user to fix the temperature or humidity. The cooldown function is exclusivelt used for starting the 5 minute timer,
and calling the minute_5 function after this time. The sound_detected function relies on the digital.irq line found below that reads signals
throughout the entire loop, and as soon as a sharp sound like a clap is detected, this function will be called. As long as the clap is not
silenced, the function turns off all buzzers and starts the cooldown timer, which will lead to the other functions. """
def minute_5(timer): # A timer function relating to the cooldown function
    global buzzer_silenced, clap_silenced 
    buzzer_silenced = False # Resets the buzzer so it can be activated again
    clap_silenced = False # Resets the clap detection so it can be activated again
    
def cooldown():
    buzzerwait_timer.init(mode=Timer.ONE_SHOT, period=5 * 60 * 1000, callback=minute_5) # This is the timer to call back the minute_5 function only once after 5 minutes of activation

def sound_detected(pin): # This links to the pin in the digital.irq line below
    global clap_silenced, buzzer_silenced
    if clap_silenced == False: # The process can only continue if the cooldown is off and the clap can be read properly
        buzzer_silenced = True # Sets the buzzer to deactivation
        clap_silenced = True # Sets the buzzer to deactivation
        stop_buzzer1() # Calls the stop_buzzer functions to cease all current buzzers
        stop_buzzer2()
        cooldown() # Calls the cooldown function to start the 5 minute timer

digital.irq(trigger=Pin.IRQ_RISING, handler=sound_detected) # One of the most important lines of code, this allows the code to check if there is a clap any time in the loop, and immediately call the function above

# LED Functions
""" The LED functions act as gateways into the many previous functions and are changed purely on the temperature and humidity output.
The all_leds_off function is a small function that just turns all LEDs off before a new read to create a flashing effect and ensure that
code doesn't get jumbled up. Each of the main LED functions have two attributes: t and h - depending on what is read in the main code
will decide what code is read. The too_high and too_low functions operate similarly, starting the buzzer timer and setting the frequency.
The warning and just_right functions also act similarly to each other, turning off their respective buzzer. All four still turn on a 
certain LED. For the comments, the too_high and warning functions will be used for explanation """
def all_leds_off(): 
    for x in LEDs: # Links back to the list earlier and draws a for loop from that
        (x).value(0) # Every LED is turned off in preparation for a new loop

def too_high(t=False, h=False):
    if t: # This set of lines only occur if temperature was in this range in the main loop
        if buzzer_silenced == False and buzzer1_on == False: # Ensures that the buzzer has to be active and it doesn't repeat itself so the timer never turns on
            pwm1.freq(800) # Sets a higher frequency for the higher temperature
            start_buzzer1() # Calls the start_buzzer function to begin the 1 minute timer then the buzzer beep
        t_red_led.value(1) # As with all the LED functions, turns on the desired LED
    if h: # This set of lines only occur is humidity was in this range in the main loop
        if buzzer_silenced == False and buzzer2_on == False:
            pwm2.freq(800) # Sets a higher frequency for the higher humidity
            start_buzzer2()
        h_red_led.value(1)

def warning(t=False, h=False):
    if t:
        stop_buzzer1() # Immediately turns off the respective buzzer or timer for the buzzer
        t_red_led.value(1) # For the colour yellow, the mixing of red and green was needed for the RGB
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
        if buzzer_silenced == False and buzzer1_on == False:
            pwm1.freq(500) # Sets a lower frequency for a lower temperature
            start_buzzer1()
        t_blue_led.value(1)
    if h:
        if buzzer_silenced == False and buzzer2_on == False:
            pwm2.freq(500) # Sets a lower frequency for a lower humidity
            start_buzzer2()
        h_blue_led.value(1)

# Main Loop
""" This is the loop where everything is called into. The main point of this loop is to continuously measure the temperature and humidity
and output the according LED function that eventually links into the buzzer and clap functions. There is a 2 second pause between loops
as that is how fast the KY-015 can properly read """
while True: # The start of the loop, continues until the entire system is turned off
    all_leds_off() # Calls the function to reset all LEDs for the new loop
    
    dht11_sensor.measure() # An extremely important line of code - this allows the KY-015 to record its surroundings
    temp = dht11_sensor.temperature() # Line to record the temperature
    humi = dht11_sensor.humidity() # Line to record the humidity
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi)) # A useless line of code in the actual loop, however this helped me with making sure the temperature and humidity were linking to the correct LED functions
    print() # Acts as a gap in readings for a clearer difference
    
    if temp > 22: # If the temperature is above 22 degrees celsius
        too_high(t=True) # Makes t true for the too_high function
    elif temp == 22 or temp == 15: # If the temperature is exactly 15 or 22 degrees celsius
        warning(t=True) # Makes t true for the warning function
    elif 15 < temp < 22: # If the temperature is between 15 and 22 degrees celsius
        just_right(t=True) # Makes t true for the just_right function
    else: # If the temperature is below 15 degrees celsius
        too_low(t=True) # Makes t true for the too_low function

    if humi > 60: # If the humidity is above 60%
        too_high(h=True) # Makes h true for the too_high function
    elif (55 <= humi <= 60) or (30 <= humi <= 35): # If the humidity is between 30% and 35% or between 55% and 60%
        warning(h=True) # Makes h true for the warning function
    elif 35 < humi < 55: # If the humidity is between 35% and 55%
        just_right(h=True) # Makes h true for the just_right function
    else: # If the humidity is below 30%
        too_low(h=True) # Makes h true for the too_low function

    sleep(2) # Pauses the loop for 2 seconds so that the temperature and humidity sensor can accurately record again next loop