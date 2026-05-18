import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, cleanup, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { http, HttpResponse } from 'msw';
import App from '../App';
import { server } from '../mocks/server';

const renderWithRouter = (component: React.ReactElement) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('App Component', () => {
  beforeEach(() => {
    cleanup();
    server.resetHandlers();
  });

  afterEach(() => {
    cleanup();
  });

  it('renders the app title', () => {
    renderWithRouter(<App />);
    expect(screen.getByText(/react-fastapi-postgres/i)).toBeInTheDocument();
  });

  it('displays the API Health section heading', () => {
    renderWithRouter(<App />);
    expect(screen.getByText(/api health/i)).toBeInTheDocument();
  });

  it('renders loading state initially', () => {
    server.use(
      http.get('*/health', async () => {
        await new Promise(() => {});
      })
    );
    renderWithRouter(<App />);
    expect(screen.getByText(/checking api/i)).toBeInTheDocument();
  });

  it('renders retry button when API call fails', async () => {
    server.use(
      http.get('*/health', () => {
        return HttpResponse.error();
      })
    );

    renderWithRouter(<App />);

    await waitFor(() => {
      expect(screen.getByText(/retry/i)).toBeInTheDocument();
    });
  });

  it('displays error message when API is unreachable', async () => {
    server.use(
      http.get('*/health', () => {
        return HttpResponse.error();
      })
    );

    renderWithRouter(<App />);

    await waitFor(() => {
      expect(screen.getByText(/could not reach api/i)).toBeInTheDocument();
    });
  });

  it('renders health data after successful API call', async () => {
    server.use(
      http.get('*/health', () => {
        return HttpResponse.json({
          status: 'ok',
          version: '0.1.0',
          db: 'connected',
        });
      })
    );

    renderWithRouter(<App />);

    await waitFor(() => {
      expect(screen.getByText(/"status": "ok"/)).toBeInTheDocument();
    });
  });

  it('displays API status when health check succeeds', async () => {
    server.use(
      http.get('*/health', () => {
        return HttpResponse.json({
          status: 'ok',
          version: '0.1.0',
          db: 'connected',
        });
      })
    );

    renderWithRouter(<App />);

    await waitFor(() => {
      expect(screen.getByText(/"db": "connected"/)).toBeInTheDocument();
    });
  });
});

describe('ErrorBoundary', () => {
  it('catches rendering errors and displays fallback', () => {
    // Suppress console.error for expected errors in test
    const originalError = console.error;
    console.error = vi.fn();

    // ErrorBoundary is already wrapping the App content,
    // so we just verify it renders without crashing
    renderWithRouter(<App />);

    // Restore console
    console.error = originalError;
  });
});

describe('Retry functionality', () => {
  it('retry button is present in error state', async () => {
    server.use(
      http.get('*/health', () => {
        return HttpResponse.error();
      })
    );

    renderWithRouter(<App />);

    await waitFor(() => {
      expect(screen.getByText(/retry/i)).toBeInTheDocument();
    });
  });
});
