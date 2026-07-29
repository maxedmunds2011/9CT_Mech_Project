# Requirements Outline
## The Need
When it is cold and damp, mould has a potential to grow. At night time, rain can also dampen windows or hot air could be stuck inside your bedroom and you wouldn't know about it. I need to create something that will allow me to know when to open and close windows and have a way to turn it off in the night.
## Proposed Solution
The solution that could be implemented is to ake a Raspberry Pi program that includes four primary sensors: a temperature sensor and humidity detector to detect their respective areas, a buzzer when the humidity or temperature reaches a certain level, and a small sound to detect the calpping of hands or other noise. LEDs could also be implemented to show how close the humidity and temperature is to being damp or cold respectively, or as a subtitute to a buzzer. 
## Key Actions
 - Temperature detector detects temperature outside of the designated range. It does this every 5 seconds.
 - A red or blue LED light is turned on depending on if it's above range (red) or below range (blue)
 - Buzzer alerts user of the temperature out of place
 - A clap from the user turns the buzzer off

This can also work for humidity, though it uses the humidity detector
## Functional Requirements
The designated temperature range is 12-20 degrees celsius, as they are the most liveable conditions for sleeping times.
A red LED or high pitched puzzer will turn on when the temperature is above 20 degrees celsius, while a blue LED or low pitched buzzer will turn on when the temperature is below 20 degrees celsius. The LED will be green only when allowed to be (in the daytime) from 9am to 7pm, when it detects the accurate temperature range.
The temperature range could change depending on the time of day, from 12-20 degrees celsius at night and 18-26 degrees celsius during the day.
## Test Cases

## Non-Functional Requirements

# Algorithms

# Development and Integration

# Testing and Debugging

# Evaluation