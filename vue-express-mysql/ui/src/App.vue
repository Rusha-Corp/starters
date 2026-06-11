<script setup lang="ts">
import { ref, onMounted } from 'vue';

interface ApiStatus {
  status: string;
  service: string;
  database: string;
  timestamp: string;
}

const apiStatus = ref<ApiStatus | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

async function fetchStatus() {
  try {
    const response = await fetch('/api/status');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    apiStatus.value = await response.json();
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Failed to connect to API';
  } finally {
    loading.value = false;
  }
}

onMounted(fetchStatus);
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>Vue Express MySQL</h1>
      <p>Full-stack starter with Vue, Express, and MySQL</p>
    </header>

    <main class="main">
      <section class="status-card">
        <h2>API Status</h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="apiStatus" class="status">
          <p><strong>Status:</strong> {{ apiStatus.status }}</p>
          <p><strong>Service:</strong> {{ apiStatus.service }}</p>
          <p><strong>Database:</strong> {{ apiStatus.database }}</p>
          <p><strong>Timestamp:</strong> {{ apiStatus.timestamp }}</p>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.app {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  font-family: system-ui, -apple-system, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #42b883;
}

.main {
  display: flex;
  justify-content: center;
}

.status-card {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  min-width: 300px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.status-card h2 {
  margin-top: 0;
  color: #333;
}

.loading {
  color: #666;
}

.error {
  color: #e74c3c;
}

.status p {
  margin: 0.5rem 0;
}
</style>
