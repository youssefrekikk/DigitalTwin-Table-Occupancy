# Digital Twin Table Occupancy System

A modern, simulated digital twin system for monitoring and managing table occupancy in cafés and restaurants. This project demonstrates IoT, real-time analytics, and ML predictions using simulated data, MQTT, FastAPI, MongoDB, and a React dashboard.

---

## 📁 Project Structure

- `simulator/` — Simulates table occupancy data and publishes to MQTT
- `ml/` — Machine learning scripts for wait time prediction
- `backend/` — FastAPI backend (API, MQTT, MongoDB, ML integration)
- `dashboard/` — React frontend for real-time monitoring and analytics
- `data/` — Generated historical data for ML
- `docker-compose.yml` — Orchestrates all services

---

## 🏗️ How It Works

- **Simulator**: Publishes realistic table occupancy data (temperature, noise, device count, etc.) to MQTT.
- **Backend**: Subscribes to MQTT, stores data in MongoDB, exposes REST API for real-time status, analytics, and ML predictions.
- **ML**: Predicts wait times using historical data and simple regression.
- **Dashboard**: Visualizes live table status, analytics, and ML predictions.

---

## 🚦 Quick Start

1. **Clone the repository**
   ```bash
   git clone <this-repo-url>
   cd DigitalTwin-Table-Occupancy
   ```
2. **Generate data and train the ML model**
   ```bash
   python ml/generate_data.py
   python ml/train_model.py
   ```
3. **Build and launch all services**
   ```bash
   docker-compose up --build
   ```
4. **Access the dashboard**
   - [http://localhost:3000](http://localhost:3000)

---

## 🌐 API Endpoints

- `/api/current_status` — Real-time table status
- `/api/historical_data` — Historical occupancy events
- `/api/predict_wait_time?table_id=...` — ML wait time prediction

---

## 🛠️ Development

- All code is in subfolders (`simulator/`, `ml/`, `backend/`, `dashboard/`).
- Use `docker-compose` for full stack, or run each service individually for development.
- PRs and contributions welcome!

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

**Built with ❤️ for the IoT and Digital Twin community**
