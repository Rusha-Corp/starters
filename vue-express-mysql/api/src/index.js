const express = require('express');
const cors = require('cors');
const mysql = require('mysql2/promise');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// MySQL connection pool
let pool;

async function initDatabase() {
  pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '3306', 10),
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'app',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
  });

  try {
    const conn = await pool.getConnection();
    console.log('Connected to MySQL database');
    conn.release();
  } catch (err) {
    console.error('MySQL connection failed:', err.message);
  }
}

// Health check endpoint
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// API status endpoint
app.get('/api/status', async (_req, res) => {
  let dbStatus = 'disconnected';
  try {
    if (pool) {
      await pool.query('SELECT 1');
      dbStatus = 'connected';
    }
  } catch {
    dbStatus = 'error';
  }

  res.json({
    status: 'ok',
    service: 'api',
    database: dbStatus,
    timestamp: new Date().toISOString(),
  });
});

// Start server
initDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`API server running on port ${PORT}`);
  });
});
