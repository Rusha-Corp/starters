import { useState, useEffect } from 'react';

interface Status {
  status: string;
  database?: string;
}

function App() {
  const [status, setStatus] = useState<Status | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || '';
    fetch(`${apiUrl}/api/status`)
      .then((res) => res.json())
      .then((data) => {
        setStatus(data);
        setLoading(false);
      })
      .catch(() => {
        setStatus({ status: 'error' });
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', maxWidth: 600, margin: '2rem auto', padding: '0 1rem' }}>
      <h1>Rusha App</h1>
      <p>React + Go Fiber + PostgreSQL</p>
      <div style={{ marginTop: '1rem', padding: '1rem', border: '1px solid #ddd', borderRadius: 8 }}>
        <h2>API Status</h2>
        {loading ? (
          <p>Loading…</p>
        ) : (
          <pre style={{ fontSize: 14 }}>{JSON.stringify(status, null, 2)}</pre>
        )}
      </div>
    </div>
  );
}

export default App;
