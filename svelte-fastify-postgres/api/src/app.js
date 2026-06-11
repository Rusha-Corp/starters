const Fastify = require('fastify');
const cors = require('@fastify/cors');
const { Pool } = require('pg');

const PORT = parseInt(process.env.PORT || '3000', 10);
const DATABASE_URL = process.env.DATABASE_URL || 'postgres://postgres:postgres@localhost:5432/appdb';

const app = Fastify({ logger: true });

// PostgreSQL connection pool
const pool = new Pool({ connectionString: DATABASE_URL });

pool.on('error', (err) => {
  app.log.error('Unexpected pg pool error', err);
});

// Plugins
app.register(cors, { origin: true });

// Health check
app.get('/health', async () => {
  return { status: 'ok' };
});

// API status with DB connectivity check
app.get('/api/status', async () => {
  let dbConnected = false;
  try {
    const client = await pool.connect();
    await client.query('SELECT 1');
    client.release();
    dbConnected = true;
  } catch {
    dbConnected = false;
  }

  return {
    status: dbConnected ? 'ok' : 'degraded',
    database: dbConnected ? 'connected' : 'disconnected',
    timestamp: new Date().toISOString(),
  };
});

// Start server
const start = async () => {
  try {
    await app.listen({ port: PORT, host: '0.0.0.0' });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
