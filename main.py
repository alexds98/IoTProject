# IoTProject-antitheft
# Created at 2020-07-09 07:32:47.478880

import streams
import adc

streams.serial()

# set alarm led for digital write
alarm_led_pin = D23
pinMode(alarm_led_pin, OUTPUT)

# set potentiometer for analog read
pot_pin = A4
pinMode(pot_pin, INPUT_ANALOG)

def blink(pin, time_on, time_off) :
        digitalWrite(pin,HIGH)   # turn the led ON by making the voltage HIGH
        sleep(time_on)           # wait for time_on 
        digitalWrite(pin,LOW)    # turn the led OFF by making the voltage LOW
        sleep(time_off)          # wait for time_off
        
def blink_times(pin) :
    pot_value = adc.read(pin)
    # print(pot_value)
    time_on = 500
    if pot_value < 2047 :
        time_on -= (2047 - pot_value) // 5
    elif pot_value > 2047 :
        time_on += (pot_value - 2047) // 5
    time_off = 1000 - time_on
    # print("time_on: ", time_on, " time_off: ", time_off)
    return (time_on, time_off)
        
def pot_led_thread(led_pin, pot_pin) :
    global stop
    while True :
        time_on, time_off = blink_times(pot_pin)
        blink(led_pin, time_on, time_off)
        if stop :
            break
        
stop = False
thread(pot_led_thread, alarm_led_pin, pot_pin)
