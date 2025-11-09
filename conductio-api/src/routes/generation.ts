import { Router, Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import path from 'path';
import fs from 'fs/promises';
import { GenerationRequest, GenerationResponse, ApiResponse } from '../types';
import { ConductioService } from '../services/conductioEngine';

const router = Router();

// Store generation jobs in memory (in production, use a database)
const generationJobs = new Map<string, {
  id: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  request: GenerationRequest;
  result?: any;
  error?: string;
  createdAt: Date;
}>();

router.post('/', async (req: Request, res: Response) => {
  try {
    // Set request timeout specifically for this route
    req.setTimeout(5 * 60 * 1000); // 5 minutes
    res.setTimeout(5 * 60 * 1000); // 5 minutes
    
    const request: GenerationRequest = req.body;
    
    // Validate request
    if (!request.layer || !['melody', 'bass', 'drums', 'chords'].includes(request.layer)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid layer',
        message: 'Layer must be one of: melody, bass, drums, chords'
      } as ApiResponse);
    }
    
    console.log(`🎵 Starting ${request.layer} generation...`);
    
    // Generate music synchronously
    const result = await ConductioService.generateLayer(request);
    
    if (!result.success || !result.outputPath) {
      return res.status(500).json({
        success: false,
        error: 'Generation failed',
        message: result.error || 'Unknown error during generation'
      } as ApiResponse);
    }
    
    // Determine which file to send back
    const outputDir = result.outputPath;
    const layer = request.layer;
    const renderAudio = request.renderAudio !== false; // Default to true
    
    let filePath: string;
    let mimeType: string;
    let fileExtension: string;
    
    if (renderAudio) {
      // Try to send audio file first
      const audioFile = path.join(outputDir, `${layer}.wav`);
      try {
        await fs.access(audioFile);
        filePath = audioFile;
        mimeType = 'audio/wav';
        fileExtension = 'wav';
        console.log(`🎶 Streaming audio file: ${audioFile}`);
      } catch {
        // Fallback to MIDI if audio not found
        const midiFile = path.join(outputDir, `${layer}.mid`);
        await fs.access(midiFile); // This will throw if MIDI also doesn't exist
        filePath = midiFile;
        mimeType = 'audio/midi';
        fileExtension = 'mid';
        console.log(`🎼 Streaming MIDI file (audio not available): ${midiFile}`);
      }
    } else {
      // MIDI only requested
      const midiFile = path.join(outputDir, `${layer}.mid`);
      await fs.access(midiFile);
      filePath = midiFile;
      mimeType = 'audio/midi';
      fileExtension = 'mid';
      console.log(`🎼 Streaming MIDI file: ${midiFile}`);
    }
    
    // Generate a creative filename
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const creativeFolder = path.basename(outputDir, '.mcpkg');
    const filename = `${creativeFolder}.${fileExtension}`;
    
    // Set headers for file download
    res.setHeader('Content-Type', mimeType);
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.setHeader('X-Generation-Info', JSON.stringify({
      layer: request.layer,
      genre: request.genre || 'general',
      key: request.key || 'C minor',
      bpm: request.bpm || 120,
      bars: request.bars || 8,
      instrument: request.instrument || 'auto',
      fileType: fileExtension,
      createdAt: timestamp
    }));
    
    // Stream the file
    return res.sendFile(path.resolve(filePath));
    
  } catch (error) {
    console.error('Generation request error:', error);
    return res.status(500).json({
      success: false,
      error: 'Generation failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    } as ApiResponse);
  }
});

// Async generation endpoint (for longer generations)
router.post('/async', async (req: Request, res: Response) => {
  try {
    const request: GenerationRequest = req.body;
    
    // Validate request
    if (!request.layer || !['melody', 'bass', 'drums', 'chords'].includes(request.layer)) {
      return res.status(400).json({
        success: false,
        error: 'Invalid layer',
        message: 'Layer must be one of: melody, bass, drums, chords'
      } as ApiResponse);
    }
    
    // Generate unique job ID
    const jobId = uuidv4();
    
    // Store job
    generationJobs.set(jobId, {
      id: jobId,
      status: 'processing',
      request,
      createdAt: new Date()
    });
    
    // Start generation asynchronously
    generateLayerAsync(jobId, request);
    
    // Return immediate response with job ID
    const response: GenerationResponse = {
      success: true,
      data: {
        id: jobId,
        layer: request.layer,
        genre: request.genre || 'general',
        key: request.key || 'C minor',
        bpm: request.bpm || 120,
        bars: request.bars || 8,
        instrument: request.instrument || 'auto',
        outputPath: '', // Will be filled when complete
        midiFile: '', // Will be filled when complete
        createdAt: new Date().toISOString()
      }
    };
    
    return res.status(202).json(response); // 202 Accepted
    
  } catch (error) {
    console.error('Async generation request error:', error);
    return res.status(500).json({
      success: false,
      error: 'Generation failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    } as ApiResponse);
  }
});

router.get('/status/:id', (req: Request, res: Response) => {
  const jobId = req.params.id;
  const job = generationJobs.get(jobId);
  
  if (!job) {
    return res.status(404).json({
      success: false,
      error: 'Job not found',
      message: `No generation job found with ID: ${jobId}`
    } as ApiResponse);
  }
  
  const response: ApiResponse = {
    success: true,
    data: {
      id: job.id,
      status: job.status,
      request: job.request,
      result: job.result,
      error: job.error,
      createdAt: job.createdAt.toISOString()
    }
  };
  
  return res.json(response);
});

router.get('/download/:id/:type', async (req: Request, res: Response) => {
  const { id: jobId, type } = req.params;
  const job = generationJobs.get(jobId);
  
  if (!job || job.status !== 'completed' || !job.result) {
    return res.status(404).json({
      success: false,
      error: 'File not found',
      message: 'Job not found, not completed, or no files available'
    } as ApiResponse);
  }
  
  try {
    let filePath: string;
    let mimeType: string;
    
    if (type === 'midi') {
      filePath = job.result.midiFile;
      mimeType = 'audio/midi';
    } else if (type === 'audio' && job.result.audioFile) {
      filePath = job.result.audioFile;
      mimeType = 'audio/wav';
    } else {
      return res.status(400).json({
        success: false,
        error: 'Invalid file type',
        message: 'Type must be "midi" or "audio"'
      } as ApiResponse);
    }
    
    // Check if file exists
    await fs.access(filePath);
    
    // Set headers and send file
    res.setHeader('Content-Type', mimeType);
    res.setHeader('Content-Disposition', `attachment; filename="${path.basename(filePath)}"`);
    return res.sendFile(path.resolve(filePath));
    
  } catch (error) {
    console.error('Download error:', error);
    return res.status(500).json({
      success: false,
      error: 'Download failed',
      message: 'Could not access or send file'
    } as ApiResponse);
  }
});

async function generateLayerAsync(jobId: string, request: GenerationRequest) {
  const job = generationJobs.get(jobId);
  if (!job) return;
  
  try {
    job.status = 'processing';
    
    const result = await ConductioService.generateLayer(request);
    
    if (result.success && result.outputPath) {
      // Find generated files
      const outputDir = result.outputPath;
      const layer = request.layer;
      
      const midiFile = path.join(outputDir, `${layer}.mid`);
      const audioFile = path.join(outputDir, `${layer}.wav`);
      
      // Check which files exist
      const midiExists = await fs.access(midiFile).then(() => true).catch(() => false);
      const audioExists = await fs.access(audioFile).then(() => true).catch(() => false);
      
      job.status = 'completed';
      job.result = {
        outputPath: outputDir,
        midiFile: midiExists ? midiFile : null,
        audioFile: audioExists ? audioFile : null,
        layer: request.layer,
        genre: request.genre || 'general',
        key: request.key || 'C minor',
        bpm: request.bpm || 120,
        bars: request.bars || 8,
        instrument: request.instrument || 'auto'
      };
      
    } else {
      job.status = 'failed';
      job.error = result.error || 'Unknown generation error';
    }
    
  } catch (error) {
    job.status = 'failed';
    job.error = error instanceof Error ? error.message : 'Unknown error';
    console.error(`Generation job ${jobId} failed:`, error);
  }
}

export { router as generationRoutes };