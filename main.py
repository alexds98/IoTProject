# IoTProject-antitheft
# Created at 2020-07-09 07:32:47.478880

import streams
import adc
import pwm
import hcsr04

streams.serial()

PASSWORD = "abba"
entered = ""

# set alarm led for digital write
alarm_led_pin = D23
pinMode(alarm_led_pin, OUTPUT)

# set potentiometer for analog read
pot_pin = A4
pinMode(pot_pin, INPUT_ANALOG)

# set buzzer for pwm
buzzer_pin = D22
buzzer_pwm_pin = D22.PWM
pinMode(buzzer_pin, OUTPUT)

# set photoresistor for analog read
phr_pin = A7
pinMode(phr_pin, INPUT_ANALOG)

# set dark led for digital write
dark_led_pin = D21
pinMode(dark_led_pin, OUTPUT)

# set board button as input with pullup built-in resistor
dark_btn_pin = BTN0
pinMode(dark_btn_pin, INPUT_PULLUP)

# set button 1 as input with pulldown built-in resistor
pass_btn1 = D19
pinMode(pass_btn1, INPUT_PULLDOWN)

# set button 2 as input with pulldown built-in resistor
pass_btn2 = D18
pinMode(pass_btn2, INPUT_PULLDOWN)

# set button 3 as input with pulldown built-in resistor
confirm_btn = D5
pinMode(confirm_btn, INPUT_PULLDOWN)

# set trigger pin for hcsr04 as digital output
trigger_pin = D17
pinMode(trigger_pin, OUTPUT)

# set echo pin for hcsr04 as digital input
echo_pin = D16
pinMode(echo_pin, INPUT)

def toggle_dark_mode() :
    global dark_mode
    # print("Toggle")
    dark_mode = not dark_mode

def blink(pin, time_on, time_off) :
        digitalWrite(pin,HIGH)   # turn the led ON by making the voltage HIGH
        sleep(time_on)           # wait for time_on 
        digitalWrite(pin,LOW)    # turn the led OFF by making the voltage LOW
        sleep(time_off)          # wait for time_off
        
def blink_times(pin) :
    pot_value = adc.read(pin)
    # print("pot_value: ", pot_value)
    time_on = 500
    if pot_value < 2047 :
        time_on -= (2047 - pot_value) // 5
    elif pot_value > 2047 :
        time_on += (pot_value - 2047) // 5
    time_off = 1000 - time_on
    # print("time_on: ", time_on, " time_off: ", time_off)
    return (time_on, time_off)
        
def pot_led_thread(led_pin, pot_pin) :
    global alarm
    while True :
        time_on, time_off = blink_times(pot_pin)
        blink(led_pin, time_on, time_off)
        if not alarm :
            break
        
def buzzer_alarm(pwm_pin) :
    INITIAL_FREQUENCY = 800
    VARIATION = 39
    frequency = INITIAL_FREQUENCY
    mode = 1
    global alarm
    while True :
        # print("frequency: ", frequency)
        period = 1000000//frequency
        pwm.write(pwm_pin, period, period//2, MICROS)
        if mode == 1 :
            frequency += 4
        else :
            frequency -= 4
        if frequency < INITIAL_FREQUENCY - VARIATION :
            mode = 1
        elif frequency > INITIAL_FREQUENCY + VARIATION :
            mode = 0
        if not alarm :
            pwm.write(pwm_pin, 0, 0)
            break
        sleep(25)
        
def light_in_dark(phr_pin, led_pin) :
    global dark_mode
    while True :
        if dark_mode :
            phr_value = adc.read(phr_pin)
            # print("phr_value: ", phr_value)
            if phr_value < 1500 :
                digitalWrite(led_pin, HIGH)
            else :
                digitalWrite(led_pin, LOW)
            sleep(500)
        else :
            digitalWrite(led_pin, LOW)
            sleep(500)
            
def update_entered(button_number) :
    global entered
    global alarm
    print("button ", button_number, " pressed")
    if alarm :
        if button_number == 1 :
            entered += "a"
        elif button_number == 2 :
            entered += "b"
        
def clear_entered() :
    global entered
    entered = ""

def check_password() :
    global entered
    global PASSWORD
    global alarm
    print("confirm button pressed")
    if alarm :
        if entered == PASSWORD :
            print("Correct password, stopping alarm")
            stop_alarm()
        else :
            clear_entered()
            print("Incorrect password")
        
def stop_alarm() :
    global alarm
    alarm = False
    clear_entered()
    
def start_alarm() :
    global alarm
    alarm = True
    thread(pot_led_thread, alarm_led_pin, pot_pin)
    thread(buzzer_alarm, buzzer_pwm_pin)
    thread(light_in_dark, phr_pin, dark_led_pin)

# on button pressed i activate/deactivate dark mode
onPinFall(dark_btn_pin, toggle_dark_mode)

# handling password buttons
onPinFall(pass_btn1, update_entered, 1)
onPinFall(pass_btn2, update_entered, 2)
onPinFall(confirm_btn, check_password)

alarm = False
dark_mode = True
thread(pot_led_thread, alarm_led_pin, pot_pin)
thread(buzzer_alarm, buzzer_pwm_pin)
thread(light_in_dark, phr_pin, dark_led_pin)
while True :
    distance = hcsr04.calculate_distance(trigger_pin, echo_pin)
    print(distance)
    if distance > 0.0 and not alarm:
        start_alarm()
    sleep(1000)    
