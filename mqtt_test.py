import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print("📩 Message received:", message.payload.decode())

client = mqtt.Client()
client.on_message = on_message

client.connect("test.mosquitto.org", 1883)
client.subscribe("traffic/data")
print("📡 Listening for traffic updates...")
client.loop_forever()
