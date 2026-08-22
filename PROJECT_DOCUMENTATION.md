# Requirements Outline
## The Need
When it is cold and damp, mold has a potential to grow. At night time, rain can also dampen windows or hot air could be stuck inside your bedroom and you wouldn't know about it. I need to create something that will allow me to know when to open and close windows and have a way to turn it off in the night.
## Proposed Solution
The solution that could be implemented is to ake a Raspberry Pi program that includes four primary sensors: a temperature sensor and humidity detector to detect their respective areas, a buzzer when the humidity or temperature reaches a certain level, and a small sound to detect the calpping of hands or other noise. LEDs could also be implemented to show how close the humidity and temperature is to being damp or cold respectively, or as a subtitute to a buzzer. 
## Key Actions
 - Temperature Sensor and Humidity Detector detects temperature and humidity respectivelty outside of the designated range. It does this every 5 seconds.
 - A red or blue LED light is turned on depending on if it's above range (red) or below range (blue)
 - Different pitched buzzer sounds alerts user of the temperature or humidity out of place
 - A clap from the user turns the buzzer off
## Functional Requirements
The designated temperature range is 15-22 degrees celsius, as they are the least likely conditions for mold to grow. 

This is paired with a humidity at between 30 - 50%, because mold germinates most in humidity of 60% or more.

Both the temperature and humidity will have a set of LEDs each for distinguishing the difference.

A red LED will turn on when the temperature is above 22 degrees celsius, or when the humidity is above 60%. After one minute without any clap detected, a high-pitched buzzer will turn on as well. This acts as the 'too high' label

A yellow LED will turn on when the temperature is at 15 or 22 degrees celsius or the humidity is between 55% and 60%. This acts as a warning for movement into the red LED areas.

A green LED will turn on and remain on as long as the temperature is between 16 and 21 degrees celsius and the humidity is between 30 and 55%. This acts as the 'just right' label and should be maintained most of the time.

A blue LED will turn on when the temperature is below 15 degrees celsius or the humidity is below 30%. After one minute without any clap detected, a low-pitched buzzer will turn on as well. This acts as the 'too low' label.

A sound sensor detects a clap when the red LED or blue LED are turned on. At a certain noise level the sound sensor will disable all buzzers for 10 minutes to allow time to fix the humidity and temperature levels
## Test Cases
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Temperature too hot | Temperature sensor reads above 22 degrees celsius | Red LED turns on. after 1 minute a high-pitched buzzer turns on |
| Temperature in high range | Temperature sensor reads 22 degrees celsius | Yellow LED turns on |
| Temperature in medium range | Temperature sensor reads 16-21 degrees celsius | Green LED turns on |
| Temperature in low range | Temperature sensor reads 15 degrees celsius | Yellow LED turns on |
| Temperature too cold | Temperature sensor reads below 15 degrees celsius | Blue LED turns on. After 1 minute a low-pitched buzzer turns on |
| Humidity too high | Humidity detector reads above 60% | Red LED turns on. after 1 minute a high-pitched buzzer turns on |
| Humidity in high range | Humidity detector reads 55-60% | Yellow LED turns on |
| Humidity in medium range | Humidity detector reads 35-55% | Green LED turns on |
| Humidity in low range | Humidity detector reads 30-35% | Yellow LED turns on |
| Humidity too cold | Humidity detector reads below 30% | Blue LED turns on. After 1 minute a low-pitched buzzer turns on |
| Sharp clap detected | Sound sensor detects hertz between 2200 and 2800 | All buzzers are disabled and turned off for 10 minutes | 
## Non-Functional Requirements
### Efficiency:
The robot can't run out of battery or randomly stop working in the middle of the day - it must remain consistently on throughout. All LEDs need to function properly and by themselves, attached to GPIO pins to reserve other pins for the more important sensors.
### Response Time
The robot should detect the temperature and humidity respectively every 5 seconds for maximum response time. The clap should be detected every 0.1 seconds to ensure a fast and connected correlation. 
### Accuracy:
The robot needs to measure the temperature and humidity fairly accurately, to one decimal place. It must detect the difference between a sharp clap and other loud sound to avoid unwanted periods where buzzers are disabled. The clap should also only work 10 minutes after the last clap to avoid stacking. 
# Algorithms
## Flowcharts
<img src="image.png" alt="Description of image">
<img src="image0.png" alt="Description of image">
<img src="image1.png" alt="Description of image">

## Pseudocode
```
BEGIN
WHILE TRUE
    INPUT temp
    IF temp is greater than 22 THEN
        too_high()
    ELIF temp is 15 or 22 THEN
        warning()
    ELIF temp is greater than 15 THEN
        just_right()
    ELSE
        too_low()
    ENDIF
    INPUT moist
    IF moist is greater than 60% THEN
        too_high()
    ELIF moist is 30%-35% or 50%-60% THEN
        warning()
    ELIF moist is greater than 35% THEN
        just_right()
    ELSE
        too_low()
    ENDIF
    ENDWHILE
END

BEGIN too_high()
clap_detect()
IF clap_detect RETURNS 'yes' THEN
    OUTPUT red_Led.value(1)
    wait (60)
    OUTPUT high_buzzer.on
END too_high()

BEGIN clap_detect()
WHILE TRUE
    IF clap_detected THEN
        OUTPUT 'yes'
    ELSE
        OUTPUT 'no'
END clap_detect()
```

# Development and Integration
``` Python
""" The purpose of this successful test was to see if the sound sensor would work when a sharp sound (like a clap or snap of fingers) would activate a random LED. This is the combination of the future sound sensor and a look at the main loop & how LEDs will react, and then to add LEDs and the temperature/humidity sensor. """

from machine import Pin, PWM # Connects the Raspberry Pi pins to Thonny
from time import sleep # Allows for the use of the sleep() function

# Initialization of GPIO18 as input
digital = Pin(18,Pin.IN, Pin.PULL_UP) # This is the setup for the sound sensor
r_led = Pin(16, Pin.OUT)
y_led = Pin(15, Pin.OUT)
g_led = Pin(14, Pin.OUT)
b_led = Pin(13, Pin.OUT)

r_led.value(0)
y_led.value(0)
g_led.value(0)
b_led.value(0) # The LED begins off

print("KY-037 Microphone test")

def too_high():
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
""" This while loop is reading the environment every 0.1 seconds to check for any sounds, specifically sharp sounds, which will turn the test LED on """

while True: # Continues until break occurs
    digital_value = digital.value() # Creating a variable based on the sound sensor input
    print(digital_value) # Used as a test to see the difference in binary
    if digital_value == 1: # The digital value at 1 represents a noise being made
        led.value(0) # Unsure why, but the (0) in this turns the LED on for 0.1 seconds
        sleep(0.1)
    else:
        led.value(1) # Unsure why, but this keeps the LED off
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

""" This unsure circumstance between the LED values will be fixed in a later evaluation. """
```
# Testing and Debugging
## Case Outlines
### Test Case 1 - Too Hot
I added this function into my code, however it doesn't include the implementation of the buzzer, or the timer that goes with it.
### Test Case 2 & 4 - Nearly Too Hot and Nearly too Cold
My warning function works smoothly, and completely fulfills the test case requirements. However, the functionality of the warning could be enhanced with a single buzzer sound instead of a continuous alarm. 
### Test Case 3 - Just Right Temperature
Similar to the warning function, the just_right function works smoothly, and won't need any buzzers as it is safe range. The range could possibly be increased but it's good for now.
### Test Case 5 - Too Cold
Similar to the too_hot function, this one will need a buzzer, however one with lower pitch so that there is a distinguishable difference between the two.
### Test Cases 6 - 10 - Humidity
These test cases are almost exact copies of the the first 5, however they are with humidity. This one will be harder to measure, and I will require the purchase of a humidity sensor to fulfill my original requirements.
### Test Case 11 - The Sound Sensor
As of now, the sound sensor works, however it only works in turning on an LED for a split second. Therefore, I will have to problem solve and figure out some ways to get it to turn off buzzers and LEDs. One way is to generally 'reverse' the current code so that it sets a value to 0 instead of 1. Alternatively, I could research properties between Raspberry Pi Pico sensors to see if there's anything else that could result in a successful clap. I also have to keep in mind the hertz range, which was researched by looking up how much hertz a shark sound (like a clap) is.

## Tests
### Test 1: Too High 
``` Python
""" The first test I'm going to try is the test case of if it is too hot, or humid, a red LED will turn on. We will do the buzzer next once this works. """

from machine import Pin # This will allow us to use the breadboard pins
from utime import sleep # Allows use of the sleep function
from dht import DHT11 # Allows use of the temperature/humidity sensor

""" Variable assigning - this also assigns certain sensors and devices to pins on the Pico. """
dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
red_led = Pin(27, Pin.OUT)

""" This variable will come in use later. """
issue = ""

""" This function was created so that the temperature and humidity can now be read outside of the main loop/function, which is imperative for switching between LEDs without having to use a sound sensor. """
def condition_read():
    dht11_sensor.measure() # Built in function with the DHT11 that measures the temperature and humidity, as seen below
    temp = dht11_sensor.temperature() 
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi)) # This is more of a visual for me to make sure that the device is working
    print()
    sleep(2) # First example of the sleep function. The number in the brackets corresponds to seconds

""" This function will be made more complex with the inclusion of the sound sensor, but for now its only purpose is to turn on a red LED until the temperature and humidity shift out of the dedicated region. """
def too_high(): 
    while temp > 22 or humi > 60: # This ensures that while these conditions are met, the LED will stay red.
        red_led.value(1) # Turns on the LED
        condition_read() # Ensures that temperature and humidity remain recorded
        
while True: # This is the main loop, which will eventually be in the main function
    """ While the temp and humi variables are made reference in the function below, the main loop doesn't see these variables so for now, the temp and humi also have to be assigned on the main loop. """
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    condition_read()
    
    """ This section will become more apparent in its use later on. """
    if temp > 22: # Requirement to run through the too_high function
        issue = "temperature"
        too_high()
    if humi > 60: # Requirement to run through the too_high function
        issue = "humidity"
        too_high()
        
    red_led.value(0) # Makes sure to turn off the LED in case it was on from before
```

Both of these test cases worked (2/11 test cases half-complete)

(From now on, I will add to this code instead of seperating them so I can lay the groundwork and move up to the sound sensor.)
### Test 2: Too High (with buzzers)
``` Python
""" Not as much was added in this test, however this leaves the groundwork for all future LED test cases. The main focus of this was to test the buzzer and implement a timer function. This was done with the research in the second part of: https://randomnerdtutorials.com/raspberry-pi-pico-interrupts-micropython/. """
from machine import Pin, PWM, Timer # Adds the Timer import for the in-built timer function
from utime import sleep
from dht import DHT11

dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
pwm = PWM(Pin(9)) # Assigning of the buzzer to a pin
red_led = Pin(27, Pin.OUT)
issue = ""

pwm.freq(800) # As shown in the test cases, the buzzer has been set to a high frequency

""" The purpose of this new function correlates with the in-built timer. After a minute of the red LED being on, this function will begin and not stop until the robot is turned off, and later when the sound sensor detects a sharp noise. """
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

""" This function was finally complete with the implementation of the timer. The role of the timer is to create a background stopwatch that doesn't interfere with the loop. """
def too_high():
    timer = Timer() # Assigns the timer to the in-built function
    timer.init(mode=Timer.PERIODIC, period = 60000, callback=minute) # The mode I explained above, but the period is the time in milliseconds (this is exactly a minute) and the callback is the function that occurs after the minute
    while temp > 22 or humi > 60:
        red_led.value(1)
        condition_read()
        
        
while True:
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    condition_read()
    
    if temp > 22:
        issue = "temperature"
        too_high()
    if humi > 60:
        issue = "humidity"
        too_high()
        
    red_led.value(0)
""" Otherwise, now its time to focus on the other LEDs and how they differ. I will create a system that changes the LED based on the temperature and humidity. """
```

Now the first 2 test cases have been fully complete. Now I need to complete the bulk of the test cases: the other LEDs that vary slightly in characteristiscs.

### Test 3: Other LEDs (Warning, Just Right & Too Low)
``` Python
""" This was, and probably will be, the biggest change in the project. While I was filling out the other lights, I noticed a problem: only the temperature would read. This was due to the temperature being stuck in a while loop, so I removed that and instead added a new set of LEDs for humidity, different through the first letters: t and h. I used this as well as knowledge of functions to create a system where it will only read if t or h is True. Now the only while loop is the main loop, and there is a flashing effect with the LEDs. """
from machine import Pin, PWM, Timer
from utime import sleep
from dht import DHT11

dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
pwm = PWM(Pin(13))

""" As I explained earlier, I seperated the LEDs into temperture-related and humidity related. """
t_yellow_led = Pin(16, Pin.OUT)
t_blue_led = Pin(26, Pin.OUT)
t_red_led = Pin(27, Pin.OUT)
t_green_led = Pin(28, Pin.OUT)

h_red_led = Pin(0, Pin.OUT)
h_yellow_led = Pin(1, Pin.OUT)
h_green_led = Pin(2, Pin.OUT)
h_blue_led = Pin(3, Pin.OUT)

timer = Timer() # This needs to be stated before all of the functions

LEDs = [t_yellow_led, t_blue_led, t_red_led, t_green_led, h_red_led, h_yellow_led, h_green_led, h_blue_led] # Used to turn off all LEDs and create the flashing effect.

def minute(timer):
    while True:
        pwm.duty_u16(32768)
        sleep(1)
        pwm.duty_u16(0)
        sleep(1)
        
""" As you can see, I changed the start_buzzer function to be a little bit more readable and accurate with the function use. The stop_buzzer function will stop the timer and turn any buzzer off when the temperature or humidity naturally change. """
def start_buzzer(freq=800, period_ms=60000):
    timer.init(mode=Timer.PERIODIC, period = period_ms, callback=minute)
    
def stop_buzzer():
    timer.deinit() # Turns off the timer
    pwm.duty_u16(0)

def condition_read():
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi))
    print()

""" I'll use this function as the example for the other three. The LED functions how have a t=false and h=false attached to them which will be resolved in the main loop to see what LEDs will turn on. Then it will turn on the selected LED. """
def too_high(t=False, h=False): # Both are originally set to false though can be changed in the main loop.
    pwm.freq(800)
    start_buzzer(freq=800, period_ms=60000)
    if t: # This correlates to if t or h is true from the main loop
        t_red_led.value(1)
    if h:
        h_red_led.value(1)
        
def warning(t=False, h=False):
    stop_buzzer()
    if t:
        t_yellow_led.value(1)
    if h:
        h_yellow_led.value(1)  
    
def just_right(t=False, h=False):
    stop_buzzer()
    if t:
        t_green_led.value(1)
    if h:
        h_green_led.value(1)    
    
def too_low(t=False, h=False):
    pwm.freq(500)
    start_buzzer(freq=800, period_ms=60000)
    if t:
        t_blue_led.value(1)
    if h:
        h_blue_led.value(1)
      

while True:
    for x in LEDs:
        (x).value(0) # This turns off all LEDs, ready for another cycle of reading

    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    condition_read()
    
    """ Here is the main if/else tree. Depending on the temperature and humidity will depend on what function is chosen and allow their respective LED. """
    if temp > 22:
            too_high(t=True) # Sets this to true so that the specific LED turns on
    elif temp == 22 or temp == 15:
            warning(t=True)
    elif 15 > temp > 22:
            just_right(t=True)
    elif temp < 22:
            too_low(t=True)
            
    if humi > 60:
            too_high(h=True)
    elif 30 >= humi >= 35 or 55 >= humi >= 60:
            warning(h=True)
    elif 35 > humi > 55:
            just_right(h=True)
    elif humi < 30:
            too_low(h=True)
            
    sleep(2) # This has been moved to the end to allow for a full, uninterupted loop

""" This update was huge, allowing for change in LEDs every 2 seconds, allowance to turn the buzzer off, and most importantly, the ability to view the state of both temperature and humidity seperately. """
```
10/11 Test Cases complete. Hardest one left.
### Test 4: Sound Detection & Final Cleanup
``` Python
""" This code is the final one for my project to fully work. There were three main things that were achieved in this. Firstly, I switched out the yellow LEDs for the RGB (using a combination of red and green) to clean up the code. I got the RGB information from https://randomnerdtutorials.com/electronics-basics-how-do-rgb-leds-work/. 
The second thing I did was the inclusion of a second buzzer for humidity, which the code was difficult to work through, so eventually I created two different pathways for the two buzzers.
The final and most important addition in this test was the completion of the final test case - the sound sensor. This was done with interrupts (learnt from: https://randomnerdtutorials.com/raspberry-pi-pico-interrupts-micropython/) so that the sound buzzer could detect claps throughout the loop instead of at a specific time. """
from machine import Pin, PWM, Timer
from utime import sleep
from dht import DHT11

digital = Pin(18, Pin.IN, Pin.PULL_UP) # Sound sensor pin
dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))

pwm1 = PWM(Pin(13))
pwm1.duty_u16(0)
pwm2 = PWM(Pin(9)) # Inclusion of second buzzer
pwm2.duty_u16(0)

""" As you can see here, there is just blue, red and green, as yellow can be made from a combination of red and green, freeing up space. """
t_blue_led = Pin(26, Pin.OUT)
t_red_led = Pin(27, Pin.OUT)
t_green_led = Pin(28, Pin.OUT)

h_red_led = Pin(15, Pin.OUT)
h_green_led = Pin(12, Pin.OUT)
h_blue_led = Pin(11, Pin.OUT)

buzzerstart1_timer = Timer()
buzzerstart2_timer = Timer() # This, along with the two below, were created to seperate the temperature and humidity flows. 
buzzerwait_timer = Timer()
buzzer1_on = False
buzzer2_on = False
buzzer_silenced = False
clap_silenced = False


LEDs = [t_blue_led, t_red_led, t_green_led, h_red_led, h_green_led, h_blue_led]

def all_leds_off():
    for x in LEDs:
        (x).value(0)

""" With these next 8 functions, they are the same as the other one with the linking name, but one flow is for the temperature (the ones) and the other is for the humidity (the 2s). This allows for the use of two buzzers at once depending on the circumstances. I added some functions to better handle this process. 
- The toggle_buzzer functions create the beeping sound instead of a straight, uninterrupted one
- The minute functions have been adapted to act as the beeping periods for the buzzer.
- The start_buzzer and stop_buzzer functions stayed mostly similar except that they removed the global variable and focused on individual ones - the buzzer_on variables. """
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
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer1) # Signifies the period in between beeping and stopping.
    
def minute2(timer):
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=500, callback=toggle_buzzer2)
    
def start_buzzer1():
    global buzzer1_on
    buzzer1_on = True # Restates a variable
    buzzerstart1_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute1)
    
def start_buzzer2():
    global buzzer2_on
    buzzer2_on = True
    buzzerstart2_timer.init(mode=Timer.PERIODIC, period=60 * 1000, callback=minute2)  
    
def stop_buzzer1():
    global buzzer1_on
    buzzer1_on = False # Restates a variable, but only after a clap has been detected or the temperature/humidity has changed
    buzzerstart1_timer.deinit()
    pwm1.duty_u16(0)
    
def stop_buzzer2():
    global buzzer2_on
    buzzer2_on = False
    buzzerstart2_timer.deinit()
    pwm2.duty_u16(0) 
    
""" This function and the cooldown function go hand-in-hand: the minute_5 is initiated after 5 minutes of buzzer silence and no claps, which allows for the continuation of buzzers afterwards. """
def minute_5(timer):
    global buzzer_silenced, clap_silenced
    buzzer_silenced = False # Allows for claps and buzzers to work again
    clap_silenced = False
    
def cooldown():
    buzzerwait_timer.init(mode=Timer.ONE_SHOT, period=5 * 60 * 1000, callback=minute_5) # This means that the minute_5 function only occurs after 5 minutes of this timer being active

""" This function acts as the gateway to all other functions related to the clapping of hands, and also to the line below about irq. When a clap is detected, this function is put to use and as long as you can still clap, everything but the leds and sensor is turned off with the cooldown function """
def sound_detected(pin):
    global clap_silenced, buzzer_silenced
    if clap_silenced == False: # Ensures that this doesn't happen in the 5 minute break between claps, before running many functions
        buzzer_silenced = True
        clap_silenced = True
        stop_buzzer1()
        stop_buzzer2()
        cooldown()

digital.irq(trigger=Pin.IRQ_RISING, handler=sound_detected) # This is an interrupt that, when the trigger is activated, the loop goes through the handler, in this case the sound_detected function

""" For the too_high and too_low functions, the ability to activate the buzzer of their specific sensor is given as long as a cooldown is not taking place. Otherwise, the option is always given for the turning off of the respective buzzers in the warning and just_right functions. """
def too_high(t=False, h=False):
    if t: 
        if buzzer_silenced == False: # Only works if the cooldown timer is not on
            pwm1.freq(800) # Now the buzzer options are locked between what the sensor reads, instead of activating no matter the occasion (due to the one buzzer)
            start_buzzer1()
        t_red_led.value(1)
    if h:
        if buzzer_silenced == False:
            pwm2.freq(800)
            start_buzzer2()
        h_red_led.value(1)

def warning(t=False, h=False):
    if t:
        stop_buzzer1() # Instead of being kept behind a True/False variable, these next two functions always use the stop_buzzer functions as it doesn't impact anything even with the buzzer silenced
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

""" The main loop remained the same. """
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
""" Additionally, I removed the condition_read function as it was only being used once and the temp and humi variables otherwise weren't defined. It could've been implemented, but it wouldn't affect anything major. """
```
All test cases complete. Now onto the evaluation.
## Test Case Evaluations
### Test Cases 1 and 6: too_high() Function:
The too_high function was probably used the most out of any of the test cases. This was due to two things: my implementation of it first and the humidity levels that regularly exceeded 60%. Because of this, this function always worked perfectly from the get-go, as did all of the LED functions. In relation to the code, the red LED on the first RGB was originally quite dim, so I had to use a lower resistor to allow for a better output. In relation to the original test cases, it perfectly fulfulled all of the necessary requirements, and with the inclusion of a second LED, both can now work seamlessly side-by-side.
### Test Cases 2, 4, 7 and 9: warning() Function:
The warning function was originally not going to make it into the code - it could've just been too hot, too cold and just right. However, I felt it was important for the user to get a more specific sense of where the temperature and humidity were at, instead of the light going straight from green to red or blue. This test case and the just_right function was difficult to correct especially in the making of the second buzzer (as the variables from humidity often crossed into temperature, and vice versa). In terms of the code, the yellow led was the most frustrating to work out because the RGB left it out (despite yellow being a primary colour). Thankfully, I researched a solution and now the code is much cleaner and easier to understand in case something wasn't working. There's nothing to complain about - this test case worked perfectly, however an improvement would be to have different shades of yellow to signify either the increase or decrease of environmental factors (however this wouldn't have been optimal for a Year 9 mech project).
### Test Cases 3 and 8: just_right() Function:
There isn't much to talk about when it comes to this function - it basically mirrored the code for the warning function, except that it was significantly easier to make because of the green function on the RGB led. Due to this, all of the things that were said for the code of the warning function retains its meaning in this function. The green led was the most used by the temperature, proving that the temperature range made sense in the context of the project and issue of moisture. This range was obviously inspired by Mr Scott's sample code on his temperature test, while mine was broadened as humidity was the more pressing concern in this mechatronics project. Again, the test cases worked without issue and there is a seamless transition between this and the warning function labeled above.
### Test Cases 5 and 10: too_low() Function:
Out of all the test cases I tested, these two were the hardest to debug. The temperature rarely dipped below 15 degrees in the day, and even at night it would have to be around ten o'clock before I could really see some progress. And the humidity never got below the green at all due to the higher-than-average green zone we created, a short-sighted mistake on my behalf, however not impacting the project that much. This was the least-used colour out of all four, and most of the changes to this function was first solved with the too_high function. However there was one prominent feature to test for these cases: the frequency of the buzzer. In the original test cases I wanted to make sure that there was a noticeable difference between the buzzer noises of too_high and too_low, even though the LED was there (the scenario could be for someone who is blind). Therefore, I created a lower frequency, not too low that it's quiet but not too high that it is commonly mistaken with the too_high buzzer. This concluded the LED test cases - this one worked successfully, though a definite improvement is to change the scale so that it dabbles into the too_high and too_low functions for an equal amount of time.
### Test Case 11: clap_detect() Function:
This was most important test case of them all, which was why I put it in its own full test. The entire purpose of my solution was to create something that wouldn't require touch. No one wants to get out of what they're doing to turn an annoying buzzer off - so why don't they just clap to turn it off? Looking back, the test case is far too specific. The device can definitely detect something in that range, sure, but it can also detect anything louder. I should've rewritten the test case instead as 'sensitive enough so that a clap is still detected from 3 metres away' instead of going into volume, because volume changes over distances. However, the general idea of it succeeded - I managed to create a working system, and at the end of it, an easy way to turn it off. All of my credit goes to this site: https://sensorkit.joy-it.net/en/sensors/ky-038 and the help of my teammate Lucas to make sure the wires were in the right position - something even a Year 11 overlooked.

There could be many improvements to be made with this device. It could temporarily turn off leds. There could be an additional buzzer to turn the claps and buzzers back on early in case someone was in a rush. However, my test case was almost perfectly completed (not including the hertz range), and the very completion of this is credit enough - I have removed the requirement to use touch for the turning off of a robot. If there was one thing I'd improve or add, it would be a way to fully turn off the system for events such as nighttime, but that's a job for the stop button.
# Evaluation
## Peer Evaluations
| Person | Plus | Minus | Evaluation |
|----------|----------|----------------| ----- |
| Michael | System functions as planned, audibly outputting a buzzer and flashing lights which did alert me to the risk of mold. The clap detection system being a very cool feature, to replace a button, working without latency. There are many different modes for different detections of temperature/humidity. | Although the clap detection system is cool, it is also unnecessary, as it does the same job as a button. The 4 LED modes are quite complicated. | The system does its job and presents cool features to deactivate the systems, and functions forever. The many detection modes and there LED outputs give it a large use case in preventing mold. The LED modes being complicated however does make it hard to understand from someone who didn’t write the code. |
| Ronav | Ur system is functional like it is able to detect temperature and humidity accurately, it buzzes and alerts the user of humidity and temp which is useful and is able to display on LEDs the status. | However Im you thing I feel u could have changed the hard wiring a bit like adding resistors and increase the reaction speed of the device. | Amazing project it is functional and works well, LEDs are able to convey status of the project, buzz is able to alert and this system doesnt malfunction which is amazing. |
## Final Evaluations:
### Final Test in Relation to Functional Criteria
My final test very accurately related to the functional criteria that I originally created, with additional parts that enhanced my robot. All LEDs work in sync with each other, changing to fit the sensor every two seconds (it would've been more beneficial if it could read the temperature and humidity faster, but the sensor physically can't). An improvement that could've been made was to specify the sound range so no extremely loud sounds turned off the system entirely. Many additions or tweaks were made to improve the system - the timer set after a clap was detected changed from 10 minutes to 5 minutes to still allow time to fix temperature and humidity while keeping it brief; and an additional warning switch was made between 30 and 35 percent for humidity so that the sensor wouldn't go from red directly into green, or vice versa. One thing that wasn't directly in the functional requirements but remained important was the link back to the issue of mould which should've been researched more.

Overall, my final test fulfilled nearly all of the functional criteria well, and even though there are some things that didn't go accordingly, the addition of the extra warning range and timer change helped enhance the final test in relation to my functional requirements.
### Final Test in Relation to Non-Functional Criteria
Compared to my Functional Requirements, less of my non-functional criteria was met, though some areas boasted better results than originally anticipated. However, some of the requirements couldn't be tested properly or fell short in their capability. In terms of response time especially, factors such as staying on all day wasn't measured, meaning that I don't know the outcome of that requirement. However, I can predict that it would stay on as long as the laptop is charging as the sensor is occurring. In terms of the LED attached to the GPIO pins, I don't think I understood how sensors worked at the time, because all of the sensors required a GPIO pin. 

Negatives aside, my response time section ended up being exceeded in the final test with my 2-second interval between reads (over double the speed of the original requirement) and a sound that would detect every moment the LED was on (technically faster than 0.1 seconds, but neither mattered that much). Again though, in terms of the accuracy requirements, I fell short in two of the three key areas: my temperature and humidity reading was to the nearest whole number instead of decimal place and the sound sensor couldn't detect the difference between a sharp clap and a loud music video playing. Thankfully, the clap time requirement was met and even shortened to allow for faster intervals in between. 

In terms of implications and changes, I'd definitely improve the accuracy and efficiency of this robot, especially for more precise tasks such as the correct sound detection. However, I also have to remember that this is a Year 9 Mechatronics test and I might've made the requirements too advanced for my current level. The main takeaway for improvement in the non-functional requirements is to specify the temperature and humidity more to ensure that the final test accordingly related to its specific need without simplifying logic.
### Final Performance in Relation to Identified Need
This was a tough one to evaluate, because there isn't supposed to be any written information for the user - instead it is purely a robot and the code used to work it. Originally I had the idea to research ways to increase or decrease temperature and humidity, and you can see the beginning of that code with the issues in the first test. My identified need was to stop the spread of mound, and in many ways my robot meets that need. It outputs temperature and humidity seperately, letting you know when its entering its respective danger zone with different buzzer frequencies. It allows you to clap to turn it off, maximising accessibility. However none of these directly contribute to the stopping of moisture if a regular user is using this system. 

The final performance in relation to my need was the area whose requirements were fufilled the least. One of the main points issued in the identified need was the ability to turn this system off at night, however that was never implemented and the user must use the regular stop button or unplug the device entirely. In terms of the first part though, the LEDs are an excellent way of showing the different temperature and humidity levels without having to read, and the buzzers add another sense to benefit people with seeing disabilities or those that are concentrated in what they're doing and aren't frequently watching the LED. Overall, the identified need could definitely be improved by focusing more on the primary issue instead of the coding and wiring.
### Project in Relation to Project Management
Project Management was the easiest area to talk about, and this was because of the inconsistent commits and lazy early few weeks that created a stressful final week. For starters, I didn't do any extra work in the first few weeks, while I should've got more done and started the testing earlier so that I had more wiggle space. Sure, my efficiency this week was great, but it could've been spread over more weeks and alleviated some of the anxiety I've felt about the submission of the project. Being sick also didn't support my cause. 

In the first week, I worked through the first section with ease, but never did more than I needed to. In the second week I felt myself slipping away from the desired point in time I should've been at, especially considering the complexity of my project. When I began my Developing in the third week, I was days behind, and combined with studying for other tests, I've stayed behind progress until today, as I'm writing this evaluation. To give credit where credit's due, I have kept a consistent dedication to making sure that I got all of the necessary parts, even buying myself and my partner Lucas sensors that the school didn't have a week before the due date, so that I had enough time to test and debug. Again though, I should've started that process around the Week 3 weekend instead of late in Week 4, as it would've allowed me to take a more relaxed approach to this assignment.
### Project in Relation to Peer Feedback
My peers gave me very similar positive responses, and minor changes that I should take into consideration. One commended me on my code and the minority of lines I needed to get it working, which I was looking out for as I tried to make my code more efficient. The relationship between the buzzer and the LED was also talked about in a positive fashion, including the cool feature that the sound sensor brings. For their negatives, they had very different things to improve on. One was relating to the reaction time and adding resistors to better suit non-functional requirements, while the other found the LED system slightly confusing and found the sound sensor cool but useless when replaced with a buzzer. While I value these opinions, I don't think I explained well enough in my requirements outline that I wanted the sound sensor to act as an easier way for people to turn something off instead of a button that would force people to go over and turn it off by hand instead of just clapping to cease the buzzer. I do agree with the increase in efficiency, which only couldn't be done due to the sensor I was using. 

However, their implications were valid - both the implication of better sensors, such as the individual temperature and humidity sensors or an active buzzer instead of a piezo, and the complex LED system that would make a normal user confused. Next time, I would focus on more of the aesthetic and cleanliness of the wires and utilisation of the standard RGB, as well as putting the respective buzzer on either side to ensure that the system is better understood.
### Future Improvements to Final Product
Finally, we end at the future improvements, and most of mine will link to better use of the sensors and tools I was given. For starters, while the code is extremely polished, I'm sure there's a way so that there only needs to be one set of buzzer functions and therefore removing around 40 lines of code, however that would be the only improvement with the base code. Non-Functional requirements would also try to be fulfilled instead of ignoring them immediately after writing them.

In terms of management, I would try to complete the earlier parts faster and move on to the main aspect of the code earlier on, like I did in the first test to feel more at ease with my position in the project instead of what I felt this week, trying to fit in the latter half of Testing and Debugging as well as the entire Evaluation segment. 

One of the main things I'd improve is relating more to the identified need instead of the code and wiring that I was more focused on. Of course, this was a Year 9 project, and mold prevention is a hard topic to try and fix with a temperature and humidity sensor, however with a greater knowledge of the material through research, I'd be able to better use those sensors particularly for the main idea. 

For the wiring, I would try and prioritise minimal use of wires, instead opting for external sensors to make the system more pronounced, or simplifying the idea so that the code doesn't require multiple different sensors. I'd make sure there's a clear difference between the temperature and humidity instead of sticking buzzers on the same side and using different placed RGB LEDs to help the normal user understand it better.

Functionality is always an important part of the project, sometimes the most important. I'd prioritise better sensors that read faster for better response time, output numbers with decimal points for better accuracy, and use more long-lasting, certified sensors for better reliability. I'd ensure that all sensors are equally as important and all contribute to the idea instead of just making a cool gimmick.

However in my opinion, the most important thing for me to improve would be my mindset. I need to get out of the headspace that this is the most important assignment ever, instead treating this as a fun assignment that doesn't need a complex code or innovative idea, because its just a Year 9 Mech Project after all.