import joblib

# Load model and encoder
model = joblib.load("ml/wait_time_model.pkl")
encoder = joblib.load("ml/table_id_encoder.pkl")

def estimate_wait_time(table_id="table001"):
    encoded = encoder.transform([table_id])[0]
    predicted = model.predict([[encoded]])[0]
    return round(predicted, 2)

if __name__ == "__main__":
    all_tables = ["table001", "table002", "table003", "table004"]
    all_occupied = True  # You can replace this with Orion API call later

    if all_occupied:
        wait_times = [estimate_wait_time(tid) for tid in all_tables]
        print(f"🚦 Estimated Wait Time: {round(sum(wait_times) / len(wait_times), 2)} minutes")
