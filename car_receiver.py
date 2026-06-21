print("🚀 car_receiver.py started")

import os
import sqlite3
import datetime
import warnings
import paho.mqtt.client as mqtt
import json

print("📁 Current working directory:", os.getcwd())
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Database setup
db_path = "traffic_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS traffic (
        timestamp TEXT,
        location TEXT,
        status TEXT,
        speed_limit INTEGER
    )
""")
conn.commit()

# Decision logic
def car_action(data):
    status = data.get("status")
    speed = data.get("speed_limit")
    if status == "Jam":
        print("🚗 Car is rerouting...")
    elif status == "Accident":
        print("🚨 Car is stopping...")
    elif status == "Clear":
        print(f"🚙 Car is moving at {speed} km/h")
    else:
        print("⚠️ Unknown traffic status received.")

# Message callback
def on_message(client, userdata, message):
    try:
        raw = message.payload.decode()
        print("📩 Raw message received:", raw)
        data = json.loads(raw)
        print("📦 Parsed data:", data)
        car_action(data)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO traffic VALUES (?, ?, ?, ?)", (
            timestamp,
            data.get("location"),
            data.get("status"),
            data.get("speed_limit")
        ))
        conn.commit()
        print("✅ Data saved to database.\n")
    except Exception as e:
        print("❌ Error processing message:", e)

# MQTT setup
print("🔧 Setting up MQTT client...")
client = mqtt.Client()
client.on_message = on_message

try:
    print("🔌 Connecting to broker...")
    client.connect("test.mosquitto.org", 1883)
    print("📶 Subscribing to topic...")
    client.subscribe("traffic/data")
    print("📡 Listening for traffic updates on 'traffic/data'...\n")
    client.loop_forever()
except Exception as e:
    print("❌ MQTT setup failed:", e)

print("✅ End of script reached")
input("✅ Script finished. Press Enter to exit...")

