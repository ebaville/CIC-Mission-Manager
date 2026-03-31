/**
 * utils/formatting.ts – Display formatting utilities.
 *
 * Converts SI values to human-readable strings.
 * No physics logic here.
 */

/** Format a distance in metres to a human-readable string. */
export function formatRange(rangeM: number): string {
  if (rangeM < 1000) {
    return `${rangeM.toFixed(1)} m`;
  }
  return `${(rangeM / 1000).toFixed(3)} km`;
}

/** Format an angle in radians as degrees with specified decimal places. */
export function formatAngleDeg(rad: number, decimals = 2): string {
  return `${((rad * 180) / Math.PI).toFixed(decimals)}°`;
}

/** Format a duration in seconds as HH:MM:SS. */
export function formatDuration(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return [h, m, s].map((v) => String(v).padStart(2, '0')).join(':');
}
