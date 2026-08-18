from machine import Pin, PWM, Timer
from utime import sleep
from dht import DHT11

digital = Pin(18, Pin.IN, Pin.PULL_UP)
dht11_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))

pwm1 = PWM(Pin(13))
pwm1.duty_u16(0)
pwm2 = PWM(Pin(9))
pwm2.duty_u16(0)

t_blue_led = Pin(26, Pin.OUT)
t_red_led = Pin(27, Pin.OUT)
t_green_led = Pin(28, Pin.OUT)

h_red_led = Pin(15, Pin.OUT)
h_green_led = Pin(12, Pin.OUT)
h_blue_led = Pin(11, Pin.OUT)

buzzerstart_timer = Timer()
buzzerwait_timer = Timer()
clap_timer = Timer()
buzzer_on = False
led_active = True
led_timer = Timer()
buzzer_silenced = False
clap_active = True

t_buzzer = False
h_buzzer = False

LEDs = [t_blue_led, t_red_led, t_green_led, h_red_led, h_green_led, h_blue_led]

def all_leds_off():
    for x in LEDs:
        x.value(0)

def clap_detect():
    global clap_active
    if clap_active == True:
        return digital.value() == 1 

def toggle_buzzer(timer):
    if pwm1.duty_u16() == 0:
        pwm1.duty_u16(32768)
    else:
        pwm1.duty_u16(0)
    if pwm2.duty_u16() == 0:
        pwm2.duty_u16(32768)
    else:
        pwm2.duty_u16(0)

def minute(timer):
    buzzerstart_timer.init(mode=Timer.PERIODIC, period=1000, callback=toggle_buzzer)
    
def minute_5(timer):
    global buzzer_silenced
    buzzer_silenced = False

def sixth_minute(timer):
    global clap_active, led_active
    clap_active = True
    led_active = True
    
def buzzer_cooldown():
    global buzzer_silenced
    buzzer_silenced = True
    buzzerwait_timer.init(mode=Timer.ONE_SHOT, period=5 * 60 * 1000, callback=minute_5)
    
def clap_cooldown():
    global clap_active
    clap_active = False
    clap_timer.init(mode=Timer.ONE_SHOT, period=10 * 1000, callback=sixth_minute)

def start_buzzer():
    global buzzer_on
    buzzer_on = True
    buzzerstart_timer.init(mode=Timer.ONE_SHOT, period=60 * 1000, callback=minute)

def stop_buzzer():
    global buzzer_on
    buzzer_on = False
    buzzerstart_timer.deinit()
    pwm1.duty_u16(0)
    
def stop_led():
    all_leds_off()
    led_active = False
    led_timer.init(mode=Timer.ONE_SHOT, period=10 * 1000, callback=sixth_minute)

def condition_read():
    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()
    print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, humi))
    print()
    return temp, humi

def too_high(t=False, h=False):
    pwm1.freq(800)
    if buzzer_on == False:
        start_buzzer()
    if led_active == True:
        if t:
            t_red_led.value(1)
        if h:
            h_red_led.value(1)

def warning(t=False, h=False):
    if t_buzzer == True:
        buzzer_off()
    if h_buzzer == True:
        buzzer_off()
    if led_active == True:
        if t:
            t_red_led.value(1)
            t_green_led.value(1)
        if h:
            h_red_led.value(1)
            h_green_led.value(1)

def just_right(t=False, h=False):
    if t_buzzer == True:
        buzzer_off()
    if h_buzzer == True:
        buzzer_off()
    if led_active == True:
        if t:
            t_green_led.value(1)
        if h:
            h_green_led.value(1)

def too_low(t=False, h=False):
    pwm1.freq(500)
    if buzzer_on == False:
        start_buzzer()
    if led_active == True:
        if t:
            t_blue_led.value(1)
        if h:
            h_blue_led.value(1)

while True:
    all_leds_off()

    dht11_sensor.measure()
    temp = dht11_sensor.temperature()
    humi = dht11_sensor.humidity()

    print("Temperature: {}°C  Humidity: {}%".format(temp, humi))
    
    if temp > 22:
        t_buzzer = True
        too_high(t=True)  
    elif temp == 22 or temp == 15:
        warning(t=True)
    elif 15 < temp < 22:
        just_right(t=True)
    else:
        too_low(t=True)
        t_buzzer = True

    if humi > 60:
        too_high(h=True)
        h_buzzer = True
    elif (55 <= humi <= 60) or (30 <= humi <= 35):
        warning(h=True)
    elif 35 < humi <= 55:
        just_right(h=True)
    else:
        too_low(h=True)
        h_buzzer = True

    sleep(2)