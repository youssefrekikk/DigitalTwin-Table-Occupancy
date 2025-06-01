from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import BackgroundTasks
import os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import threading
import joblib

MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_TOPIC = "/iot/data"

# MongoDB setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["digitaltwin"]
table_status_col = db["table_status"]
historical_col = db["table_history"]

# ML model loading (lazy)
ml_model = None
ml_encoder = None

def load_ml():
    global ml_model, ml_encoder
    if ml_model is None or ml_encoder is None:
        try:
            ml_model = joblib.load("/app/../ml/wait_time_model.pkl")
            ml_encoder = joblib.load("/app/../ml/table_id_encoder.pkl")
        except Exception as e:
            print("ML model not loaded:", e)
            ml_model, ml_encoder = None, None

def predict_wait_time(table_id):
    load_ml()
    if ml_model and ml_encoder:
        try:
            encoded = ml_encoder.transform([table_id])[0]
            predicted = ml_model.predict([[encoded]])[0]
            return round(float(predicted), 2)
        except Exception as e:
            print("ML prediction error:", e)
    # Fallback: return a random or fixed value
    return 10.0

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code ", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        # Upsert latest status by table id
        table_status_col.update_one(
            {"id": data["id"]},
            {"$set": data},
            upsert=True
        )
        # Insert into history
        historical_col.insert_one(data)
    except Exception as e:
        print("Error processing MQTT message:", e)

def mqtt_worker():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()

def start_mqtt():
    thread = threading.Thread(target=mqtt_worker, daemon=True)
    thread.start()

app = FastAPI()

# Allow CORS for dashboard frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    start_mqtt()

@app.get("/")
def read_root():
    return {"status": "Backend is running"}

@app.get("/api/current_status")
def get_current_status():
    tables = list(table_status_col.find({}, {"_id": 0}))
    return {"tables": tables}

@app.get("/api/historical_data")
def get_historical_data(limit: int = 100):
    # Return the most recent N records
    records = list(historical_col.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit))
    return {"history": records}

@app.get("/api/predict_wait_time")
def api_predict_wait_time(table_id: str = "table001"):
    wait_time = predict_wait_time(table_id)
    return {"table_id": table_id, "predicted_wait_time": wait_time} 