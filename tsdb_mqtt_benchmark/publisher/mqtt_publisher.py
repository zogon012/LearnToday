import threading
import time
import random
import paho.mqtt.client as mqtt
import json

BROKER = "mosquitto"
PORT = 1883
CHANNELS = 10
FPS = 10
DURATION_SEC = 600  # 테스트 시간(초)

def publish_channel(channel_id):
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    topic = f"fire/bbox/channel{channel_id}"
    for _ in range(FPS * DURATION_SEC):
        bbox = {
            "channel": channel_id,
            "timestamp": time.time(),
            "x": random.randint(0, 1920),
            "y": random.randint(0, 1080),
            "w": random.randint(30, 300),
            "h": random.randint(30, 300),
            "score": round(random.uniform(0.8, 1.0), 2),
            "class": "fire"
        }
        client.publish(topic, json.dumps(bbox))
        print(json.dumps(bbox))
        time.sleep(1.0 / FPS)
    client.disconnect()

threads = []
for ch in range(CHANNELS):
    t = threading.Thread(target=publish_channel, args=(ch,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("모든 채널 bbox publish 완료!")
