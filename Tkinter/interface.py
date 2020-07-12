import tkinter as tk
import paho.mqtt.client as mqtt
import requests
import config

window = tk.Tk()
window.geometry("300x100")
window.title("IoT Antitheft")
window.resizable(False, False)

alarm_active = False

ALARM_DEACTIVATED_TEXT = "Your home is safe"
ALARM_ACTIVATED_TEXT = "Alarm!"

def telegram_bot_sendtext(bot_message):
    bot_token = config.BOT_TOKEN
    bot_chatID = config.BOT_CHATID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def place_label(label, short=False):
    if short:
        label.place(relx=0.38, rely=0.01)
    else:
        label.place(relx=0.13, rely=0.01)

def hide_widget(widget):
    widget.place_forget()

def change_label_text(label, text):
    label['text'] = text

def change_label_color(label, color):
    label['fg'] = color

def activate_alarm():
    global alarm_active
    alarm_active = True
    telegram_bot_sendtext("L'allarme è stato attivato!")
    change_label_text(alarm_label, ALARM_ACTIVATED_TEXT), 
    change_label_color(alarm_label, "red"), 
    place_label(alarm_label, True), 
    hide_widget(activate_alarm_button)
    deactivate_alarm_button.place(relx=0.35, rely=0.5)

def deactivate_alarm():
    global alarm_active
    alarm_active = False
    telegram_bot_sendtext("Hai disattivato l'allarme")
    change_label_text(alarm_label, ALARM_DEACTIVATED_TEXT), 
    change_label_color(alarm_label, "green"), 
    place_label(alarm_label), 
    hide_widget(deactivate_alarm_button)
    activate_alarm_button.place(relx=0.35, rely=0.5)

alarm_label = tk.Label(window, text=ALARM_DEACTIVATED_TEXT, fg="green", font=("Helvetica", 20))
place_label(alarm_label)

activate_alarm_button = tk.Button(text="Activate alarm", command=lambda: [activate_alarm(), publish_activated()])
activate_alarm_button.place(relx=0.35, rely=0.5)

deactivate_alarm_button = tk.Button(text="Deactivate alarm", command=lambda: [deactivate_alarm(), publish_deactivated()])

def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("receving ", msg)
    if msg == "Alarm is active" and not alarm_active:
        activate_alarm()
    elif msg == "Alarm is deactive" and alarm_active:
        deactivate_alarm()

def publish_activated():
    if client.is_connected:
        try:
            client.publish("alex/alarm_command", "Activate alarm", 1, retain=True)
            print("publishing 'Activate alarm' on alex/alarm_command")
        except Exception as e:
            print(e)

def publish_deactivated():
    if client.is_connected:
        try:
            client.publish("alex/alarm_command", "Deactivate alarm", 1, retain=True)
            print("publishing 'Deactivate alarm' on alex/alarm_command")
        except Exception as e:
            print(e)
        

print("creating new instance")
client = mqtt.Client() #create new instance
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect("test.mosquitto.org") #connect to broker

print("Subscribing to topic alex/alarm_state")
client.subscribe("alex/alarm_state")

#Start the MQTT Mosquito process loop
client.loop_start() 

if __name__ == "__main__" :
    window.mainloop()