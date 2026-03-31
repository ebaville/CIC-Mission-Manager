"""
physics/roe_propagation.py – ROE-based relative orbit propagation.

Provides:
  StateTransitionMatrixProvider  – Abstract interface for STM computation.
  KoenigGuffantiDamicoSTM        – KGD 2017 closed-form STM for QNS ROE.
  RoeSTMPropagator               – Propagates ROE state using an STM provider.
  RelativePerturbationConfig     – Perturbation model selection for the STM.

Governing equations:
  delta_alpha(t) = Phi(t, t0) * delta_alpha(t0)
  delta_alpha(t) = Phi(t, t0) * delta_alpha(t0) + Gamma(t, t0) * u  [with control]

  where Phi is the 6x6 closed-form STM from Koenig–Guffanti–D'Amico 2017.

Perturbation content of the KGD STM:
  - Keplerian relative motion (Kepler drift)
  - J2 zonal harmonic (secular effects on RAAN and omega)
  - Differential atmospheric drag (optional, two drag modes)

Validity domain:
  - Arbitrary eccentricity chief orbit.
  - Small deputy formation relative to chief (first-order theory).
  - J2 is dominant; higher-order harmonics not included.
  - Drag model assumes constant or slowly varying Ballistic Coefficient difference.

References:
  [1] Koenig, Guffanti, D'Amico, "New STMs for Spacecraft Relative Motion in
      Perturbed Orbits", JGCD 2017. DOI: 10.2514/1.G001514
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from app.core.enums import DragMode
from app.domain.states import KeplerianElements, QnsRoeState


# ---------------------------------------------------------------------------
# Perturbation configuration
# ---------------------------------------------------------------------------

@dataclass
class RelativePerturbationConfig:
    """Perturbation configuration for the relative dynamics STM.

    Attributes:
        use_j2               : Include J2 in the STM.
        use_differential_drag: Include differential drag in the STM.
        drag_mode            : Drag formulation to use.
        ballistic_coeff_diff : Difference in ballistic coefficient (deputy - chief)
                               [kg/m^2], required for density-model-specific mode.
    """

    use_j2: bool = True
    use_differential_drag: bool = False
    drag_mode: DragMode = DragMode.NONE
    ballistic_coeff_diff: float = 0.0


# ---------------------------------------------------------------------------
# STM interface
# ---------------------------------------------------------------------------

class StateTransitionMatrixProvider(ABC):
    """Abstract interface for relative STM computation."""

    @abstractmethod
    def compute_phi(
        self,
        chief_mean_elements: KeplerianElements,
        dt_s: float,
        perturbation_config: RelativePerturbationConfig,
    ) -> NDArray[np.float64]:
        """Compute the 6×6 relative-motion state transition matrix.

        Args:
            chief_mean_elements: Mean Keplerian elements of the chief at epoch t0.
            dt_s               : Propagation time [s].
            perturbation_config: Perturbation model selection.

        Returns:
            Phi: 6×6 state transition matrix mapping
                 delta_alpha(t0) → delta_alpha(t0 + dt_s).
        """


# ---------------------------------------------------------------------------
# KGD STM implementation
# ---------------------------------------------------------------------------

class KoenigGuffantiDamicoSTM(StateTransitionMatrixProvider):
    """Koenig–Guffanti–D'Amico analytical STM for QNS ROE.

    Implements the closed-form 6×6 STM derived in KGD 2017 for the
    quasi-nonsingular ROE state.

    The STM is computed analytically (no numerical integration) and includes:
      - Keplerian relative motion drift terms.
      - J2 secular drift of RAAN and argument of perigee (when use_j2=True).
      - Differential drag (when use_differential_drag=True).

    The STM structure (symbolic, see paper for full expressions):
      Phi = Phi_Kep + Phi_J2 + Phi_drag

    Status: stub – structure defined, full algebraic expressions are TODO.

    References:
      [1] Koenig, Guffanti, D'Amico, JGCD 2017, Eq. (27)–(42).
    """

    def compute_phi(
        self,
        chief_mean_elements: KeplerianElements,
        dt_s: float,
        perturbation_config: RelativePerturbationConfig,
    ) -> NDArray[np.float64]:
        """Compute the KGD 6×6 STM for QNS ROE.

        Returns a 6×6 identity matrix as a placeholder until the full
        algebraic expressions are implemented.
        """
        # TODO: implement full KGD STM
        # Pseudo-code:
        #
        #   a = chief_mean_elements.a_m
        #   e = chief_mean_elements.e
        #   i = chief_mean_elements.i_rad
        #   omega = chief_mean_elements.omega_rad
        #
        #   n = sqrt(mu / a^3)         # mean motion [rad/s]
        #   T = 2*pi / n               # orbital period [s]
        #
        #   # Keplerian drift term:
        #   # Phi_Kep = I + d_Phi_Kep * dt
        #   # where d_Phi_Kep[1,0] = -3/2 * n  (semi-major → mean longitude coupling)
        #
        #   # J2 secular rates (when use_j2):
        #   # d_omega/dt = 3/4 * J2 * (Re/p)^2 * n * (5*cos(i)^2 - 1)
        #   # d_RAAN/dt  = -3/2 * J2 * (Re/p)^2 * n * cos(i)
        #   # p = a*(1-e^2)   (semi-latus rectum)
        #
        #   # Build Phi from Keplerian, J2, drag contributions
        #   # ...
        #
        #   return Phi  # shape (6, 6)
        raise NotImplementedError(
            "KoenigGuffantiDamicoSTM.compute_phi is not yet implemented."
        )


# ---------------------------------------------------------------------------
# ROE STM propagator
# ---------------------------------------------------------------------------

class RoeSTMPropagator:
    """Propagates the QNS ROE state using an STM provider.

    This is the default relative-motion propagator.  It does NOT integrate
    ODEs; instead it evaluates the analytical STM and applies it to the state.

    For manoeuvre planning, a control input matrix Gamma can be added.

    Attributes:
        stm_provider: STM computation backend (default: KoenigGuffantiDamicoSTM).
    """

    def __init__(
        self,
        stm_provider: StateTransitionMatrixProvider | None = None,
    ) -> None:
        self.stm_provider = stm_provider or KoenigGuffantiDamicoSTM()

    def propagate(
        self,
        roe_k: QnsRoeState,
        chief_mean_elements_k: KeplerianElements,
        dt_s: float,
        perturbation_config: RelativePerturbationConfig | None = None,
        control_delta_v_mps: NDArray[np.float64] | None = None,
    ) -> QnsRoeState:
        """Propagate ROE state by dt_s seconds.

        Args:
            roe_k                 : Current QNS ROE state at epoch t_k.
            chief_mean_elements_k : Chief mean Keplerian elements at epoch t_k.
            dt_s                  : Propagation time step [s].
            perturbation_config   : Perturbation model configuration.
            control_delta_v_mps   : Optional delta-v impulse [m/s] in QSW frame.

        Returns:
            QnsRoeState at epoch t_k + dt_s.
        """
        # TODO: implement ROE propagation via STM
        # Pseudo-code:
        #
        #   config = perturbation_config or RelativePerturbationConfig()
        #   Phi = self.stm_provider.compute_phi(chief_mean_elements_k, dt_s, config)
        #
        #   vec_k   = roe_k.as_vector()
        #   vec_k1  = Phi @ vec_k
        #
        #   if control_delta_v_mps is not None:
        #       Gamma = compute_control_influence_matrix(chief_mean_elements_k, dt_s)
        #       vec_k1 += Gamma @ control_delta_v_mps
        #
        #   return QnsRoeState.from_vector(vec_k1,
        #                                  chief_a_m=roe_k.chief_a_m,
        #                                  epoch_s=roe_k.epoch_s + dt_s)
        raise NotImplementedError("RoeSTMPropagator.propagate is not yet implemented.")
