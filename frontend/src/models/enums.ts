/**
 * models/enums.ts – TypeScript enumerations mirroring backend core/enums.py.
 *
 * Rules:
 *   - Keep in sync with backend app/core/enums.py.
 *   - Never re-derive these values; import from this file everywhere.
 */

export enum RelativeFrame {
  QSW = 'QSW',
  TNW = 'TNW',
  LOS = 'LOS',
  DOCK = 'DOCK',
}

export enum RelativeModelMode {
  KGD_QNS_J2 = 'KGD_QNS_J2',
  KGD_QNS_J2_DRAG = 'KGD_QNS_J2_DRAG',
  HCW = 'HCW',
  TRUTH_DIFFERENCE = 'TRUTH_DIFFERENCE',
}

export enum MissionPhaseType {
  FAR_RANGE_TRANSFER = 'FAR_RANGE_TRANSFER',
  ROE_HOMING = 'ROE_HOMING',
  CLOSING = 'CLOSING',
  HOLD_POINT = 'HOLD_POINT',
  INSPECTION = 'INSPECTION',
  RETREAT = 'RETREAT',
  ABORT = 'ABORT',
}

export enum GuidanceLawType {
  IMPULSIVE_TRANSFER = 'IMPULSIVE_TRANSFER',
  ROE_HOMING = 'ROE_HOMING',
  CLOSING = 'CLOSING',
  HOLD_POINT = 'HOLD_POINT',
  RETREAT = 'RETREAT',
}

export enum SensorType {
  RANGE_AZ_EL = 'RANGE_AZ_EL',
  LINE_OF_SIGHT = 'LINE_OF_SIGHT',
  CAMERA_FEATURE = 'CAMERA_FEATURE',
}

export enum ExportFormat {
  CSV = 'CSV',
  JSON = 'JSON',
  YAML = 'YAML',
  CIC_OEM = 'CIC_OEM',
}

export enum DragMode {
  NONE = 'NONE',
  DENSITY_MODEL_SPECIFIC = 'DENSITY_MODEL_SPECIFIC',
  DENSITY_MODEL_FREE = 'DENSITY_MODEL_FREE',
}
