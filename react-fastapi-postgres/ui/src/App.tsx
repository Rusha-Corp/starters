import { useEffect, useState, Component, ReactNode } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api',
});

interface HealthResponse {
  status: string;
  version: string;
  db?: string;
}

/**
 * Error boundary component for graceful error handling
 */
interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div style={{ color: 'red', padding: '2rem' }}>
            <h2>Something went wrong</h2>
            <p>{this.state.error?.message}</p>
            <button onClick={() => window.location.reload()}>Reload</button>
          </div>
        )
      );
    }
    return this.props.children;
  }
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const checkHealth = () => {
    setLoading(true);
    setError(null);
    
    api
      .get<HealthResponse>('/health')
      .then((res) => {
        setHealth(res.data);
        setLoading(false);
      })
      .catch((err: unknown) => {
        const message = err instanceof Error ? err.message : 'Unknown error';
        setError(message);
        setLoading(false);
        
        // Retry after 5 seconds on failure
        setTimeout(checkHealth, 5000);
      });
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <ErrorBoundary>
      <main style={{ fontFamily: 'system-ui', maxWidth: 640, margin: '4rem auto', padding: '0 1rem' }}>
        <h1>🚀 react-fastapi-postgres</h1>
        <p>Your Rusha starter project is running.</p>

        <section>
          <h2>API Health</h2>
          {loading && <p>Checking API…</p>}
          {error && (
            <p style={{ color: 'red' }}>
              Could not reach API: {error}
              <button 
                onClick={checkHealth}
                style={{ marginLeft: '1rem', cursor: 'pointer' }}
              >
                Retry
              </button>
            </p>
          )}
          {health && !loading && (
            <pre style={{ background: '#f4f4f4', padding: '1rem', borderRadius: 4 }}>
              {JSON.stringify(health, null, 2)}
            </pre>
          )}
        </section>
      </main>
    </ErrorBoundary>
  );
}
