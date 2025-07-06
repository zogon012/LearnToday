import json
import time
import paho.mqtt.client as mqtt
import taos

conn = taos.connect()
cursor = conn.cursor()
cursor.execute("""CREATE DATABASE IF NOT EXISTS benchmark;""")
cursor.execute("""USE benchmark;""")
cursor.execute("""CREATE STABLE IF NOT EXISTS sensor_data(ts TIMESTAMP, value FLOAT) TAGS(location BINARY(64));""")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    ts = data["timestamp"]
    value = data["value"]
    sql = f"INSERT INTO d1 USING sensor_data TAGS('lab') VALUES({ts}, {value})"
    try:
        cursor.execute(sql)
        print("Inserted:", sql)
    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.connect("mosquitto", 1883, 60)
client.subscribe("sensor/tdengine")
client.on_message = on_message
client.loop_forever()
