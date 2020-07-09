import timers

timer = timers.timer()
elapsed = 0

def calculate_distance(trigger_pin, echo_pin) :
        # print("Initialization")
        digitalWrite(trigger_pin, LOW)
        sleep(1)
        digitalWrite(trigger_pin, HIGH)
        sleep(1)
        digitalWrite(trigger_pin, LOW)
        
        while True:
            echo_value = digitalRead(echo_pin)
            if echo_value == 1 :
                timer.start()
                break
            
        while digitalRead(echo_pin) == 1 :
            elapsed = timer.get()
            
        # print("Elapsed time: ", elapsed, " ms")
        distance = elapsed * 34.38 / 2 # velocità del suono nell'aria circa 343.8 m/s cioè 34.38 cm/ms
        # print("Distance: ", distance, " cm")
        return distance