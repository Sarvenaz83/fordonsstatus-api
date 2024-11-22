import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "https://<your-api-gateway-url>/dev"; // Replace with your deployed API Gateway URL

function App() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    // Fetch vehicles from the backend
    axios
      .get(`${API_URL}/vehicles`)
      .then((response) => {
        setVehicles(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Failed to fetch vehicles");
        setLoading(false);
      });
  }, []);

  const createVehicle = () => {
    axios
      .post(`${API_URL}/vehicles`, {
        model: "Volvo XC90",
        status: "active",
      })
      .then((response) => {
        alert("Vehicle created successfully!");
        setVehicles((prev) => [...prev, response.data]);
      })
      .catch((err) => {
        alert("Failed to create vehicle");
      });
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <h1>Fordonsstatus</h1>
      <button onClick={createVehicle}>Add Vehicle</button>
      <ul>
        {vehicles.map((vehicle) => (
          <li key={vehicle.id}>
            <strong>{vehicle.model}</strong> - {vehicle.status}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
