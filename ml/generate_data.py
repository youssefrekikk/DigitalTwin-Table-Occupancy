import pandas as pd
import random
from datetime import datetime, timedelta

TABLE_IDS = ["table001", "table002", "table003", "table004"]

rows = []
for _ in range(500):  # Generate 500 occupancy events
    table_id = random.choice(TABLE_IDS)
    start = datetime(2024, 5, 1) + timedelta(minutes=random.randint(0, 10000))
    duration = random.randint(5, 120)  # in minutes
    end = start + timedelta(minutes=duration)
    temperature = round(random.uniform(20, 28), 1)
    noiseLevel = round(random.uniform(50, 80), 1)
    occupied = True  # Since this is an occupancy event
    deviceCount = random.randint(1, 4)
    timestamp = start.isoformat() + "Z"

    rows.append({
        "table_id": table_id,
        "start_time": start.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": duration,
        "temperature": temperature,
        "noiseLevel": noiseLevel,
        "occupied": occupied,
        "deviceCount": deviceCount,
        "timestamp": timestamp
    })

df = pd.DataFrame(rows)
df.to_csv("./data/occupancy.csv", index=False)
print("✅ Historical data with features saved to ../data/occupancy.csv")
