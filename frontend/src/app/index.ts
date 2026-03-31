/**
 * src/app/index.ts – Application-level configuration constants.
 *
 * Centralised location for app-wide constants that should not be duplicated.
 */

/** Base URL for the backend API. Proxied by Vite in development. */
export const API_BASE_URL = '/api/v1';

/** Default simulation time step [s]. */
export const DEFAULT_TIME_STEP_S = 10.0;

/** Default relative dynamics model (must match backend default). */
export const DEFAULT_RELATIVE_MODEL = 'KGD_QNS_J2';

/** Application version string. */
export const APP_VERSION = '0.1.0';
