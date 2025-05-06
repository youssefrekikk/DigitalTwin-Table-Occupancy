import paho.mqtt.publish as publish
import random
import time
import json

BROKER = "mosquitto"  # Docker service name
TOPIC = "/iot/data"

TABLE_IDS = ["table001", "table002", "table003", "table004"]

def generate_table_data(table_id):
    return {
        "id": table_id,
        "temperature": round(random.uniform(20, 28), 1),
        "noiseLevel": round(random.uniform(50, 80), 1),
        "occupied": random.choice([True, False])
    }

while True:
    for table_id in TABLE_IDS:
        payload = generate_table_data(table_id)
        print(f"Publishing for {table_id}: {payload}")
        publish.single(
            topic=TOPIC,
            payload=json.dumps(payload),
            hostname=BROKER
        )
    time.sleep(5)
