"""
core/conventions.py – Single authoritative source for all coordinate, frame,
quaternion, and angle conventions used in the backend.

Rules:
- Every convention must be documented here.
- Sub-modules must import from this file; they must never re-derive conventions.
- Any change here is a breaking change for the whole backend.

References:
  [1] Montenbruck & Gill, "Satellite Orbits", 2000.
  [2] Vallado, "Fundamentals of Astrodynamics and Applications", 4th ed.
  [3] Koenig, Guffanti, D'Amico, "New STMs for Spacecraft Relative Motion in
      Perturbed Orbits", JGCD 2017.
"""

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------

#: Standard gravitational parameter of Earth [m^3 / s^2].
MU_EARTH_M3S2: float = 3.986_004_418e14

#: Mean equatorial radius of Earth [m].
R_EARTH_M: float = 6_378_137.0

#: J2 zonal harmonic coefficient (dimensionless).
J2_EARTH: float = 1.082_626_68e-3

#: Earth rotation rate [rad/s].
OMEGA_EARTH_RADS: float = 7.292_115e-5

# ---------------------------------------------------------------------------
# Inertial frame definition
# ---------------------------------------------------------------------------

#: Truth inertial frame: Earth-Centred Inertial (ECI), J2000 epoch.
#: Origin     : Earth centre of mass.
#: X-axis     : vernal equinox direction at J2000.0.
#: Z-axis     : Earth north celestial pole at J2000.0.
#: Y-axis     : completes right-handed triad.
#: Units      : metres and metres/second.
INERTIAL_FRAME = "ECI_J2000"

# ---------------------------------------------------------------------------
# Local orbital frame (QSW) definition
# ---------------------------------------------------------------------------

#: QSW (also called LVLH or RSW) frame, origin at the reference spacecraft.
#: Q-axis (R) : unit vector in the radial direction (r / |r|).
#: S-axis (S) : unit vector in the along-track direction, completing the plane
#:              with W: S = W × Q.
#: W-axis (W) : unit vector normal to the orbital plane: (r × v) / |r × v|.
#: Note       : the frame rotates with the orbit; it is NOT inertial.
QSW_FRAME_DESCRIPTION = "QSW: Q=radial, S=along-track, W=cross-track (right-handed)"

# ---------------------------------------------------------------------------
# Local orbital frame (TNW) definition
# ---------------------------------------------------------------------------

#: TNW frame, origin at the reference spacecraft.
#: T-axis     : unit vector along the velocity vector (v / |v|).
#: N-axis     : unit vector in the orbit normal direction: (r × v) / |r × v|.
#:              Note: for circular orbits N ≡ W.
#: W-axis     : W = T × N (cross-track, same as QSW-W for circular orbit).
TNW_FRAME_DESCRIPTION = "TNW: T=tangential, N=orbit-normal, W=cross-track (right-handed)"

# ---------------------------------------------------------------------------
# Line-of-sight (LOS) frame definition
# ---------------------------------------------------------------------------

#: LOS frame, origin at the chief/target spacecraft.
#: x_LOS : unit vector pointing from chief to deputy along the LOS.
#: y_LOS : unit vector in the elevation direction (positive up from equatorial).
#: z_LOS : completes right-handed triad.
#: Azimuth   : angle in the local horizontal plane from the S-axis, positive
#:             towards the W-axis.  Range: [0, 2*pi) rad.
#: Elevation : angle above the local horizontal plane.  Range: [-pi/2, pi/2] rad.
LOS_FRAME_DESCRIPTION = "LOS: azimuth from S-axis positive toward W, elevation positive up"

# ---------------------------------------------------------------------------
# Docking frame definition
# ---------------------------------------------------------------------------

#: Docking frame, origin at the deputy docking port.
#: z_DOCK : docking axis (approach direction, positive toward target port).
#: x_DOCK : lateral direction 1.
#: y_DOCK : lateral direction 2 = z_DOCK × x_DOCK.
#: Defined by the deputy vehicle geometry; must be provided as part of Vehicle.
DOCKING_FRAME_DESCRIPTION = "DOCK: z=docking approach axis, x/y lateral, origin at deputy port"

# ---------------------------------------------------------------------------
# Quaternion ordering convention
# ---------------------------------------------------------------------------

#: Repository-wide quaternion convention: SCALAR LAST, i.e. q = [q_x, q_y, q_z, q_w].
#: The scalar (real) component is the last element of the 4-vector.
#: Rotation direction: active rotation of vectors; body-to-inertial if not stated.
#: Normalisation: quaternions must be unit quaternions: |q| = 1.
QUATERNION_CONVENTION = "SCALAR_LAST: [q_x, q_y, q_z, q_w]"

# ---------------------------------------------------------------------------
# Orbital element ordering
# ---------------------------------------------------------------------------

#: Keplerian orbital element ordering used throughout the backend.
#: (a [m], e [-], i [rad], RAAN [rad], omega [rad], M [rad])
#: where:
#:   a     = semi-major axis
#:   e     = eccentricity
#:   i     = inclination
#:   RAAN  = right ascension of the ascending node (Omega)
#:   omega = argument of perigee
#:   M     = mean anomaly
KEPLERIAN_ELEMENT_ORDER = "(a, e, i, RAAN, omega, M)  [m, -, rad, rad, rad, rad]"

# ---------------------------------------------------------------------------
# Quasi-nonsingular ROE ordering
# ---------------------------------------------------------------------------

#: QNS ROE state vector ordering (Koenig–Guffanti–D'Amico convention).
#: delta_alpha_qns = [delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]
#: All components dimensionless (normalised by chief semi-major axis a_c where
#: applicable) except delta_lambda which is an angular quantity in radians.
QNS_ROE_ORDER = "[delta_a, delta_lambda, delta_ex, delta_ey, delta_ix, delta_iy]"

# ---------------------------------------------------------------------------
# Angle wrapping rules
# ---------------------------------------------------------------------------

#: Mean anomaly M      : wrapped to [0, 2*pi) rad.
#: Argument of perigee : wrapped to [0, 2*pi) rad.
#: RAAN                : wrapped to [0, 2*pi) rad.
#: Inclination         : NOT wrapped; valid domain [0, pi] rad.
#: Azimuth (LOS)       : wrapped to [0, 2*pi) rad.
#: Elevation (LOS)     : NOT wrapped; valid domain [-pi/2, pi/2] rad.
ANGLE_WRAPPING_RULES = (
    "M, omega, RAAN, azimuth: [0, 2*pi);  "
    "inclination: [0, pi];  "
    "elevation: [-pi/2, pi/2]"
)

# ---------------------------------------------------------------------------
# Sign conventions for azimuth and elevation
# ---------------------------------------------------------------------------

#: Azimuth:   measured from the S-axis (along-track), positive toward the W-axis
#:            (cross-track), in the local horizontal plane.
#: Elevation: measured from the local horizontal plane toward the orbit-normal
#:            (W-axis), positive upward.
AZ_EL_SIGN_CONVENTION = (
    "azimuth positive from S toward W;  elevation positive toward W"
)

# ---------------------------------------------------------------------------
# Unit system
# ---------------------------------------------------------------------------

#: All internal values are SI.
#: At API boundaries, units must be declared explicitly.
#: Silent conversion between unit families is forbidden.
INTERNAL_UNIT_SYSTEM = "SI: metres, seconds, radians, kilograms, newtons"
