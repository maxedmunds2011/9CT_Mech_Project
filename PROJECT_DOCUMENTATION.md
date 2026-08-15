# Requirements Outline
## The Need
When it is cold and damp, mould has a potential to grow. At night time, rain can also dampen windows or hot air could be stuck inside your bedroom and you wouldn't know about it. I need to create something that will allow me to know when to open and close windows and have a way to turn it off in the night.
## Proposed Solution
The solution that could be implemented is to ake a Raspberry Pi program that includes four primary sensors: a temperature sensor and humidity detector to detect their respective areas, a buzzer when the humidity or temperature reaches a certain level, and a small sound to detect the calpping of hands or other noise. LEDs could also be implemented to show how close the humidity and temperature is to being damp or cold respectively, or as a subtitute to a buzzer. 
## Key Actions
 - Temperature Sensor and Humidity Detector detects temperature and humidity respectivelty outside of the designated range. It does this every 5 seconds.
 - A red or blue LED light is turned on depending on if it's above range (red) or below range (blue)
 - Different pitched buzzer sounds alerts user of the temperature or humidity out of place
 - A clap from the user turns the buzzer off
## Functional Requirements
The designated temperature range is 15-22 degrees celsius, as they are the least likely conditions for mould to grow. 

This is paired with a humidity at between 30 - 50%, because mould germinates most in humidity of 60% or more.

Both the temperature and humidity will have a set of LEDs each for distinguishing the difference.

A red LED will turn on when the temperature is above 22 degrees celsius, or when the humidity is above 60%. After one minute without any clap detected, a high-pitched buzzer will turn on as well. This acts as the 'too high' label

A yellow LED will turn on when the temperature is at 15 or 22 degrees celsius or the humidity is between 55% and 60%. This acts as a warning for movement into the red LED areas.

A green LED will turn on and remain on as long as the temperature is between 16 and 21 degrees celsius and the humidity is between 30 and 55%. This acts as the 'just right' label and should be maintained most of the time.

A blue LED will turn on when the temperature is below 15 degrees celsius or the humidity is below 30%. After one minute without any clap detected, a low-pitched buzzer will turn on as well. This acts as the 'too low' label.

A sound sensor detects a clap when the red LED or blue LED are turned on. At a certain noise level the sound sensor will disable all buzzers for 10 minutes to allow time to fix the humidity and temperature levels
## Test Cases
| Test Case | Input     | Expected Output   |
|---------- |---------- |----------------   |
| Temperatue too hot | Temperature sensor reads above 22 degrees celsius | Red LED turns on. after 1 minute a high-pitched buzzer turns on |
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
The robot will need to detect both the temperature and humidity using their respective sensor, doing this every 5 seconds for maximum efficiency. The clap should be detected every 0.1 seconds to ensure a fast and connected correlation. It can't run out of battery or randomly stop working in the middle of the day - it must remain consistently on throughout. All LEDs need to function properly and by themselves, attached to GPIO pins to reserve other pins for more the more important sensors.
### Response Time
The robot should detect the temperature and humidity respectively every 5 seconds for maximum efficiency. The clap should be detected every 0.1 seconds to ensure a fast and connected correlation. 
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

BEGIN warning()
clap_detect()
IF clap_detect RETURNS 'yes' THEN
    OUTPUT yellow_Led.value(1)
END warning()

BEGIN just_right()
clap_detect()
IF clap_detect RETURNS 'yes' THEN
    OUTPUT green_Led.value(1)
END just_right()

BEGIN too_low()
clap_detect()
IF clap_detect RETURNS 'yes' THEN
    OUTPUT red_Led.value(1)
    wait (60)
    OUTPUT low_buzzer.on
END too_low()

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
""" The purpose of this successful test was to see if the sound sensor would work when a sharp sound (like a clap or snap of fingers) would activate a random LED. This is the combination of the future sound sensor and a look at the main loop & how LEDs will react """

from machine import Pin, ADC # Connects the Raspberry Pi pins to Thonny
from time import sleep # Allows for the use of the sleep() function

# Initialization of GPIO18 as input
digital = Pin(18,Pin.IN, Pin.PULL_UP) # This is the setup for the sound sensor
led = Pin(16, Pin.OUT) # This is setup for the test LED
led.value(0) # The LED begins off

print("KY-037 Microphone test")


""" This while loop is reading the environment every 0.1 seconds to check for any sounds, specifically sharp sounds, which will turn the test LED on """

while True: # Continues until break occurs
    digital_value = digital.value() # Creating a variable based on the sound sensor input
    print(digital_value) # Used as a test to see the difference in binary
    if digital_value == 1: # The digital value at 1 represents a noise being made
        led.value(0) # Unsure why, but the (0) in this turns the LED on for 0.1 seconds
        sleep(0.1)
    else:
        led.value(1) # Unsure why, but this keeps the LED off

""" This unsure circumstance between the LED values will be fixed in a later evaluation. """
```
# Testing and Debugging
### Test 1: Too High 
``` Python
""" The first test I'm going to try is the test case of if it is too hot, or humid, a red LED will turn on. We will do the buzzer next once this works. """

from machine import Pin
from utime import sleep
from dht import DHT11

dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
red_led = Pin(27, Pin.OUT)
issue = ""

def condition_read():
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi))
    print()
    sleep(2)

def too_high():
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
```
Both of these test cases worked (2/11 test cases half-complete)

(From now on, I will add to this code until the sound sensor, where I will use my main.py code.)
### Test 2: Too High (with buzzers)
``` Python

```

### Test 3: Other LEDs (Warning, Just Right & Too Low)
``` Python

```

### Test 4: Sound Detection
``` Python

```

### Test 5: Putting it all together
``` Python

```

### Test 6: Cleanup and Quality of Life
``` Python

```

# Evaluation