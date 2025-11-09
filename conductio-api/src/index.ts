import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import { generationRoutes } from './routes/generation';
import { instrumentRoutes } from './routes/instruments';
import { healthRoutes } from './routes/health';
import { filesRoutes } from './routes/files';

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Set higher timeout for music generation requests (5 minutes)
app.use('/api/generate', (req, res, next) => {
  req.setTimeout(5 * 60 * 1000); // 5 minutes
  res.setTimeout(5 * 60 * 1000); // 5 minutes
  next();
});

// Routes
app.use('/api/health', healthRoutes);
app.use('/api/generate', generationRoutes);
app.use('/api/instruments', instrumentRoutes);
app.use('/api/files', filesRoutes);

// Global error handler
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Error:', err);
  res.status(500).json({
    success: false,
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use('*', (req: express.Request, res: express.Response) => {
  res.status(404).json({
    success: false,
    error: 'Route not found',
    message: `Cannot ${req.method} ${req.originalUrl}`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🎵 Conductio API server running on port ${PORT}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
  console.log(`🎼 API Documentation: http://localhost:${PORT}/api/health/info`);
});

export default app;