import { Router, Request, Response } from 'express';
import path from 'path';
import fs from 'fs/promises';

const router = Router();

interface ExistingFile {
  id: string;
  fileName: string;
  layer: string;
  filePath: string;
  audioPath?: string;
  midiPath?: string;
  createdAt: Date;
  metadata: {
    genre: string;
    key: string;
    bpm: number;
    bars: number;
    instrument: string;
  };
}

// Use absolute path to the conductio-service output directory
const OUTPUT_DIR = '/Users/abaker/me.workspace/conductio/conductio-service/output';

// List all existing generated files
router.get('/', async (req: Request, res: Response) => {
  try {
    const existingFiles: ExistingFile[] = [];
    
    // Check if output directory exists
    try {
      await fs.access(OUTPUT_DIR);
    } catch {
      return res.json({
        success: true,
        data: []
      });
    }

    // Read all .mcpkg directories
    const entries = await fs.readdir(OUTPUT_DIR, { withFileTypes: true });
    const mcpkgDirs = entries.filter(entry => entry.isDirectory() && entry.name.endsWith('.mcpkg'));

    for (const dir of mcpkgDirs) {
      const dirPath = path.join(OUTPUT_DIR, dir.name);
      
      try {
        const dirContents = await fs.readdir(dirPath);
        
        // Find MIDI and audio files
        const midiFiles = dirContents.filter(file => file.endsWith('.mid'));
        const audioFiles = dirContents.filter(file => file.endsWith('.wav'));
        
        for (const midiFile of midiFiles) {
          const baseName = path.basename(midiFile, '.mid');
          const layer = baseName; // melody.mid -> melody
          
          // Get file stats for creation date
          const midiPath = path.join(dirPath, midiFile);
          const stats = await fs.stat(midiPath);
          
          // Check if corresponding audio file exists
          const audioFile = audioFiles.find(audio => 
            path.basename(audio, '.wav') === baseName
          );
          
          // Extract metadata from folder name (e.g., "wild_canyon_melody.mcpkg")
          const folderBaseName = path.basename(dir.name, '.mcpkg');
          const parts = folderBaseName.split('_');
          
          // Default metadata (we can't extract all details from filename)
          const metadata = {
            genre: 'unknown',
            key: 'C minor',
            bpm: 120,
            bars: 8,
            instrument: 'auto'
          };

          const existingFile: ExistingFile = {
            id: `${dir.name}_${baseName}`,
            fileName: audioFile ? `${folderBaseName}.wav` : `${folderBaseName}.mid`,
            layer: layer,
            filePath: audioFile ? path.join(dirPath, audioFile) : midiPath,
            audioPath: audioFile ? path.join(dirPath, audioFile) : undefined,
            midiPath: midiPath,
            createdAt: stats.mtime,
            metadata
          };

          existingFiles.push(existingFile);
        }
      } catch (error) {
        console.error(`Error reading directory ${dir.name}:`, error);
        continue;
      }
    }

    // Sort by creation date (newest first)
    existingFiles.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

    return res.json({
      success: true,
      data: existingFiles
    });

  } catch (error) {
    console.error('Error scanning existing files:', error);
    return res.status(500).json({
      success: false,
      error: 'Failed to scan existing files',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Serve a file for download/streaming
router.get('/file/:fileId', async (req: Request, res: Response) => {
  try {
    const fileId = req.params.fileId;
    
    // Parse the file ID to get directory and file info
    const parts = fileId.split('_');
    if (parts.length < 3) {
      return res.status(400).json({
        success: false,
        error: 'Invalid file ID format'
      });
    }
    
    // Reconstruct the directory name and layer
    const dirName = `${parts[0]}_${parts[1]}_${parts[2]}.mcpkg`;
    const layer = parts[3] || parts[2]; // fallback for different naming patterns
    
    const dirPath = path.join(OUTPUT_DIR, dirName);
    
    // Look for audio file first, then MIDI
    const preferAudio = req.query.format !== 'midi';
    let filePath: string;
    let mimeType: string;
    
    if (preferAudio) {
      const audioPath = path.join(dirPath, `${layer}.wav`);
      try {
        await fs.access(audioPath);
        filePath = audioPath;
        mimeType = 'audio/wav';
      } catch {
        // Fallback to MIDI
        filePath = path.join(dirPath, `${layer}.mid`);
        mimeType = 'audio/midi';
      }
    } else {
      filePath = path.join(dirPath, `${layer}.mid`);
      mimeType = 'audio/midi';
    }

    // Check if file exists
    try {
      await fs.access(filePath);
    } catch {
      return res.status(404).json({
        success: false,
        error: 'File not found'
      });
    }

    // Set headers and stream the file
    const fileName = path.basename(filePath);
    res.setHeader('Content-Type', mimeType);
    res.setHeader('Content-Disposition', `attachment; filename="${fileName}"`);
    
    return res.sendFile(path.resolve(filePath));
    
  } catch (error) {
    console.error('Error serving file:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to serve file',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

export { router as filesRoutes };