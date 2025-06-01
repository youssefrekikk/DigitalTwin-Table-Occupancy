import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the generated data
# Use the correct path and include more features for training

df = pd.read_csv("./data/occupancy.csv")

# Encode table_id
le = LabelEncoder()
df["table_id_encoded"] = le.fit_transform(df["table_id"])

# Use more features for prediction
X = df[["table_id_encoded", "temperature", "noiseLevel", "deviceCount"]]
y = df["duration_minutes"]
model = LinearRegression()
model.fit(X, y)

# Save model and encoder
joblib.dump(model, "ml/wait_time_model.pkl")
joblib.dump(le, "ml/table_id_encoder.pkl")
print("✅ Model trained and saved with extra features.")
