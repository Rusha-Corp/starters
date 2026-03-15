import { useEffect, useState } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api',
});

interface HealthResponse {
  status: string;
  version: string;
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<HealthResponse>('/health')
      .then((res) => setHealth(res.data))
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error';
        setError(message);
      });
  }, []);

  return (
    <main style={{ fontFamily: 'system-ui', maxWidth: 640, margin: '4rem auto', padding: '0 1rem' }}>
      <h1>🚀 react-fastapi-postgres</h1>
      <p>Your Rusha starter project is running.</p>

      <section>
        <h2>API Health</h2>
        {health && (
          <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: 4 }}>
            {JSON.stringify(health, null, 2)}
          </pre>
        )}
        {error && <p style={{ color: 'red' }}>Could not reach API: {error}</p>}
        {!health && !error && <p>Checking API…</p>}
      </section>
    </main>
  );
}
