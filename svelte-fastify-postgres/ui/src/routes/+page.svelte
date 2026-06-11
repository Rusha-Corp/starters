<script>
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:3000';

  let status = $state(null);
  let loading = $state(false);
  let error = $state(null);

  async function checkStatus() {
    loading = true;
    error = null;
    try {
      const res = await fetch(`${apiUrl}/api/status`);
      status = await res.json();
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="hero">
  <h1>Svelte + Fastify + PostgreSQL</h1>
  <p>A full-stack starter with SvelteKit, Fastify, and PostgreSQL.</p>

  <button onclick={checkStatus} disabled={loading}>
    {loading ? 'Checking...' : 'Check API Status'}
  </button>

  {#if error}
    <p class="error">Error: {error}</p>
  {/if}

  {#if status}
    <div class="status">
      <p><strong>Status:</strong> {status.status}</p>
      <p><strong>Database:</strong> {status.database}</p>
      <p><strong>Timestamp:</strong> {status.timestamp}</p>
    </div>
  {/if}
</div>

<style>
  .hero {
    text-align: center;
    padding: 3rem 0;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
  }

  p {
    color: #666;
    margin-bottom: 1.5rem;
  }

  button {
    background: #ff3e00;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border-radius: 4px;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .status {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 4px;
    text-align: left;
  }

  .status p {
    color: #333;
    margin-bottom: 0.25rem;
  }

  .error {
    color: #d32f2f;
    margin-top: 1rem;
  }
</style>
