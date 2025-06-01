import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Typography, Grid, Card, CardContent, Button, TextField } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000/api';

function App() {
  const [tables, setTables] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedTable, setSelectedTable] = useState('table001');
  const [waitTime, setWaitTime] = useState(null);

  // Fetch current table status
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await axios.get(`${API_BASE}/current_status`);
        setTables(res.data.tables);
      } catch (e) {}
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  // Fetch historical data
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(`${API_BASE}/historical_data?limit=100`);
        setHistory(res.data.history);
      } catch (e) {}
    };
    fetchHistory();
  }, []);

  // Fetch wait time prediction
  const handlePredict = async () => {
    try {
      const res = await axios.get(`${API_BASE}/predict_wait_time?table_id=${selectedTable}`);
      setWaitTime(res.data.predicted_wait_time);
    } catch (e) {
      setWaitTime('N/A');
    }
  };

  // Prepare chart data
  const chartData = {
    labels: history.map((h) => h.timestamp),
    datasets: [
      {
        label: 'Occupancy (deviceCount)',
        data: history.map((h) => h.deviceCount),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom>Table Occupancy Dashboard</Typography>
      <Grid container spacing={2}>
        {tables.map((table) => (
          <Grid item xs={12} sm={6} md={3} key={table.id}>
            <Card sx={{ background: table.occupied ? '#ffe0e0' : '#e0ffe0' }}>
              <CardContent>
                <Typography variant="h6">{table.id}</Typography>
                <Typography>Occupied: {table.occupied ? 'Yes' : 'No'}</Typography>
                <Typography>Device Count: {table.deviceCount}</Typography>
                <Typography>Temp: {table.temperature}°C</Typography>
                <Typography>Noise: {table.noiseLevel} dB</Typography>
                <Typography variant="caption">{table.timestamp}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Typography variant="h5" sx={{ mt: 4 }}>Historical Analytics</Typography>
      <Line data={chartData} />

      <Typography variant="h5" sx={{ mt: 4 }}>Wait Time Prediction</Typography>
      <Grid container spacing={2} alignItems="center">
        <Grid item>
          <TextField
            label="Table ID"
            value={selectedTable}
            onChange={(e) => setSelectedTable(e.target.value)}
            size="small"
          />
        </Grid>
        <Grid item>
          <Button variant="contained" onClick={handlePredict}>Predict</Button>
        </Grid>
        <Grid item>
          {waitTime !== null && (
            <Typography>Predicted Wait Time: <b>{waitTime} min</b></Typography>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default App; 