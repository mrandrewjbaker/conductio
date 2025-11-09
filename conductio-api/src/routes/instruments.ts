import { Router, Request, Response } from 'express';
import { ApiResponse, Instrument, InstrumentCategory } from '../types';
import { ConductioService } from '../services/conductioService';

const router = Router();

router.get('/', async (req: Request, res: Response) => {
  try {
    const result = await ConductioService.listInstruments();
    
    if (result.success && result.instruments) {
      const response: ApiResponse<Instrument[]> = {
        success: true,
        data: result.instruments
      };
      res.json(response);
    } else {
      res.status(500).json({
        success: false,
        error: 'Failed to list instruments',
        message: result.error || 'Unknown error'
      } as ApiResponse);
    }
    
  } catch (error) {
    console.error('Instrument listing error:', error);
    res.status(500).json({
      success: false,
      error: 'Instrument listing failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    } as ApiResponse);
  }
});

router.get('/categories', async (req: Request, res: Response) => {
  try {
    const result = await ConductioService.listInstruments();
    
    if (result.success && result.instruments) {
      // Group instruments by category
      const categoriesMap = new Map<string, Instrument[]>();
      
      result.instruments.forEach(instrument => {
        if (!categoriesMap.has(instrument.category)) {
          categoriesMap.set(instrument.category, []);
        }
        categoriesMap.get(instrument.category)!.push(instrument);
      });
      
      const categories: InstrumentCategory[] = Array.from(categoriesMap.entries()).map(
        ([name, instruments]) => ({
          name,
          instruments: instruments.sort((a, b) => a.id - b.id)
        })
      );
      
      // Sort categories in a logical order
      const categoryOrder = ['Popular', 'Piano', 'Guitar', 'Bass', 'Strings', 'Brass', 'Woodwinds', 'Synth'];
      categories.sort((a, b) => {
        const aIndex = categoryOrder.indexOf(a.name);
        const bIndex = categoryOrder.indexOf(b.name);
        if (aIndex === -1 && bIndex === -1) return a.name.localeCompare(b.name);
        if (aIndex === -1) return 1;
        if (bIndex === -1) return -1;
        return aIndex - bIndex;
      });
      
      const response: ApiResponse<InstrumentCategory[]> = {
        success: true,
        data: categories
      };
      res.json(response);
    } else {
      res.status(500).json({
        success: false,
        error: 'Failed to list instrument categories',
        message: result.error || 'Unknown error'
      } as ApiResponse);
    }
    
  } catch (error) {
    console.error('Instrument categories error:', error);
    res.status(500).json({
      success: false,
      error: 'Instrument categories listing failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    } as ApiResponse);
  }
});

export { router as instrumentRoutes };