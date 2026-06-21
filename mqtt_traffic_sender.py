import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import paho.mqtt.client as mqtt
import time
import json
from traffic_simulator import generate_traffic_data

BROKER = "test.mosquitto.org"
PORT = 1883
TOPIC = "traffic/data"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"🚦 Connected to broker at {BROKER}:{PORT}")
        print("📡 Sending traffic updates every 5 seconds...\n")
    else:
        print(f"❌ Connection failed with code {rc}")

client.on_connect = on_connect

try:
    client.connect(BROKER, PORT)
    client.loop_start()

    while True:
        traffic_data = generate_traffic_data()
        message = json.dumps(traffic_data)  # ✅ Proper JSON format
        result = client.publish(TOPIC, message)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"📤 Sent to '{TOPIC}':", traffic_data)
        else:
            print(f"❌ Failed to send message")
        time.sleep(5)

except Exception as e:
    print("❌ Error connecting to MQTT broker:", e)
