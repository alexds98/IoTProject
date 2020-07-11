import timers

timer = timers.timer()
counter = 0
elapsed = 0

def calculate_distance(trigger_pin, echo_pin) :
        # print("Initialization")
        digitalWrite(trigger_pin, LOW)
        sleep(1)
        digitalWrite(trigger_pin, HIGH)
        sleep(1)
        digitalWrite(trigger_pin, LOW)
        
        while digitalRead(echo_pin) == 0:
            if counter > 100:
                counter = 0
                return -1.0
            counter += 1
        
        timer.start()
            
        while digitalRead(echo_pin) == 1:
            if counter > 100:
                counter = 0
                return -1.0
            counter += 1
        
        elapsed = timer.get()
            
        # print("Elapsed time: ", elapsed, " ms")
        distance = elapsed * 34.38 / 2 # velocità del suono nell'aria circa 343.8 m/s cioè 34.38 cm/ms
        # print("Distance: ", distance, " cm")
        return distance