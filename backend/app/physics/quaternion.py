"""
physics/quaternion.py – Quaternion mathematics.

Convention (repository-wide, see core/conventions.py):
  SCALAR LAST: q = [q_x, q_y, q_z, q_w]
  Unit quaternion: |q| = 1
  Rotation semantics: active rotation of vectors; body-to-inertial if not stated.

Provides:
  Quaternion            – Quaternion wrapper with algebra operations.
  quaternion_multiply   – Hamilton product.
  quaternion_conjugate  – Conjugate (= inverse for unit quaternions).
  quaternion_normalize  – Normalise to unit length.
  quaternion_to_dcm     – Convert to 3×3 direction cosine matrix.
  dcm_to_quaternion     – Convert 3×3 DCM to quaternion (Shepperd's method).
  quaternion_error      – Attitude error quaternion between two quaternions.
  rotate_vector         – Rotate a 3-vector by a unit quaternion.

Governing equations:
  Kinematics: dq/dt = 0.5 * q ⊗ [omega_x, omega_y, omega_z, 0]
              where omega is angular velocity in body frame.

References:
  [1] Shepperd, "Quaternion from rotation matrix", JGCD 1978.
  [2] Schaub & Junkins, "Analytical Mechanics of Space Systems", 3rd ed.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


class Quaternion:
    """Scalar-last unit quaternion wrapper.

    Internal representation: numpy array [q_x, q_y, q_z, q_w].
    All operations preserve the scalar-last convention.

    Usage:
        q = Quaternion([0.0, 0.0, 0.0, 1.0])   # identity
        q_inv = q.conjugate()
        q_product = q1.multiply(q2)
    """

    __slots__ = ("_q",)

    def __init__(self, components: NDArray[np.float64] | list[float]) -> None:
        self._q = np.asarray(components, dtype=np.float64)
        if self._q.shape != (4,):
            raise ValueError("Quaternion must be initialised with a 4-element array.")

    @classmethod
    def identity(cls) -> "Quaternion":
        """Return the identity quaternion [0, 0, 0, 1]."""
        return cls([0.0, 0.0, 0.0, 1.0])

    @property
    def array(self) -> NDArray[np.float64]:
        """Return the underlying [q_x, q_y, q_z, q_w] array."""
        return self._q.copy()

    @property
    def q_xyz(self) -> NDArray[np.float64]:
        """Return the vector part [q_x, q_y, q_z]."""
        return self._q[:3].copy()

    @property
    def q_w(self) -> float:
        """Return the scalar part q_w."""
        return float(self._q[3])

    @property
    def norm(self) -> float:
        """Return the quaternion norm."""
        return float(np.linalg.norm(self._q))

    @property
    def is_unit(self) -> bool:
        """Return True if the quaternion is normalised to within 1e-9."""
        return abs(self.norm - 1.0) < 1e-9

    def normalize(self) -> "Quaternion":
        """Return a normalised copy of this quaternion."""
        n = self.norm
        if n < 1e-15:
            raise ValueError("Cannot normalise a zero quaternion.")
        return Quaternion(self._q / n)

    def conjugate(self) -> "Quaternion":
        """Return the quaternion conjugate q* = [-q_xyz, q_w].

        For unit quaternions, conjugate equals inverse.
        """
        return Quaternion(np.array([-self._q[0], -self._q[1], -self._q[2], self._q[3]]))

    def multiply(self, other: "Quaternion") -> "Quaternion":
        """Compute the Hamilton product self ⊗ other.

        Uses the scalar-last convention throughout.
        """
        # TODO: implement Hamilton product for scalar-last convention
        # Pseudo-code (scalar-last [qx, qy, qz, qw]):
        #   q1 = self._q;  q2 = other._q
        #   w1, w2 = q1[3], q2[3]
        #   v1, v2 = q1[:3], q2[:3]
        #
        #   w_out = w1*w2 - dot(v1, v2)
        #   v_out = w1*v2 + w2*v1 + cross(v1, v2)
        #
        #   return Quaternion([v_out[0], v_out[1], v_out[2], w_out])
        raise NotImplementedError("Quaternion.multiply is not yet implemented.")

    def rotate_vector(self, v: NDArray[np.float64]) -> NDArray[np.float64]:
        """Rotate a 3-vector by this unit quaternion.

        Computes: v_out = q ⊗ [v, 0] ⊗ q*

        Args:
            v: 3-element vector to rotate.

        Returns:
            Rotated 3-vector.
        """
        # TODO: implement active vector rotation
        # Pseudo-code:
        #   q_v = Quaternion([v[0], v[1], v[2], 0.0])
        #   q_rot = self.multiply(q_v).multiply(self.conjugate())
        #   return q_rot.q_xyz
        raise NotImplementedError("Quaternion.rotate_vector is not yet implemented.")

    def to_dcm(self) -> NDArray[np.float64]:
        """Convert to 3×3 direction cosine matrix (DCM).

        Returns:
            DCM R such that v_B = R @ v_I (body from inertial).
        """
        # TODO: implement quaternion → DCM conversion
        # Pseudo-code (scalar-last [qx, qy, qz, qw]):
        #   qx, qy, qz, qw = self._q
        #   R = [[1 - 2*(qy^2+qz^2), 2*(qx*qy - qz*qw), 2*(qx*qz + qy*qw)],
        #        [2*(qx*qy + qz*qw), 1 - 2*(qx^2+qz^2), 2*(qy*qz - qx*qw)],
        #        [2*(qx*qz - qy*qw), 2*(qy*qz + qx*qw), 1 - 2*(qx^2+qy^2)]]
        #   return R
        raise NotImplementedError("Quaternion.to_dcm is not yet implemented.")

    @classmethod
    def from_dcm(cls, dcm: NDArray[np.float64]) -> "Quaternion":
        """Convert a 3×3 DCM to a unit quaternion using Shepperd's method.

        Args:
            dcm: 3×3 direction cosine matrix.

        Returns:
            Unit Quaternion in scalar-last convention.
        """
        # TODO: implement DCM → quaternion using Shepperd's method
        # Pseudo-code:
        #   trace = dcm[0,0] + dcm[1,1] + dcm[2,2]
        #   # find maximum component to avoid numerical issues near singularities
        #   # ... (see Shepperd 1978)
        raise NotImplementedError("Quaternion.from_dcm is not yet implemented.")

    def attitude_error(self, q_ref: "Quaternion") -> "Quaternion":
        """Compute the attitude error quaternion relative to a reference.

        delta_q = q_ref^-1 ⊗ self

        Args:
            q_ref: Reference (desired) attitude quaternion.

        Returns:
            Error quaternion delta_q.
        """
        return q_ref.conjugate().multiply(self)

    def __repr__(self) -> str:
        q = self._q
        return f"Quaternion([{q[0]:.6f}, {q[1]:.6f}, {q[2]:.6f}, {q[3]:.6f}])"


def quaternion_kinematics(
    q: NDArray[np.float64],
    omega_body_rads: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Compute quaternion time derivative from angular velocity.

    Governing equation:
        dq/dt = 0.5 * q ⊗ [omega_x, omega_y, omega_z, 0]

    Args:
        q             : Current quaternion [q_x, q_y, q_z, q_w].
        omega_body_rads: Angular velocity in body frame [rad/s], shape (3,).

    Returns:
        dq/dt as a 4-element array [dq_x/dt, dq_y/dt, dq_z/dt, dq_w/dt].
    """
    # TODO: implement quaternion kinematics
    # Pseudo-code:
    #   omega_quat = [omega_body_rads[0], omega_body_rads[1], omega_body_rads[2], 0.0]
    #   dq_dt = 0.5 * hamilton_product(q, omega_quat)
    #   return dq_dt
    raise NotImplementedError("quaternion_kinematics is not yet implemented.")
