import { useState, useEffect } from 'react';

interface HealthResponse {
  status: string;
  service: string;
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || '';
    fetch(`${apiUrl}/api/health`)
      .then((res) => res.json())
      .then((data: HealthResponse) => setHealth(data))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem' }}>
      <h1>Rusha App</h1>
      <p>Welcome to your Rusha application.</p>
      {health && (
        <p>
          API Status: <strong>{health.status}</strong> ({health.service})
        </p>
      )}
      {error && <p style={{ color: 'red' }}>API Error: {error}</p>}
    </div>
  );
}

export default App;
