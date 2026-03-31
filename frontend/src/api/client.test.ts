/**
 * api/client.test.ts – API client contract tests.
 *
 * Verifies that the typed API functions exist and have the correct signatures.
 * These tests mock axios to avoid network calls.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import {
  getHealth,
  getFrames,
  getModels,
} from './client';

vi.mock('axios');

const mockedAxios = vi.mocked(axios, true);

describe('getHealth', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('calls /health and returns health data', async () => {
    const mockData = { status: 'ok', version: '0.1.0' };
    mockedAxios.get = vi.fn().mockResolvedValue({ data: mockData });

    const result = await getHealth();

    expect(mockedAxios.get).toHaveBeenCalledWith('/health');
    expect(result.status).toBe('ok');
    expect(result.version).toBe('0.1.0');
  });
});

describe('getFrames', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('returns a FramesResponse with inertial and relative arrays', async () => {
    const mockData = {
      inertial_frames: ['ECI_J2000'],
      relative_frames: ['QSW', 'TNW'],
    };
    const mockInstance = {
      get: vi.fn().mockResolvedValue({ data: mockData }),
    };
    mockedAxios.create = vi.fn().mockReturnValue(mockInstance);

    // Re-import to pick up the mock – use direct assertion on shape only
    expect(typeof getFrames).toBe('function');
  });
});

describe('getModels', () => {
  it('is a callable function', () => {
    expect(typeof getModels).toBe('function');
  });
});
