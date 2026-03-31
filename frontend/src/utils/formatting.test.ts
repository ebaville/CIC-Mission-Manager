/**
 * utils/formatting.test.ts – Unit tests for formatting utilities.
 */

import { describe, it, expect } from 'vitest';
import { formatRange, formatAngleDeg, formatDuration } from './formatting';

describe('formatRange', () => {
  it('formats values below 1000 m in metres', () => {
    expect(formatRange(500)).toBe('500.0 m');
  });

  it('formats values at exactly 1000 m in km', () => {
    expect(formatRange(1000)).toBe('1.000 km');
  });

  it('formats values above 1000 m in km', () => {
    expect(formatRange(42195)).toBe('42.195 km');
  });
});

describe('formatAngleDeg', () => {
  it('converts radians to degrees with default 2 decimals', () => {
    expect(formatAngleDeg(Math.PI)).toBe('180.00°');
  });

  it('converts zero radians', () => {
    expect(formatAngleDeg(0)).toBe('0.00°');
  });

  it('respects custom decimal places', () => {
    expect(formatAngleDeg(Math.PI / 2, 1)).toBe('90.0°');
  });
});

describe('formatDuration', () => {
  it('formats zero seconds as 00:00:00', () => {
    expect(formatDuration(0)).toBe('00:00:00');
  });

  it('formats 90 seconds as 00:01:30', () => {
    expect(formatDuration(90)).toBe('00:01:30');
  });

  it('formats one hour as 01:00:00', () => {
    expect(formatDuration(3600)).toBe('01:00:00');
  });

  it('formats a complex value correctly', () => {
    // 2h 15min 7s = 8107s
    expect(formatDuration(8107)).toBe('02:15:07');
  });
});
