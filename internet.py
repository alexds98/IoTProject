from lwmqtt import mqtt
from wireless import wifi

SSID = "FASTWEB-77EF88"
PASSWORD = "98KZ76HAYT"

def connect():
    from espressif.esp32net import esp32wifi as wifi_driver
    wifi_driver.auto_init()
    
    
    print("Establishing Link...")
    while True:
        try:
            return wifi.link(SSID, wifi.WIFI_WPA2, PASSWORD)
        except Exception as e:
            print("Wifi Linking failed. Attempting to reconnect...")
        sleep(5000)
    
    
            
class Client(mqtt.Client):
        
    def loop_failure(self):
        print("Loop Failure!")
        while True:
            try:
                if not wifi.is_linked():
                    print("WiFi was not linked. Relinking...")
                    wifi.link(SSID, wifi.WIFI_WPA2, PASSWORD)
                print("Attempting to reconnect...")
                self.reconnect()
                break
            except Exception as e:
                pass
            sleep(5000)
        return mqtt.RECOVERED
        
        
    def __init__(self, client_id, clean_session=True):
        mqtt.Client.__init__(self, client_id, clean_session)
        
    # Method override
    def connect(self, host, keepalive=10, breconnect_cb=None, aconnect_cb=None):
        while True:
            try:
                mqtt.Client.connect(self, host, keepalive, breconnect_cb=breconnect_cb, aconnect_cb=aconnect_cb, loop_failure=self.loop_failure)
                break
            except Exception as e:
                print("connecting...", e)
            sleep(5000)